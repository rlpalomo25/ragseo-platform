import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.database import Base, get_db
from app.main import app
from app.models.agent_task import AgentTask
from app.models.chunk import DocChunk
from app.models.document import DocReference, Document
from app.models.external import (
    AIOverviewImpressions,
    Backlink,
    CallTracking,
    DomainMetric,
    DomainReport,
    ExternalExport,
    GA4Event,
    KeywordEstimate,
    LeadSummary,
    SearchConsoleDaily,
    SearchConsoleDim,
    TopPage,
)
from app.models.job import AgentJob, JobStage
from app.models.learning import ContentPerformanceSnapshot, ContentPublication, LearningSignal
from app.models.user import Session as UserSession
from app.models.user import User
from fastapi.testclient import TestClient
from pgvector.sqlalchemy import Vector
from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker


@compiles(Vector, "sqlite")
def _compile_vector_sqlite(type_, compiler, **kw):
    return "BLOB"


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

ALL_TABLES = [
    User.__table__,
    UserSession.__table__,
    Document.__table__,
    DocReference.__table__,
    AgentTask.__table__,
    DocChunk.__table__,
    AgentJob.__table__,
    JobStage.__table__,
    ExternalExport.__table__,
    SearchConsoleDim.__table__,
    SearchConsoleDaily.__table__,
    AIOverviewImpressions.__table__,
    KeywordEstimate.__table__,
    Backlink.__table__,
    TopPage.__table__,
    CallTracking.__table__,
    LeadSummary.__table__,
    GA4Event.__table__,
    DomainReport.__table__,
    DomainMetric.__table__,
    ContentPublication.__table__,
    ContentPerformanceSnapshot.__table__,
    LearningSignal.__table__,
]


@pytest.fixture(autouse=True)
def disable_embeddings(monkeypatch):
    """Keep the suite hermetic: no real embedding API calls.

    Tests that exercise the embedding providers re-enable it explicitly and
    stub the HTTP layer.
    """
    from app.config import get_settings

    get_settings().embedding_provider = "none"


@pytest.fixture(autouse=True)
def no_celery_broker(monkeypatch):
    """Keep the suite hermetic: dispatch must never touch the Redis broker.

    ``create_job`` → ``run_agent_task.delay()`` would otherwise open a real
    connection to ``settings.redis_url`` (failing hard when Redis is down).
    Tests that want the recorded-dispatch assertions re-monkeypatch this on
    their own (see test_orchestrator.py's ``no_celery`` fixture).
    """
    monkeypatch.setattr(
        "app.tasks.run_agent_task.delay",
        lambda *args, **kwargs: None,
    )


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine, tables=ALL_TABLES)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine, tables=ALL_TABLES)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def test_user(db_session):
    from app.services.auth_service import hash_password

    user = User(username="testwriter", password_hash=hash_password("secret123"), role="writer")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture()
def admin_user(db_session):
    from app.services.auth_service import hash_password

    user = User(username="testadmin", password_hash=hash_password("adminpass"), role="admin")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def login(client, username, password):
    return client.post("/api/auth/login", json={"username": username, "password": password})


def seed_doc(db, doc_number, title, content, version="1.0"):
    doc = Document(
        doc_number=doc_number,
        title=title,
        filename=f"Doc {doc_number}_ {title}.md",
        content=content,
        version=version,
        series=doc_number[0] + "00",
        status="active",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@pytest.fixture()
def doctrine_corpus(db_session):
    """Mini doctrine corpus covering every governing doc agents reference."""
    seed_doc(
        db_session,
        "100",
        "Master Content Doctrine",
        "# Master Content Doctrine\n\nCore content rules live here.",
        version="8.6",
    )
    seed_doc(
        db_session,
        "130",
        "MasterShield Brand Module",
        "# MasterShield Brand Module\n\nVoice: The Guardian Engineer. Problem-first posture.",
        version="5.8",
    )
    seed_doc(
        db_session,
        "131",
        "Klean Gutter Brand Module",
        "# Klean Gutter Brand Module\n\nVoice: DIY-friendly helper.",
        version="4.2",
    )
    seed_doc(
        db_session,
        "316",
        "MasterShield Writer Agent Instructions",
        "# Writer Instructions\n\nFollow the block order. Three questions above the fold.",
        version="13.8",
    )
    seed_doc(
        db_session,
        "316-C",
        "Comparison and Category Page Structure",
        "# Comparison Page Structure\n\nH1 pattern, comparison table required.",
        version="2.1",
    )
    seed_doc(
        db_session, "320", "Klean Gutter Writer Agent Instructions", "# Klean writer rules", version="13.8"
    )
    seed_doc(db_session, "324", "MMGG Writer Agent Instructions", "# MMGG writer rules", version="13.9")
    seed_doc(
        db_session,
        "132",
        "MMGG Brand Module",
        "# MMGG Brand Module\n\nVoice: Knowledgeable Neighbor.",
        version="6.3",
    )
    seed_doc(
        db_session,
        "328",
        "Auditor Agent Instructions",
        "# Auditor Instructions\n\nCritical fails: structure deviation, missing trust claims.",
        version="16.15",
    )
    return db_session
