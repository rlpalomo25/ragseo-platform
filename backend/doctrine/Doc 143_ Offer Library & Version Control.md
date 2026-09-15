# Doc 143: The Offer Library & Version Control Protocol

**Version:** 1.0
**Date:** 2026-03-29

## 1.0 Purpose: To Systematize Persuasion

This document defines **The Offer Library & Version Control Protocol**, the central repository for every testable marketing offer in the system. Its purpose is to transform our calls to action from static text into a managed, version-controlled library of persuasive assets. 

This protocol directly addresses the "Offer System Still Light" gap identified by Luther, operationalizing the principles of Hormozi's "Grand Slam Offer" at scale. We no longer have "CTAs"; we have versioned, tracked, and optimized offers.

## 2.0 The Core Principle: Offers Are Managed Assets

An offer is not just a button. It is a discrete, testable asset with a unique identity, a version history, and a performance record. Every offer is managed through this central library, ensuring that we can track the performance of every headline, every piece of copy, and every button text change across the entire portfolio.

## 3.0 The Offer Library

This library is the single source of truth for all offers. Every offer is assigned a unique ID and version number.

| Offer ID | Version | Offer Name | Headline | Body Copy | CTA Button Text | Status | Impression Threshold |
| :---

> **Quick Reference**
> **Owns:** The management and tracking of all active marketing offers.
> **Rule 1:** Only approved offers from this library may be used in content.
> **Rule 2:** Every offer must have a defined version number and tracking parameter.
> **Rule 3:** Expired or underperforming offers must be archived, not deleted.
> **If/Then:** If launching a new campaign, select the offer with the highest historical conversion rate for that audience segment.

---
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OFR-001` | 1.0 | Standard Quote | Get a Free, No-Obligation Quote | Find out exactly how much it will cost to protect your home with the nation's top-rated gutter guard. | Get My Free Quote | `Active` | 50,000 |
| `OFR-001` | 1.1 | Standard Quote + Urgency | Get a Free, No-Obligation Quote This Week | Prices are updated monthly. Lock in your price by scheduling a quote this week. | Get My Free Quote Now | `Testing` | 50,000 |
| `OFR-002` | 1.0 | Buyer's Guide | Download the Free Gutter Guard Buyer's Guide | Our 10-page guide reveals the 3 questions you must ask before buying any gutter guard. | Download the Guide | `Active` | 25,000 |

### 3.1 Version Control Protocol

- **Minor Version (e.g., 1.0 → 1.1):** Any change to the headline, body copy, or button text requires a new minor version.
- **Major Version (e.g., 1.2 → 2.0):** A fundamental change to the value proposition (e.g., adding a discount, changing the deliverable) requires a new major version.
- **Status:** An offer can be `Active` (approved for use), `Testing` (currently in an A/B test via Doc 211), `Fatigued` (performance has decayed, pending rotation), or `Archived` (no longer in use but kept for historical data).

## 4.0 Page-Level Offer Tracking

To connect offers to performance, every content asset in the system must have the following metadata field:

- **`Active_Offer_ID`**: The full ID and version number of the offer currently displayed on that page (e.g., `OFR-001-v1.1`).

This creates an unbreakable link between a specific page's conversion rate and the exact offer version that produced it.

## 5.0 The Offer Fatigue & Auto-Rotation Protocol

This protocol prevents winning offers from decaying silently. It ensures that we are actively managing offer performance and rotating in fresh creative before the old offer dies completely.

1.  **Impression Monitoring:** The **System Governor (Doc 230)** continuously monitors the total impressions for every `Active` offer on every page.
2.  **Fatigue Detection Trigger:** Once an offer crosses its **Impression Threshold**, a new monitoring rule is activated. If the offer's **conversion rate drops by more than 25% from its peak** for a sustained period (14 days), its status is automatically changed to `Fatigued`.
3.  **Automated Rotation:** The Governor immediately and automatically replaces the `Fatigued` offer with the next available `Active` offer version for that Offer ID (e.g., rotates from `OFR-001-v1.0` to `OFR-001-v1.1`).
4.  **Escalation:** If no other `Active` version is available in the library, the Governor escalates the issue to the **CRO Lead** with the mandate: **"Create new offer version for `[Offer ID]` to combat fatigue."**

## 6.0 The Winner Replication Engine

This protocol ensures that a winning test is not an isolated event, but a new piece of intelligence that is systematically deployed across the portfolio. It is how the system learns and compounds its gains.

1.  **Winner Declaration:** When **Doc 211 (A/B Testing & Experimentation Protocol)** declares a winner in an offer test, it sends a `WINNER_DECLARED` signal to this protocol.
2.  **Candidate List Generation:** Upon receiving the signal, the system generates a **Replication Candidate List**. This is a list of all other pages in the portfolio that meet the following criteria:
    *   **Similar Page Type:** (e.g., blog post, landing page)
    *   **Similar Audience Intent:** (e.g., informational, transactional)
    *   **Currently using an older or lower-performing version of the same Offer ID.**
3.  **Automated Rollout:** The **System Governor (Doc 230)** creates a new optimization task for each page on the Replication Candidate List. The task is to replace the existing offer with the newly-crowned winner.
4.  **Confirmation & Monitoring:** The system monitors the performance of the new offer on the replicated pages to ensure that the lift is consistent.

This engine transforms every A/B test from a one-time optimization into a system-wide upgrade.

## 7.0 Integration with the Governance Layer

This library is not a standalone document; it is a core component of the optimization engine.

- **Doc 204 (Performance Enforcement & Optimization Protocol):** Playbook #2 (CTA Enhancement) is now modified. Instead of prescribing text, it will now instruct the operator to **"Select a new offer version from the Doc 143 Offer Library to test."**
- **Doc 211 (A/B Testing):** When an A/B test is run on an offer, the results (winner, loser, statistical significance) are recorded directly in the Offer Library against the tested versions. This is how the library learns.
- **Doc 230 (System Governor):** The Governor is responsible for ensuring that the `Active_Offer_ID` on a page's metadata matches the offer being rendered to the user, ensuring data integrity.

This protocol elevates our offers from simple CTAs to a fully managed, data-driven system for improving conversion. It is the engine that will power our revenue growth.