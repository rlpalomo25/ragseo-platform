# Doc 205: Closed Loop Enforcement Protocol

**Document:** 205
**Version:** 5.0
**Last Updated:** April 7, 2026

## 1.0 Purpose: The System's Immune Response

This document defines the **Closed-Loop Enforcement Protocol**, the system's automated immune response to content that fails to perform. Its purpose is to ensure that when **Doc 201 (Content Performance Rubric)** identifies a problem, a specific, non-negotiable enforcement action is taken.

This protocol is the critical link that turns monitoring into action. It is the 'enforcement' in Performance Enforcement.

## 2.0 The Core Principle: Interrupt, Triage, Then Act

This protocol operates on a two-speed system. It first checks for high-priority strategic interrupts that require immediate action. If none are present, it proceeds to a standard, revenue-focused triage of the performance issue.

Not all performance issues are created equal. This protocol's primary function is to triage every flagged asset and assign a **Severity Tier**. This tier, combined with the **Opportunity Score from Doc 210**, determines the precise action that the **System Governor (Doc 230)** will take.

## 3.0 Priority Interrupt: The Distribution Enforcement Loop

This is the system's response to Luther's critique that distribution is a secondary concern. It is now a primary, mandatory action under specific conditions.

*   **Trigger:** Asset is received from **Doc 201** with the `DISTRIBUTION_PRIORITY` flag.
*   **Cause:** The asset has a high **Distribution Gap score (>=4)** as per **Doc 210**, indicating high potential but critically low reach.
*   **Mandatory Action:** The **System Governor (Doc 230)** immediately routes the asset to **Stage 9 (Publish & Distribute)** with the non-negotiable instruction: **"Execute Mandatory Seeding Cycle (Doc 125)."**
*   **Next Step:** The standard optimization process is **paused** for this asset. After the seeding cycle is complete, the asset's performance is re-evaluated in the next monthly cycle. This ensures we amplify what we have before we try to fix it.

## 4.0 Standard Triage: The Severity Tiers

If no priority interrupt is triggered, the asset proceeds to the standard severity assessment:

When an asset is flagged by Doc 201, it is assigned one of the following three severity tiers:

| Tier | Name | Criteria | Default Action |
| :--- | :--- | :--- | :--- |
| **1** | **Severe** | The asset is in the bottom 20% of the portfolio for Page-Level ROI **OR** is more than 50% below benchmark on a primary conversion metric. | **Escalate to Steward Delegation Matrix (see Section 4.1)** |

---

### 4.1 Steward Delegation Matrix

When an asset is flagged as **Severity 1**, the following delegation rules apply:

| Condition | Delegate To | Action Required | Timeline |
|-----------|-------------|-----------------|----------|
| **Root cause unknown** | Analyst Agent (Doc 300) | Conduct root cause analysis | 48 hours |
| **Technical issue detected** | Architect Agent (Doc 312) | Create technical fix brief | 24 hours |
| **Content quality issue** | Auditor Agent (Doc 328) | Full content rewrite | 72 hours |
| **Brand voice violation** | Brand Lead | Re-evaluate brand guidelines | 24 hours |
| **Opportunity score < 20** | System Governor (Doc 230) | Archive or deprioritize | Immediate |

**Escalation Protocol:**
1. System Governor flags asset as Severity 1
2. Assigns to appropriate Steward based on matrix above
3. Steward has 24-72 hours to complete action
4. Asset re-enters pipeline with documented fix
5. If no fix possible within 2 cycles, asset is archived
| **2** | **Moderate** | The asset is performing 25-50% below benchmark on any single KPI. | **Automated Optimization Cycle:** The asset is routed to **Doc 204** for a standard optimization playbook. The decision to test vs. replace is determined by **Doc 211 (A/B Testing & Experimentation Protocol)**. |
| **3** | **Minor** | The asset is performing 0-25% below benchmark on any single KPI. | **Monitor & Log:** The issue is logged for monitoring. No immediate action is taken. If the asset is flagged again in the next cycle, it is automatically upgraded to Severity 2. |

## 5.0 The Test-vs-Replace Decision Gateway

For all **Severity 2** issues, the decision to implement a fix directly or to A/B test it is not subjective. It is governed by the rules in **Doc 211 (A/B Testing & Experimentation Protocol)**, which uses the Opportunity Score from Doc 210 to make the final determination.

**Clarification on the Doc 211/39 Edge Case:**

To resolve the potential conflict between this document and Doc 211, the rule is absolute: **Doc 211 is the final authority on the test-vs-replace decision.** This document (Doc 205) provides the *triage* that determines if an asset even gets to the testing gateway. Doc 211 makes the final call once it arrives.

This ensures that our testing resources are focused on the right assets: those with significant potential where a failed change could do more harm than good.

## 6.0 Integration with the System Governor (Doc 230)

This protocol is executed by the System Governor. The process is as follows:

1.  **Trigger:** Doc 201 flags an asset.
2.  **Interrupt Check:** The protocol first checks for the `DISTRIBUTION_PRIORITY` flag. If present, the Mandatory Seeding Cycle is executed, and the process halts for this asset.
3.  **Filter (if no interrupt):** Doc 210 assigns an Opportunity Score. If the score is below the "Do Nothing" threshold, the process stops.
4.  **Triage:** The asset is assigned a Severity Tier (1, 2, or 3) based on the criteria in Section 4.0.
5.  **Action:** Doc 211 executes the action defined by the Severity Tier, routing the asset to the System Steward, the automated optimization cycle (Doc 204 & 41), or the monitoring queue.

This closed-loop process ensures that every performance issue is detected, triaged, and addressed with the appropriate level of urgency and rigor.