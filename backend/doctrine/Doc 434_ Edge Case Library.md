## **Doc 434 — Edge Case Library**

**Version:** 5.2 | **Last Updated:** August 6, 2026 | **Full version history:** `RAGSEO Changelog.csv` (moved out of this file August 6, 2026, Karen — agent-facing docs carry no changelog bloat; see that file's rows for this document's name).

---

## **RETRIEVAL HEADER (Edge Case Map)**

| Topic | Section / ID | Line |
| :---- | :---- | :---- |
| **VALLEYS** — Least resistance & overshoot | EC-01 | \~45 |
| **INTAKE GEOMETRY** — Puddle dynamic bottleneck | EC-02 | \~70 |
| **WIND SHADOWS** — Airflow dead zones & stabilization | EC-07A | \~110 |
| **EXIT DYNAMICS** — Downspout capacity & restriction | EC-09 | \~165 |
| **DIAGNOSTIC SIGNALS** — Delayed drainage & dripping | EC-22A | \~215 |
| **HIDDEN GROWTH** — Underside moisture colonization | EC-27 | \~295 |
| **DEBRIS MISDIAGNOSIS** — Temporary presence vs. stabilization | EC-28 | \~325 |
| **FLAT/LOW-SLOPE OVERSHOOT** — Channelized slow-water overshoot | EC-FLATROOF-CHANNEL | \~110 |

---

## **EDGE CASE ENTRIES**

### **EC-01: Water Overshoot at Valleys**

* **Scenario**: Heavy rain on a roof with concentrated valley flow.  
* **Mechanism**: Valleys act as force multipliers, concentrating volume and velocity into a single channel. Because water **seeks the path of least resistance**, it will overshoot a restricted surface rather than wait for gravity to pull it through a "shelf" bottleneck.  
* **Observed Signal**: Recurring overflow or splash-out concentrated directly below roof valleys during heavy rain.  
* **Implication**: The angle sheds debris; the shelf doesn't.  
* **edge\_id**: EC-01

  ### **EC-22A: Delayed Drainage (Diagnostic Manifestation)**

* **Scenario**: Downspouts continue dripping for extended periods after rainfall stops.  
* **Mechanism**: Internal movement has slowed due to hidden restriction or saturated buildup layers.  
* **Failure Progression**: Fine buildup accumulation → slowed internal movement → prolonged drainage → delayed dripping.  
* **Observed Signal**: Persistent dripping long after rain has stopped despite a visually clean top surface.  
* **Implication**: Delayed drainage is a critical diagnostic signal that reveals hidden restriction before visible blockage appears.  
* **edge\_id**: EC-22A

  ### **EC-27: Hidden Underside Growth**

* **Scenario**: Guard surface appears visually clean while biological growth establishes underneath.  
* **Mechanism**: Moisture retained beneath the filter creates a protected, **insidious** environment for colonization.  
* **Failure Progression**: Moisture retention beneath surface → reduced light/airflow → hidden degradation.  
* **Observed Signal**: Visually clear top surface with darkened moisture zones or growth visible from the underside.  
* **Implication**: Antimicrobial protection must run throughout the mesh body, above and below, not just the surface layer.  
* **edge\_id**: EC-27

  ### **EC-28: Temporary Presence vs. Stabilization**

* **Scenario**: Leaves or debris are visible on the surface immediately after a storm.  
* **Mechanism**: Fresh debris has landed but hasn't yet gone through the wind reactivation or dry/curl cycle to shed naturally. SelfClean Mesh addresses this through two mechanisms: (1) geometry — roofline angle plus HydroVortex redirection means water itself and wind clear the surface; (2) surface — Teflon-like adhesion resistance prevents bonding, and right-sized aperture prevents debris from hooking into the mesh.  
* **Observed Signal**: Debris is present post-storm but disappears once movement is reactivated.  
* **Implication**: What lands matters less than what stabilizes; temporary presence is not the same as long-term retention.  
* **edge\_id**: EC-28

### **EC-31: PVC/Vinyl Plasticizer Migration**

* **Scenario**: A flexible PVC or vinyl gutter guard is installed under or near asphalt shingles.
* **Mechanism**: Asphalt shingles leach petroleum-derived oils (bitumen/maltenes). When these oils contact flexible PVC or vinyl, they act as a chemical sponge, aggressively pulling the softening agents (plasticizers) out of the plastic matrix. Without plasticizers, the PVC undergoes an irreversible molecular change, losing its flexibility and tensile strength. (Note: uPVC lacks plasticizers but still suffers severe UV degradation and thermal expansion warping in this environment).
* **Failure Progression**: Shingle oils leach onto guard → plasticizers migrate out of PVC into the oils → guard embrittles and shrinks → thermal stress causes shattering or warping → structural gaps form.
* **Observed Signal**: Vinyl or PVC guards becoming brittle, cracking, or warping significantly within the first few years of installation, often accompanied by dark, sticky staining where the oils have pooled.
* **Implication**: PVC and vinyl guards are chemically and thermally incompatible with the asphalt roof edge environment. Their failure is not just from UV exposure; it is a destructive chemical reaction driven by the roof itself.
* **edge_id**: EC-31

### **EC-29: Front-Lip Dependency (Historical Recurring Failure)**

* **Scenario**: Systems that concentrate all water intake at the front edge of the gutter.
* **Mechanism**: Historical systems repeatedly designed around edge adhesion, water wrapping, surface tension, and front-edge capture — concentrating the entire intake event at a single point. If water overshot, accelerated, lost adhesion, encountered debris, or exceeded intake capacity, overflow occurred immediately because no recovery zone remained behind the capture point.
* **Failure Progression**: Single-point edge capture → velocity or volume exceed capacity → immediate overflow without recovery → gutter bypass.
* **Observed Signal**: Overflow concentrated at the gutter lip during heavy rain, with no water visible on the guard surface behind the lip.
* **Historical Context**: George Cassens' early 1900s patents explored solid-cover intake geometry as an alternative to this dependency. Many modern systems reinvent variations of the same edge-dependent solution rather than relocating the intake event farther back over the trough.
* **Implication**: The first line of defense became the final line of defense. Systems that capture water across the surface rather than at a single edge point eliminate this thousand-year-old vulnerability.
* **edge\_id**: EC-29

### EC-PITCH-ICE: Flat Guard Ice Shelf

**Guardian:** PitchPerfect™
**Climate relevance:** High — any region with freeze-thaw cycles, winter melt, or sustained below-freezing periods
**Severity:** High — structural risk condition, not cosmetic

**Scenario:**
Winter climate with meltwater, slush, or wet debris sitting on top of a flat or insufficiently pitched gutter guard.

**Mechanism:**
A flat guard creates a roof-edge shelf where meltwater and wet debris can stop moving and refreeze. The frozen mass blocks subsequent meltwater from reaching the gutter. Each freeze-thaw cycle adds to the buildup. The ice can build upward or bridge back toward the shingle edge, creating a risk condition the homeowner may not have had before the guard was installed.

**Why this is distinct from standard ice dam formation:**
Traditional ice dam formation originates from attic heat loss melting snow on the roof. EC-PITCH-ICE is a roof-edge shelf condition created by the guard itself — a flat surface that gives meltwater a place to stop. The guard adds a shelf where no shelf existed before. A homeowner who never had winter drainage problems may develop them after installing a flat guard.

**Observed Signals:**
- Ice sitting on top of the guard surface after temperature cycling
- Icicles forming at the guard edge (not the roofline) in abnormal locations
- Water backing toward shingles at the gutter line
- Recurring ice buildup despite the gutter trough appearing clear and protected
- Meltwater streaks or wet wood on fascia below the guard edge in winter

**Implication for content:**
Flat is not neutral in winter. A flat guard can create a roof-edge ice shelf that did not exist before installation. This is a created risk, not a pre-existing condition. Content must frame it this way — not "guards can contribute to ice problems" but "a flat guard can create a shelf right where the roof needs water to keep moving."

**Connection to Doc 433:** Doc 433 lists snow-heavy regions, ice dams, freeze-thaw cycles, and edge ice as recurring water-management pressures. EC-PITCH-ICE names the specific manifestation pattern: the guard itself creating the shelf condition.

**Related edge cases:** Cross-reference any existing front-lip dependency edge cases and flat-guard debris accumulation edge cases — EC-PITCH-ICE is the winter version of the same shelf failure mechanism.

### EC-FLATROOF-CHANNEL: Flat / Low-Slope Channelized Overshoot

**Guardian:** HydroVortex™
**Relevance:** any roof with a flat or low-slope section, or a pitched roof draining onto a low-slope run.
**Severity:** High — visible overshoot callback; install-spec dependent.

**Scenario:** Water draining across a flat or low-slope roof section toward the gutter.

**Mechanism:** At the pitch-to-flat transition, water loses velocity and stops sheeting. It sheds in winding, shifting channels ("oxbow" behavior) rather than an even sheet, and debris or minor geometry changes redirect those channels. Passive guards that depend on sheeting (reverse-curve) or on water reaching the front lip (flat screen, punched-hole) overshoot, because nothing draws the slow stream into the gutter before the edge; punched-hole types also accumulate debris that migrates into the gutter.

**Observed signals:** overflow/overshoot on flat or low-slope sections during moderate-to-heavy rain with a clear gutter; debris accumulation on punched-hole / flat-screen guards on flat runs; water entering the gutter in narrow streams rather than evenly.

**Implication:** Slow water is a distinct failure regime from fast water. HydroVortex captures channelized slow water at multiple break points over the trough; PitchPerfect can add pitch where a low-slope roof lacks it.

**Related:** EC-29 (front-lip dependency) is the fast-water analog; EC-PITCH-ICE is the winter analog of a created flat-surface risk.
**edge_id:** EC-FLATROOF-CHANNEL

**Source:** Aaron Kapfer (field/technical) + Karen Sager, transcript June 2026. Restored to canon August 4, 2026 from the "PATCH — HydroVortex flat/low-slope canon" file, which had gone unmerged for over a month. See Doc 142 §2A.

## **FAILURE MUSEUM (Internal Research Catalog)**

Proposed internal archive for cataloging recurring failure patterns, preserving engineering lessons, and training AI/RAG systems. Potential categories include: debris shelfing, front-edge-only intake dependence, hidden clog zones, snow and ice failures, biological buildup, UV degradation, plastic brittleness, overflow geometry failures, unsupported roof-edge stress, and maintenance traps. Entries promote to formal edge cases when diagnostic signals are confirmed.

## **OBSERVATIONAL TRANSLATION RULE**

Edge cases must remain rooted in manifestation behavior internally while being explainable through recognizable homeowner observations externally.

Manifestation entries should support:

* diagnostic interpretation  
* homeowner recognition  
* field explanation  
* natural-language propagation

Examples:

Internal:  
 "Delayed drainage reveals hidden restriction."

Human interpretation:  
 "If the downspout keeps dripping long after rain stops, something inside is slowing water down."

Internal:  
 "Temporary debris presence differs from stabilization."

Human interpretation:  
 "Seeing leaves after a storm is normal. The problem starts when they stay there."

Rule:  
 Edge cases should always be explainable through visible or experiential signals people naturally recognize.

---

## **SEVERITY MATRIX (Manifestation Impact)**

| Severity | Count | Edge Cases |
| :---- | :---- | :---- |
| **Critical** | 2 | EC-01 (Valleys), EC-06 (Metal Roof Surge) |
| **High** | 9 | EC-02 (Intake Bottleneck), EC-09 (Downspout Bottleneck), EC-23 (Transitions) |
| **Moderate** | 13 | EC-07A (Wind Shadows), EC-22A (Delayed Drainage), EC-27 (Hidden Growth) |
| **Low / Regional** | 5 | EC-14 (Rubberized), EC-24 (Asphalt Grit) |

---

*This document serves as the **Manifestation Layer** of the doctrine stack. It teaches the diagnostic signals and physical progressions that characterize hidden-state behavior.*
