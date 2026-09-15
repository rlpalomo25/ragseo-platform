# Doc 209: The System Operating Loop

**Version:** 1.0 | **Last Updated:** July 18, 2026 | **Series:** 200 (Workflow & Governance)
**Purpose:** the top-level doc that turns a library of rules into a running system. Every other doc is a rule; this is the heartbeat that makes the rules move. If you read one doc to understand how RAGSEO stays alive instead of frozen at a point in time, read this.

---

## 0. Source of truth (read first)

**Canon lives in exactly ONE place: the OneDrive `Brain Trust` folder.** FileZilla / FTP is a **downstream mirror**, kept current automatically by a one-way sync (OneDrive → FTP). 

- Edit canon **only** in OneDrive. Never edit on FTP — those edits are overwritten on the next sync and lost.
- The team **reads** from FTP (real-time newest copy); they never author there.
- This is what ends shadow-drift: one authoritative copy, one generated mirror, no hand-maintained second home.

The GPTs/agents load their knowledge from this same canon. When canon changes, the mirror and the uploaded knowledge files must both refresh (see §4 and Doc 208).

---

## 1. Why a library isn't a system

A document is passive. It does nothing until something reads it. A pile of well-written docs is a library, not an organism — which is why the system has felt like a snapshot: it was one. Four organs turn the library into a living loop. The system has all four *as documents*; until now none were wired to a clock or a shared file.

## 2. The four organs

**1. Clock — the heartbeat.** Scheduled tasks fire on a cadence so agents stop being one-time events a human must remember to trigger.
- Competitive Watch (Doc 311): **weekly, Friday.**
- Frontier Monitoring (Doc 360): **monthly.**

**2. Memory — shared, persistent state.** A known place each agent writes so others can read later. Lives in `company/intel/`:
- `competitive-watch-latest.md` — Doc 311 overwrites weekly.
- `frontier-radar-latest.md` — Doc 360 writes monthly.
- **The Answer Ledger** — every question/keyword we've answered → its home URL → status. The Strategist checks it *before* planning any FAQ, so nothing is written twice (enforces one-home-per-question mechanically). Seed: the KPI workbook's **Keyword Governance** tab + Doc 432 Gold Answers.

**3. Inbox — the nervous system.** `company/intel/system-update-inbox.md`: the single "take action: update all" queue. Monitors and humans add items; **Doc 208 (Change Ripple Protocol)** processes each and checks it off. Nothing changes canon without passing through here.

**4. Senses — the feedback loop.** The vital-few KPIs that tell the system whether the work worked. Only four feed a content decision:
- **Rank / move** (rankings, impressions, CTR)
- **Convert** (conversion, revenue, ROI)
- **AI-cited** (Visby)
- **Competitive share of voice** (from Doc 311)

Everything else in the old 12-engine dashboard (technical SEO, site speed, security, link building, local) is **infrastructure health** — a monthly/quarterly check, never part of the weekly content loop. The 12-engine weekly dashboard is retired precisely because no one could sustain it; the vital four replace it.

## 3. The loop

**produce → publish → sense → feed back → produce better.**
The clock keeps it moving. Memory stops it repeating itself. The inbox propagates change. The senses tell it whether any of it worked. Remove any one organ and it stops being a loop.

## 4. The discipline: auto vs. gate

Calibrated by blast radius — this is where "we've been too lax" gets fixed without recreating a bottleneck:

- **Auto (no human gate):** anything that only *informs* a human who then decides. Example: the weekly competitive report landing in `competitive-watch-latest.md`. It changes nothing on its own.
- **Human gate (nothing takes effect until Karen approves):** anything that *changes canon, publishes, or feeds a number into a decision automatically.* The system-update inbox, any doc edit, any publish. 

Holistic does **not** mean unattended. The clock and memory make the loop self-sustaining; the human stays at the approval gate, where every drift this system ever suffered could have been caught.

## 5. Organ → document map

| Organ / job | Cadence | Document(s) |
|---|---|---|
| Front door / intent gate | on keyword | Router (Doc 306) + the Intent Gate (Doc 153/304 step 1) |
| Per-keyword SERP | on demand | Doc 307 (spec) → Jose's n8n agent (implementation) |
| Competitive watch (write) | weekly | Doc 311 → `competitive-watch-latest.md` |
| Competitive synthesis (read) | on demand | Doc 305 → reads last few reports, hands the Strategist the trend |
| Frontier / freshness | monthly | Doc 360 → writes to the inbox |
| Answer ledger (memory) | continuous | Keyword Governance registry + Doc 432 |
| Propagation | on change | Doc 208 (Change Ripple Protocol) |
| Senses (KPIs) | weekly/monthly | vital-four senses file (rank / convert / cite / SoV) |

## 6. Status — honest (what's live vs. dormant)

- **Live:** the produce path — Intent → 304 → 153 → writers (316/320/324) → 328 → publish.
- **Dormant, to switch on:** the two scheduled monitors (311, 360); the `company/intel/` state files; the update inbox; the answer-ledger wiring; the vital-four senses file; the OneDrive→FTP mirror.

Switching those on is what converts RAGSEO from a snapshot into a system that maintains itself.