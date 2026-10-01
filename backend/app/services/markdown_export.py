"""Render an approved job's writer draft as a standalone Markdown file.

The draft itself is stored verbatim in the writer AgentTask's ``output_data``
(``output.content_markdown``, produced by ``run_writer``), so exporting is a
read + format job: nothing is regenerated and no model is called.
"""

import json
import re
import unicodedata

from sqlalchemy.orm import Session as DBSession

from app.models.agent_task import AgentTask
from app.models.job import AgentJob, JobStage

# Only these six fields are lifted into the front matter. Ordered deliberately:
# the three SEO fields are always present (WriterMeta requires them with
# min_length=1); the rest are optional and omitted when empty.
FRONT_MATTER_FIELDS = (
    "title",
    "meta_title",
    "meta_description",
    "brand",
    "content_type",
    "archetype",
)

MAX_FILENAME_LENGTH = 80


def select_writer_output(db: DBSession, job: AgentJob) -> dict | None:
    """Return the ``output`` dict of the newest writer stage that has a draft.

    Scans writer stages newest-first rather than taking the latest stage
    unconditionally. A revision loop can create several writer stages, and
    ``retry_job`` preserves earlier ones as ``skipped``, so the newest stage may
    hold no usable output. Skipping empty ones also filters out failed tasks:
    ``run_agent`` only writes ``output_data`` on success.

    The models define no ORM ``relationship()``, so stage->task is an explicit
    join rather than ``stage.task``.
    """
    tasks = (
        db.query(AgentTask)
        .join(JobStage, JobStage.task_id == AgentTask.id)
        .filter(JobStage.job_id == job.id, JobStage.agent_type == "writer")
        .order_by(JobStage.sequence.desc())
        .all()
    )

    for task in tasks:
        output = (task.output_data or {}).get("output")
        if not isinstance(output, dict):
            continue
        if (output.get("content_markdown") or "").strip():
            return output
    return None


def _yaml_scalar(value: object) -> str:
    """Quote a value as a YAML double-quoted scalar.

    ``json.dumps`` emits a valid YAML double-quoted string, so colons, quotes,
    hashes, newlines and leading dashes need no hand-rolled escaping.
    """
    return json.dumps(str(value), ensure_ascii=False)


def build_markdown(output: dict) -> str:
    """Build a Markdown document with YAML front matter and the draft verbatim."""
    lines = ["---"]
    for field in FRONT_MATTER_FIELDS:
        value = output.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            continue
        lines.append(f"{field}: {_yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + output["content_markdown"]


def _slug(text: str | None) -> str:
    """Reduce text to an ASCII filename stem, or "" if nothing usable remains."""
    if not text:
        return ""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug[:MAX_FILENAME_LENGTH].strip("-")


def slugify(text: str | None, fallback: str) -> str:
    """Build an ASCII filename stem, falling back when there is nothing usable."""
    return _slug(text) or _slug(fallback) or "draft"


def build_filename(output: dict, job: AgentJob) -> str:
    """``<title-slug>.md`` for Content-Disposition, with the job id as backstop.

    Tries each candidate in turn rather than nesting fallbacks, so a title that
    is entirely punctuation does not swallow the job id.
    """
    stem = _slug(output.get("title")) or _slug(job.title) or str(job.id)
    return f"{stem}.md"