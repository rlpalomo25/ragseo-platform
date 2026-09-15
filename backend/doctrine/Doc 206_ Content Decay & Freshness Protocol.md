# Doc 206: Decay and Freshness Protocol

**Version:** 4.0
**Date:** 2026-03-29

## 1.0 Purpose: To Combat Content Entropy

This document defines the **Content Decay & Freshness Protocol**, the system's defense against the natural entropy of content relevance. Its purpose is to ensure that no content asset is allowed to quietly die. It transforms content from a depreciating asset into a managed portfolio where every piece is either performing, being improved, or being retired.

This protocol directly addresses the "Content Decay" gap identified in Luther's final critique.

## 2.0 The Core Principle: Content is a Living Asset

An article is not a static object. It is a living asset whose relevance and accuracy decay over time. This protocol introduces a **Freshness Score** to every content asset. This score is degraded by two vectors: the steady decay of **time** and the immediate impact of **performance drops**. This dual-vector model ensures that the system is both proactive (planning for age) and reactive (responding to market signals).

## 3.0 The Freshness Score

Every content asset is assigned a Freshness Score upon publication.

1.  **Initial Score:** All new or fully refreshed assets start with a **Freshness Score of 100**.
2.  **Decay Rate:** The score decreases by **5 points every 30 days**.
3.  **Floor:** The score cannot go below 0.

> **Formula:** `Freshness Score = MAX(0, 100 - (5 * (Days Since Last Major Update / 30)))`

## 4.0 The Dual-Vector Decay Model

### 4.1 Time-Based Decay (Entropy)

This is the default, predictable decay based on the age of the asset.

- **Decay Rate:** The score decreases by **5 points every 30 days**.
- **Formula:** `Time-Based Penalty = 5 * (Days Since Last Major Update / 30)`

### 4.2 Signal-Based Decay (Performance Triggers)

This is an immediate, penalty-based decay triggered by negative performance signals. These penalties are applied instantly upon detection and stack with time-based decay.

| Signal | Threshold | Freshness Score Penalty |
| :--- | :--- | :--- |
| **Ranking Drop** | Primary keyword ranking drops by >5 positions MoM | **-15 points** |
| **Traffic Drop** | Organic traffic drops by >20% MoM | **-10 points** |
| **Citation Drop** | New referring domains drop by >50% MoM | **-5 points** |

## 5.0 Automated Re-Score & Refresh Triggers

The Freshness Score is not just a metric; it is a trigger that forces action at specific, non-negotiable intervals.

| Trigger Event | Threshold | Mandatory Action |
| :--- | :--- | :--- |
| **Automated Re-Score** | Freshness Score drops **below 70** (approx. 6 months) | The asset is automatically sent back to **Doc 210 (Revenue Intelligence & Prioritization Engine)** for a full re-calculation of its Opportunity Score. This re-introduces the asset into the optimization pool based on its current potential, not its historical performance. |
| **Forced Refresh Review** | Freshness Score drops **below 40** (approx. 12 months) | The asset is flagged for a **Mandatory Refresh Review**. It is escalated to the **System Steward** with a recommendation to either: a) execute a full refresh (re-entering the pipeline at Stage 3), or b) retire the asset and redirect its URL. |

## 6.0 Integration with the System Governor (Doc 230)

This protocol is a time-based, automated function executed by the System Governor.

1.  **Continuous Monitoring:** The Governor continuously monitors both the age of assets (for time-based decay) and their core performance signals (for signal-based decay).
2.  **Score Calculation:** The Freshness Score is recalculated daily, applying both time-based and any new signal-based penalties.
3.  **Trigger Evaluation:** It checks for any assets that have crossed the `Re-Score` (<70) or `Forced Refresh` (<40) thresholds.
3.  **Automated Routing:**
    *   If `Re-Score` is triggered, the asset is immediately sent to the Doc 210 engine.
    *   If `Forced Refresh` is triggered, the asset is escalated to the System Steward's queue.

This protocol ensures that the system is not just fixing broken content, but is actively managing the health and relevance of its entire content portfolio over time. It is the system's long-term memory and short-term memory, preventing valuable assets from being forgotten and once-valuable assets from being forgotten.