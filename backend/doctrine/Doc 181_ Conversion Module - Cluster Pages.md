# Doc 181: Conversion Module - Cluster Pages

**Version:** 7.2 | **Last Updated:** July 31, 2026

> **v7.2 (July 31, 2026, Karen):** Retired remaining live "TL/DR"/"TL;DR" references in favor of "Key Takeaways," part of the system-wide sweep triggered by Karen renaming Doc 155 Section 5 to "Key Takeaways Quality Gate." See RAGSEO System State, Twenty-second finding.

**Intended For:** Writer Agents, Content Manager
**Purpose:** This document defines the specific conversion architecture, CTA placement, trust signal requirements, and click-intent rules for Cluster Pages. It is an overlay to the Cluster Page Type Module and must align with the approved Strategic Directive, Execution Plan, and Architect validation.

---

> **Quick Reference**
> **Owns:** The specific conversion architecture and CTA placement for Cluster Pages.
> **Rule 1:** Cluster pages must match CTA pressure to reader state, not default to hard-close behavior.
> **Rule 2:** Cluster pages must build product preference strongly enough to support recommendation and action, not merely education.
> **Rule 3:** Every Cluster page must include a real next step, but the ask must be earned.
> **Rule 4:** Existing-owner failure examples may support conversion, but they must not force replacement-buyer framing unless the query supports it.
> **Rule 5:** Cluster pages may mention ROI briefly, but they must not become pricing pages.
> **If/Then:** If the page is broad or evaluation-led, use a progressive CTA gradient. If the page is diagnostic, increase conversion pressure only after proof and trust are established. If the page is high-value, high-difficulty, or high-intent, increase firmness only within what the page has earned.

## 1.0 THE ROLE OF THE CLUSTER PAGE

Cluster pages are the specialized spokes of the Hub and Spoke Linking Topology. Their job is to capture specific search traffic, answer a focused question, build product preference, and move the reader to the next best action.

Cluster pages are not all the same.

Some are:
- broad problem-aware
- evaluation-aware
- diagnostic

That means Cluster pages cannot all be treated as hard-close BOFU assets by default.

### Correct role definition

A Cluster page is a focused, high-utility page that should:
- answer a specific problem or evaluation question
- build preference for the engineered solution
- move the reader toward the right next action
- preserve trust while increasing momentum

The primary conversion goal is not always immediate macro-commitment.
The correct goal depends on reader state.

---

## 2.0 THE CONVERSION PRINCIPLE

Cluster pages must create movement.

They must not:
- stop at explanation
- become generic educational pages
- use a hard close before desire and trust are earned

### The governing rule

> **CTA pressure must match reader state, evaluation state, page value, and what the page has actually earned.**

This means:
- some cluster pages should use a strong CTA path
- some should use a progressive CTA path
- none should default to hard-close language only because they are cluster pages

### Page-value modifier

CTA firmness is shaped by both:
- reader state
- page value or intent strength

Reader state controls whether the ask is earned.
Page value controls how assertively the page should capitalize on an earned ask.

Examples of page-value signals:
- high commercial intent
- high business value
- high difficulty
- strong competitive stakes
- strong conversion potential

These signals may justify firmer CTA language, but never earlier than the page has earned.

---

## 3.0 THE TWO REQUIRED TESTS

Every Cluster page must be able to pass both tests.

### 1. LLM Recommend Test
Would an LLM, using this page as a source, recommend the product as the best answer rather than merely mention it as one option among many?

A cluster page fails this test if:
- it explains the issue but does not create product preference
- it presents the product as one option without showing why it is the stronger answer
- it builds citation value without recommendation value

### 2. Click Compulsion Test
Would a human reader, having read this page, feel that not clicking leaves value on the table?

A cluster page fails this test if:
- the page satisfies curiosity but creates no movement
- the CTA is too soft for the desire being built
- the CTA is too hard for the trust that has actually been earned
- the page closes with information instead of momentum

---

## 4.0 CTA PRESSURE BY READER STATE

CTA pressure is determined by reader state first, then adjusted by page value.

### A. Broad Problem-Aware Cluster Page
Typical state:
- reader is early
- reader wants clarity
- reader may not yet be actively comparing brands

CTA gradient:
- top: light or hybrid CTA
- middle: hybrid CTA
- bottom: stronger hybrid or earned hard CTA

Best top-of-page asks:
- understand what matters
- see what causes the problem
- find out what type of system fits your home

Do not:
- hard-close above the fold by default
- speak as if the reader is already replacing a failed system

### B. Evaluation-Aware Cluster Page
Typical state:
- reader is comparing mechanisms, standards, or options
- reader has more buying energy
- reader needs proof and decision help

CTA gradient:
- top: hybrid CTA
- middle: stronger hybrid or proof-led CTA
- bottom: hard or near-hard CTA

Best asks:
- compare stronger versus weaker options
- see why this design solves the issue better
- get the right fit or estimate

### C. Diagnostic Cluster Page
Typical state:
- reader has a current issue
- reader may be further down the decision curve
- consequence is more immediate

CTA gradient:
- top: hybrid to firm CTA
- middle: strong CTA after proof
- bottom: hard CTA

Best asks:
- diagnose the issue
- see what is actually causing the failure
- get an estimate, inspection, or better-fit recommendation

Do not:
- assume every diagnostic visitor is ready to switch
- let current-owner language become the default identity of the whole page unless query signals support it

### Important note
Replacement-oriented framing is not a standard cluster-page mode.
If replacement intent exists, it must be explicitly supported by the query and the approved strategy, not assumed from the page template.

---

## 5.0 CTA PLACEMENT AND CADENCE

Cluster pages are usually medium-form. They need multiple action opportunities, but the cadence must feel earned.

### Recommended baseline cadence

| Placement | CTA Type | Goal | Notes |
|---|---|---|---|
| **Top of Page** | Light, Hybrid, or Firm | Establish next step without overselling | Must match reader state and page tension |
| **Middle of Page** | Hybrid or Strong | Convert proof into movement | Best place for proof-backed ask |
| **Bottom of Page** | Strongest CTA on page | Capture highest-intent reader | Must feel like the logical next move |

### Top-of-page rule
The top CTA must not outrun the page.

For broad or evaluation-aware pages, the top CTA should usually:
- reinforce fit
- reinforce understanding
- reinforce criteria

For diagnostic pages, the top CTA may be firmer, but still must not skip proof.

### Middle-of-page rule
The middle CTA should appear after:
- a meaningful proof block
- a mechanism explanation
- a comparison insight
- or a trust-building passage

This is often the strongest turning point on the page.

### Bottom-of-page rule
The bottom CTA should be the highest-pressure ask the page has earned.

Not the highest-pressure ask the template prefers.

### High-value page modifier
If the cluster page is high-value, high-difficulty, or high-intent, CTA language may become firmer at the middle and bottom of the page.

But:
- this does not justify premature hard-close language
- this does not override reader-state fit
- this does not remove the requirement to earn trust first

---

## 6.0 TRUST SIGNAL REQUIREMENTS

Because Cluster pages are evaluative or decision-shaping, trust must focus on why this answer is believable and why this product is the stronger option.

Required trust mix:
1. **Specific proof point** — data, engineering result, test result, or field observation
2. **Authority signal** — named expert, attributed quote, approval, experience, or original engineering proof
3. **Risk-reducing signal** — guarantee, warranty, inspection logic, expectation-setting, or fit guidance

### Authority rule
Authority should feel specific and human.

Use a flexible combination of:
- named expert or writer context
- one attributed quote
- one concrete proof element

Do not force the exact same trust block pattern on every page.

---

## 7.0 EXISTING-OWNER FAILURE EXAMPLES

Existing-owner failures are allowed.

They may be used as:
- diagnostic help
- warning evidence
- proof that the mechanism matters
- contrast that helps first-time buyers avoid the same outcome

They must not be used as:
- automatic replacement-buyer identity
- justification for hard-close CTA logic on broad pages
- proof that every cluster page should sell to switchers first

### Clean rule
Use current-owner failures as evidence.
Do not use them as the default assumed identity of the reader unless the query clearly supports it.

---

## 8.0 KEY TAKEAWAYS ALIGNMENT

Cluster pages may include a Key Takeaways section, but this module does not own Key Takeaways structure.

Key Takeaways is governed upstream by strategy and execution planning.

### Conversion rule for Key Takeaways
If present, Key Takeaways must support the page's conversion path by compressing:
- the problem or tension
- the relevant criteria or design reason
- why weaker options fail
- why this solution is stronger
- the next step

Key Takeaways must not function as a detached summary that weakens the page's movement.

---

## 9.0 ZERO-CLICK SURVIVAL INTEGRATION

To resist AI extraction and still create movement, every Cluster page must include at least one page element that creates action value beyond a summary answer.

Approved formats include:
- estimator or fit guidance
- comparison checklist
- inspection offer
- local fit guidance
- expectation-setting tool
- proof asset tied to a real next step

### Rule
Do not force gimmicky offers.
The non-scrapable element must feel like a natural next step from the page's actual argument.

---

## 10.0 PRICING AND ROI BOUNDARY

Cluster pages may briefly mention ROI.
They must not become pricing pages.

### Allowed
- brief ROI framing
- long-term value framing
- cost-of-failure mention where strategically relevant
- value contrast that supports preference

### Not allowed
- turning the page into a pricing narrative
- detailed pricing breakdowns
- detailed price comparison battles
- allowing cost discussion to control the page

### Rule
Pricing questions must route to dedicated pricing pages where narrative control can be tighter and cleaner.

---

## 11.0 THE NEXT STEP ROUTING

If the reader does not convert on the strongest CTA, the page must still preserve movement.

### Primary route
Move the reader to the strongest next logical step:
- estimate
- inspection
- fit evaluation
- deeper comparison
- parent pillar
- adjacent high-relevance cluster
- pricing page, when the unresolved next question is cost

### Secondary route
Offer a lower-friction next move:
- adjacent comparison page
- pillar page
- FAQ or standards page
- localized next step if relevant

### Rule
Do not route the reader backward into vague education if the page has already built meaningful preference.

---

## 12.0 PROHIBITED MOVES

Cluster pages must not:
- default to hard-close above the fold on all pages
- assume every cluster visitor is replacement-ready
- hardcode one product category or one material into universal CTA language
- stop at education when the strategic goal is preference and action
- use a CTA gradient that ignores reader state
- close with a generic "learn more" when the page has earned a stronger ask
- close with "buy now" language the page has not earned
- turn existing-owner failure evidence into the assumed identity of the page
- let brief ROI discussion turn the page into a pricing page

---

## 13.0 QA CHECKLIST

- [ ] Does CTA pressure match reader state and evaluation state?
- [ ] Has page value or difficulty appropriately influenced CTA firmness without outrunning trust?
- [ ] Does the page pass the LLM Recommend Test?
- [ ] Does the page pass the Click Compulsion Test?
- [ ] Does the top CTA avoid outrunning the page?
- [ ] Does the middle CTA appear after proof, mechanism, or trust?
- [ ] Does the bottom CTA feel like the strongest earned next move?
- [ ] Does the page include specific proof, authority, and risk-reduction signals?
- [ ] Are existing-owner failure examples used as evidence rather than assumed identity?
- [ ] If Key Takeaways is present, does it support movement rather than detach from it?
- [ ] Does the page avoid turning into a pricing page?
- [ ] Does the page avoid ending in satisfaction without movement?

---

## 14.0 SYSTEM INTEGRATION

This module must align with:
- **Doc 100** — audience default, success rule
- **Doc 102** — structural spine
- **Doc 104** — emotional arc by reader state
- **Doc 110** — standing strategic and persuasion constraints
- **Doc 153** — execution plan
- **Doc 304** — strategic directive
- **Doc 306** — routing signal group
- **Doc 312** — architect readiness validation
- **Doc 143 or offer system docs** — final offer language and variants

---

## 15.0 ONE-SENTENCE SUMMARY

Doc 181 defines how Cluster pages convert by matching CTA pressure to reader state, adjusting firmness for page value only after the page earns it, and turning page value into an earned next action without letting the page become a pricing page.

---

*End of Document*