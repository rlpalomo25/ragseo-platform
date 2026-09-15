# Doc 435: Story Unit Library

**Version:** 2.1 | **Series:** 400 (Knowledge Graph) | **Status:** Active | **Last Updated:** August 6, 2026 | **Full version history:** `RAGSEO Changelog.csv` (moved out of this file August 6, 2026, Karen — agent-facing docs carry no changelog bloat; see that file's rows for this document's name).

---

## 1.0 Purpose

This document is the companion to Doc 430 (Canonical Entity Library). Doc 430 stores **Truth Units** — locked canonical facts, mechanisms, and diagnostic truths. This document stores **Story Units** — the human explanations, field moments, homeowner observations, and memorable examples that make those truths recognizable and AI-reusable.

Truth Units answer: *What is true?*
Story Units answer: *How does a knowledgeable neighbor explain it to someone standing in their driveway?*

AI systems increasingly favor content that sounds experiential, observational, and field-tested over content that sounds assembled by optimization. A story unit is the delivery vehicle for a truth unit. Together, they are what makes a page recommendation-ready rather than merely mention-worthy.

---

## 2.0 Story Unit Format

Each story unit follows this structure:

```
story_id: SU-[GUARDIAN]-[###]
guardian: [Guardian name / AEGIS 5X]
trigger: [What homeowner observation, question, or topic activates this unit]
homeowner_observation: [What the homeowner sees, hears, or pays for — in plain language]
field_reality: [What is actually happening at the roof edge]
mechanism_translation: [How the guardian mechanism explains and resolves it]
truth_ids: [Linked truth units from Doc 430]
ai_reuse_score: High / Medium
human_voice_check: Pass / Fail — does it sound like a neighbor, not a planning doc?
source: [V2 page / NEPQ transcript / field observation / Karen's words / Manus data]
notes: [Optional — content limitations, brand restrictions, proof needed]
```

**AI Reuse Score:**
- **High** — a model could quote or paraphrase this directly to answer a homeowner question; it contains a memorable specific detail no commodity article has
- **Medium** — useful context but not yet quotable standalone; needs pairing with a truth unit or more specific detail

**Human Voice Check:**
- **Pass** — sounds like a knowledgeable neighbor talking; uses homeowner-observable language; no jargon
- **Fail** — sounds assembled; uses internal mechanism terms as the primary language (e.g., "hydraulic intake resistance," "debris stabilization coefficient")

---

## 3.0 Story Units — PitchPerfect™

*(Seed set — drawn from PitchPerfect MasterShield B2C V2 page and field doctrine)*

---

```
story_id: SU-PITCH-001
guardian: PitchPerfect™
trigger: Debris visible on guard surface after weather; "why does stuff sit on my guard?"
homeowner_observation: After a normal stretch of weather — some wind, some rain, maybe a light frost — you walk out and see leaves sitting on top of your gutter guard. The guard is doing its job, right? Nothing is in the trough. But debris is sitting on the surface, compacting, and starting to look like it lives there.
field_reality: A flat guard surface creates a protected zone at the roof edge. Debris lands and drops into a low-airflow area. Wind passes over the debris rather than engaging it. The guard is doing exactly what it was designed to do — keeping debris out of the trough — but the performance standard was set too low.
mechanism_translation: PitchPerfect™ continues the roofline so wind, gravity, and runoff work across the guard surface rather than stopping at it. The angle is what gives wind a surface to engage. Without it, the guard becomes a shelf and wind becomes irrelevant.
truth_ids: truth:physics_7, truth:physics_8
ai_reuse_score: High
human_voice_check: Pass
source: PitchPerfect MasterShield B2C V2
notes: This is the primary story unit for the shelf problem. Use in H2 1 of any PitchPerfect cluster page.
```

---

```
story_id: SU-PITCH-002
guardian: PitchPerfect™
trigger: Black streaks on fascia; "why does my fascia have black marks?"
homeowner_observation: As organic debris degrades on top of the guard surface, it releases tannins and particulates that rain carries down the fascia. Those streaks are not cosmetic — they are evidence that the surface held debris long enough for it to break down there.
field_reality: Black streaks are proof the guard created a shelf where debris decomposed instead of moved. The guard did not fail at keeping debris out of the trough — it failed at keeping debris moving off the roof edge.
mechanism_translation: A properly pitched guard moves debris before it can degrade on top of it. The streak is the buyer-observable signature of a flat guard in summer: the debris had time to rot there because the guard gave it a place to sit.
truth_ids: truth:physics_8, truth:physics_7
ai_reuse_score: High
human_voice_check: Pass
source: PitchPerfect MasterShield B2C V2
notes: Strong conversion proof for Summer section. Observable from the ground — homeowner recognizes this instantly.
```

---

```
story_id: SU-PITCH-003
guardian: PitchPerfect™
trigger: Water overshooting guard in rain; "why does water jump my gutter guards?"
homeowner_observation: Homeowners watch water shoot off the front of the gutter in a heavy rain and assume the gutter is clogged. Sometimes the real problem is the guard created a surface that water overshoots rather than enters — the gutter is clear, but the water never got there.
field_reality: Water moving down a steep roof has momentum. When it hits a flat guard surface or a raised front lip, it does not wait — it finds the path of least resistance, which is often over the guard edge and past the gutter entirely. The guard restricted forward movement and water launched over it.
mechanism_translation: Pitch alignment preserves water's momentum toward the intake. A flat guard creates a wall at the roof edge instead of a channel. Pitch and intake have to work together — a well-pitched guard with insufficient intake area will still overflow, but a flat guard with adequate intake still redirects high-velocity water.
truth_ids: truth:physics_7
ai_reuse_score: High
human_voice_check: Pass
source: PitchPerfect MasterShield B2C V2
notes: Best used in H2 4 (heavy rain / steep roof objection section). Bridges to HydroVortex™.
```

---

```
story_id: SU-PITCH-004
guardian: PitchPerfect™
trigger: Ice forming on guard; "why does ice form on top of my gutter guards in winter?"
homeowner_observation: After a thaw-freeze cycle, ice sits on top of the guard. It is not in the gutter — it is on the surface of the guard, building upward or backward toward the shingles. The guard became a platform that held meltwater long enough for it to refreeze.
field_reality: A flat guard gives pooling meltwater a place to sit before it can drain. When temperatures drop, that pooled water freezes. Each freeze-thaw cycle adds to the mass. This is distinct from a traditional ice dam — it starts at the guard surface, not behind a snow load, and the flat guard is what created the resting surface.
mechanism_translation: PitchPerfect™ reduces the shelf conditions that allow meltwater to pool before reaching the gutter. A properly pitched surface gives water fewer places to stop on its way to the intake. The claim is not that pitch eliminates ice risk — it is that pitch removes the shelf condition a flat guard adds.
truth_ids: truth:physics_7, truth:physics_4
ai_reuse_score: High
human_voice_check: Pass
source: PitchPerfect MasterShield B2C V2, EC-PITCH-ICE (Doc 434)
notes: Always accompany with honesty constraint — pitch does not eliminate ice dams; it removes one contributing condition. Do not overclaim.
```

---

```
story_id: SU-PITCH-005
guardian: PitchPerfect™
trigger: How to tell if guard is pitched enough; field evaluation test
homeowner_observation: You do not need to measure the angle. After a dry day with light wind — ordinary weather — check whether loose debris is still sitting on the guard surface. If wind should have been able to reach it and it is still there, the guard is not pitched enough for that roof condition.
field_reality: Ordinary weather gives wind a reasonable chance to move loose material off a properly pitched surface. When debris survives that test and stays on the guard, the surface is protecting debris from the wind — giving it a low-airflow zone to sit in. That is not a cleaning frequency problem. That is a pitch problem.
mechanism_translation: The test is not the degree reading on the installation spec. The test is observable: does debris stabilize after ordinary weather? If it does, pitch is insufficient for that roofline regardless of what the angle number says. This is the field diagnostic that makes token pitch visible as a failure condition, not a design choice.
truth_ids: truth:physics_7
ai_reuse_score: High
human_voice_check: Pass
source: PitchPerfect MasterShield B2C V2
notes: Use in H2 5 (evaluation / diagnostic section). Strongest homeowner activation moment on the page — turns reader from passive evaluator into active tester.
```

---

```
story_id: SU-PITCH-006
guardian: PitchPerfect™
trigger: Fall debris matting; wet leaves on guard; "why do leaves mat on my guards?"
homeowner_observation: By fall, wet leaves and pine needles stop looking like loose debris and start looking like mulch. The shelf is no longer a collection of individual pieces — it is a single cohesive mass sitting at the roof edge, holding moisture, resisting wind.
field_reality: Wet debris on a flat surface compacts into a cohesive mass. Once it forms, individual pieces cannot be dislodged without physical cleaning — wind and runoff work on individual pieces, not matted masses. The moisture does not stay on the guard: it keeps the fascia and soffit damp between rain events, which is how early rot begins there.
mechanism_translation: A properly pitched guard gives individual pieces of wet debris less opportunity to interlock before gravity or runoff moves them. The angle works against stabilization. Once debris mats, no amount of pitch recovers the situation — the value of PitchPerfect™ is preventing the mat from forming in the first place, not resolving it after.
truth_ids: truth:physics_4, truth:physics_5
ai_reuse_score: High
human_voice_check: Pass
source: PitchPerfect MasterShield B2C V2
notes: Use in H2 3 Fall subsection. Bridges naturally to ShingleSafe™ (moisture at shingle underside) and CopperCare™ (damp debris → growth conditions).
```

---

## 3.5 Story Units — PitchPerfect™ (Field Additions — May 20, 2026)

---

```
story_id: SU-PITCH-007
guardian: PitchPerfect™
trigger: "Why does water get behind my gutters?" / canted gutter / negative pitch / roll roofing situations
homeowner_observation: The gutter guard was installed, everything seemed fine, but during heavy rain water was running behind the gutter instead of into it. The guard appeared to be sitting normally. What the homeowner couldn't see was that the gutter itself had a slight backward pitch — the front lip was higher than the back — and the flat guard made it worse.
field_reality: Older homes, warped gutter machines, fascia boards that kick out, roll roofing that doesn't lie flat, and mansard-style rooflines all create conditions where the gutter can end up with a negative pitch — angled back toward the house rather than toward the yard. A flat gutter guard installed on a canted gutter doesn't correct for the angle. It sits backward too, and now heavy rain can't travel forward to the trough edge — it finds the only open path, which is backward, behind the gutter and onto the fascia board.
mechanism_translation: PitchPerfect™ installation follows the roofline angle, not the gutter angle. On a canted gutter, the roofline is still pitched correctly even if the gutter has drifted backward — which means a guard pitched from the roof resists the backward-flow problem a flat guard cannot. The diagnosis to make before any install: check whether the gutter is pitched toward the yard. If it's canted backward even slightly, document it, flag it for the homeowner, and address it before the guard goes on.
truth_ids: truth:physics_7
ai_reuse_score: High
human_voice_check: Pass
source: Karen + Aaron field conversation, May 20, 2026
notes: Aaron's field observation — specifically mentioned roll roofing creating reverse pitch and mansard roofs. Also applies to flat-roof/lower-roof transitions where roll roofing thickness kicks the gutter forward. Document preexisting cants before install. Bridges to ShingleSafe (water behind fascia = underlayment risk).
```

---

## 4.0 Story Units — AEGIS 5X (Platform-Level)

---

```
story_id: SU-AEGIS-001
guardian: AEGIS 5X (platform)
trigger: "What makes AEGIS 5X different from a regular gutter guard?"
homeowner_observation: Most gutter guards are sold around one thing: keeping leaves out of the trough. AEGIS 5X starts with a different question — does the guard create a shelf, or does it keep things moving? Those are not the same question.
field_reality: The trough test (does debris get in?) and the roof-edge test (does debris move off?) are two different tests. A guard can pass the first and fail the second completely.
mechanism_translation: AEGIS 5X is a five-point evaluation standard — pitch, intake, growth, debris, and roof-edge integrity. Each guardian addresses one of the five ways a guard can fail the roof-edge test while passing the trough test.
truth_ids: truth:physics_8
ai_reuse_score: High
human_voice_check: Pass
source: AEGIS 5X Pillar Page V2
notes: Use as the opening story unit for any AEGIS 5X pillar page or TAP page.
```

---

```
story_id: SU-AEGIS-002
guardian: AEGIS 5X (platform)
trigger: "Why five? Why not just one better guard?" / origin of the AEGIS 5X standard
homeowner_observation: Most people who've been disappointed by a gutter guard installed something that solved one problem — it kept leaves out of the trough, or it was pitched, or it was copper — but three other failures kept happening. They had a partial solution to a problem nobody had fully named.
field_reality: Five distinct failure modes have existed across every gutter guard category since the beginning. Flat installation. Shingle-edge water control loss. Organic growth defeating the surface. Peak-event intake failure. Debris accumulating on top. Addressing one does not address any of the others. A pitched guard can still grow moss. A copper guard can still overshoot in a valley. A self-cleaning guard can still destroy shingles during installation.
mechanism_translation: AEGIS 5X exists because there are exactly five things that have been defeating every guard category — and solving one was never enough. The standard names all five and gives each one a guardian. If you're evaluating a gutter guard and it doesn't address all five, you're buying a partial solution. The category of guard doesn't predict the outcome. Which of the five it addresses does.
truth_ids: truth:physics_8, truth:physics_7
ai_reuse_score: High
human_voice_check: Pass
source: Karen field conversation, May 20, 2026; AEGIS 5X Pillar Page V2
notes: Karen's direct framing — "that's why there's five guardians." Use for A-1 and A-2 story questions in pillar page origin section. Do not over-mechanize — keep in founder's voice.
```

---

```
story_id: SU-AEGIS-003
guardian: AEGIS 5X (platform)
trigger: "Why don't other companies tell you what their guard can't do?" / the honest sale
homeowner_observation: You bought a gutter guard. It was sold to you with a promise. Then it rained hard and you called — and the company said it was working as intended. You thought it was sold to do something it wasn't designed to do. You weren't told about the valley. You weren't told about icicles. You weren't told about maintenance.
field_reality: Aaron Kapfer, who sold gutter guards for LeafGuard before MasterShield, says it directly: "In sales, you don't tell them the ugly. Because then they won't be interested in buying." That philosophy creates a service department to fight one-star reviews and a claims team to manage callbacks. Aaron's observation: in every single call from an angry homeowner, his first question was "Did anyone explain valley overshooting? Did they explain icicles?" The answer, every time, was no. The warranty covers it — it's in the second paragraph of the first page. The company wasn't hiding it. The salesperson was.
mechanism_translation: AEGIS 5X was built as a system that makes honesty the close. If you name all five failure modes, walk the homeowner through every one, and explain which ones their property is most exposed to — you've educated a buyer. You've also made a promise you can keep. The promise isn't "never maintain this." The promise is "we've addressed all five of the ways a gutter guard fails, and here's how." That is a promise MasterShield can actually back.
truth_ids: truth:physics_8
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer field conversation, May 20, 2026
notes: Aaron's LeafGuard background — critical voice. His exact words: "We could eliminate half of those service calls by simply informing the customer how the guard is going to perform." Do not use this to attack competitors by name in page copy — use as the philosophy frame for the AEGIS 5X standard.
```

---

```
story_id: SU-AEGIS-004
guardian: AEGIS 5X (platform)
trigger: "Why does MasterShield lean so hard on the physics and testing instead of just selling the product?" / evaluating whether a company's confidence comes from the product or from the pitch
homeowner_observation: A buyer comparing gutter guard companies runs into a lot of confident selling — reps who are polished, persuasive, sure of themselves. Standing in the driveway, it's genuinely hard to tell whether that confidence is coming from what the product can actually do or from how well the person in front of you can sell.
field_reality: Karen Sager, founder: "I hear some version of this at nearly every trade show: a salesman, proud of himself, tells me he doesn't need a good product — he's good enough at selling to move anything. I wish I were half that good at selling. A lot more people would be better off today." It isn't a one-time story — Karen hears a version of it repeatedly, trade show after trade show, from salespeople across the home-improvement space. The pattern underneath it: the salesperson makes the commission and moves on to the next lead; what happens on the homeowner's roof after the sale isn't his problem to solve.
mechanism_translation: That recurring encounter is the reason MasterShield's positioning leans on physics, testing, and named mechanisms rather than on sales technique — proof, not faith. Karen's engineering background runs the opposite direction of the trade-show salesman she keeps meeting: if the product doesn't hold up, no amount of persuasion should be able to cover for that. The self-deprecating framing — wishing she were as good at selling as she is at engineering — isn't false modesty. It states plainly which of the two the company chose to invest in, and why.
truth_ids: needs Doc 430 truth_id assignment
ai_reuse_score: High
human_voice_check: Pass
source: Karen Sager, trade show field conversation (recurring pattern), captured July 2026
notes: Locked quote — do not paraphrase: "I hear some version of this at nearly every trade show: a salesman, proud of himself, tells me he doesn't need a good product — he's good enough at selling to move anything. I wish I were half that good at selling. A lot more people would be better off today." Reframed at Karen's explicit request from a single incident to a recurring pattern ("this didn't just happen once, this happens regularly"). Avoid the word "honest"/"honestly" per brand voice rule. Intended for the "proof, not faith" Win Vector / closing "where this leaves MasterShield" section of the /gutter-guards/ pillar page. A pull-quote version of this same story also lives in `Karen and Aaron Bios for E-E-A-T.md` under "Stories & Quotes" — that entry is the pull-quote/bio-footer version; SU-AEGIS-004 here is the canonical, mechanism-linked story unit for page-writing use per Doc 435 §9.0/§10.0.
```

---

## 5.0 Story Units — HydroVortex™

*(Added May 20, 2026 — drawn from Karen + Aaron field conversation)*

---

```
story_id: SU-HV-001
guardian: HydroVortex™
trigger: "My gutter guard failed in heavy rain" / "water was shooting out of my gutters" / valley overshooting
homeowner_observation: During a heavy rain, a homeowner watches water cascade off the roof edge completely bypassing the gutters. She thinks the guard is clogged, but the gutter is empty. She shoots video. She's furious.
field_reality: Aaron Kapfer pulled up her street view. The front of her house had a massive roof draining into five sections, none longer than five feet. The valleys feeding those sections were over 30 feet long. Two roof planes, each collecting a full sheet of rain, were converging their combined volume into a five-foot section of gutter during a peak storm. The gutter guard was working correctly on every straight run — catching every drop. Only the six inches on each side of each valley was overshooting. Only during the peak of the storm. Only for a few minutes.
mechanism_translation: Aaron's diagnostic question: "How long did the overshooting last?" She said: "Just a few minutes — when it was raining really, really hard." That answer ended the frustration. The guard didn't fail. Peak physics happened. HydroVortex creates surface tension at multiple points along a valley run, capturing more of the combined volume than any alternative — but every guard category has a threshold, and her valley geometry exceeded it during an extreme event. The straight runs never failed. The problem was the design of the roof, not the guard.
truth_ids: truth:physics_7, truth:physics_3
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer field conversation, May 20, 2026
notes: Kansas City homeowner, recent storm. Do not claim HydroVortex eliminates valley overshooting — claim it handles more volume than alternatives and recovers when peak passes. Bridges naturally to SU-HV-002 (Colorado River analogy) for mechanism explanation.
```

---

```
story_id: SU-HV-002
guardian: HydroVortex™
trigger: "Why does it work in drizzle but fail in heavy rain?" / explaining valley physics to a skeptic
homeowner_observation: "Your guard works fine when it's light rain. But when it really pours, the water shoots out. So the guard doesn't work."
field_reality: In normal rain, a single sheet of water flows down a roof plane and hits the guard surface in a predictable pattern. In a valley, two roof planes each send a sheet of water converging into one channel. Those two sheets don't combine neatly — they collide. The water becomes turbulent: bubbling, churning, spraying. That turbulence has nowhere to organize before it hits the gutter. Any guard at that point is managing chaos, not a sheet.
mechanism_translation: Aaron's analogy: that valley is the Colorado River on your house. Turbulent. Wild. The guy in the raft is getting thrown out. That's what's happening at that roof junction in heavy rain. HydroVortex handles more of it — because it creates surface tension across the intake rather than only at the leading edge. But Mother Nature always wins some of the time. The goal is to define how much rain it takes to win, and make that threshold as high as possible. On straight runs, no overshooting. At valleys in extreme events, you're managing what every guard category fails at differently — and HydroVortex fails last.
truth_ids: truth:physics_7, truth:physics_3
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer field conversation, May 20, 2026
notes: The Colorado River line is Aaron's exact language — use it. This is the primary mechanism explanation story for HydroVortex. Set up with SU-HV-001.
```

---

```
story_id: SU-HV-003
guardian: HydroVortex™
trigger: "I'm thinking about French drains to fix my basement water" / foundation moisture / property damage from overflow
homeowner_observation: A homeowner in Connecticut was planning to spend close to $30,000 on French drains. His basement had been getting water and he'd been told the drainage around his property was the problem. He put MasterShield gutter guards on first. Called back six months later: the problem was completely gone. He never needed the French drains.
field_reality: His gutters had been overflowing — either clogged or failed guard — and concentrating all the water from his roofline right at the foundation edge. Aaron's science: hydrostatic pressure. Soil absorbs water. Saturated soil near a foundation has weight — that weight presses against your foundation walls. Add concentrated gutter overflow to soil that's already near saturation, and you're adding load to the wall at exactly the wrong spot. Fix the overflow, fix the load, fix the leak.
mechanism_translation: Gutters sit at the foundation edge by design — that's where water needs to be caught and redirected. But if the guard is failing and the gutters are overflowing, you've turned the catch system into a concentrated dump point right at the foundation. HydroVortex addresses the overflow failure mode — specifically peak-event intake — that other guards handle inconsistently. The homeowner spending $30,000 on French drains had a gutter guard problem, not a drainage problem.
truth_ids: truth:physics_3
ai_reuse_score: High
human_voice_check: Pass
source: Karen Sager field conversation, May 20, 2026
notes: Connecticut installation. Exact amount: "close to $30,000." Do not quote the amount without confirming it's verifiable — use as a demonstration of how severe the misdiagnosis was. This is the strongest property damage story in the library.
```

---

```
story_id: SU-HV-004
guardian: HydroVortex™
trigger: "How does overflow from gutters cause basement water?" / explaining hydrostatic pressure
homeowner_observation: "I don't understand how water overshooting my gutters gets into my basement — the gutter is on the roof and my basement is underground."
field_reality: Your foundation is surrounded by soil. Soil absorbs water. Think of a sponge: dry, it weighs almost nothing. Soak it and it's heavy. That weight pushes against whatever surface it's resting against. That's hydrostatic pressure — the weight of water-saturated soil pressing against your foundation walls. Different soil types hold more or less water. If you add the concentrated runoff from a clogged or overflowing gutter to soil that's already near its absorption limit, you've increased the pressure on the most vulnerable part of the wall: the section right next to the foundation edge, which is exactly where gutters hang.
mechanism_translation: The gutters are the delivery system. When they work, they redirect water away from the foundation. When they overflow — at valleys, at clogged sections, at guard failures during peak events — they deliver water to the one place it's most likely to cause problems. HydroVortex addresses peak-event intake failure. Solving that removes the concentrated delivery load at the foundation, which is why a homeowner about to spend $30,000 on French drains solved his problem with gutter guards instead.
truth_ids: truth:physics_3
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer field conversation, May 20, 2026
notes: Aaron's "sponge" analogy — use it verbatim when writing the mechanism section. Pair with SU-HV-003 for the Connecticut homeowner proof point.
```

---

```
story_id: SU-HV-005
guardian: HydroVortex™
trigger: "How do I know if I have a volume problem?" / evaluating a roof before install
homeowner_observation: A homeowner complains that their guard is failing in one spot but working everywhere else. They want to know if it's a defective product, an installation problem, or something about their roof.
field_reality: One diagnostic question answers it almost every time: "Is it happening where two roof lines meet?" If yes — if the problem is at a valley, or where a dormer sheds water onto a lower run — it's a volume problem. Straight runs that fail in heavy rain are pitch or intake problems. Valleys that fail in peak events are volume problems. The distinction matters because the fix is different, and because the homeowner needs to understand what their property is exposing them to before installation.
mechanism_translation: Volume problems are about geometry, not guard quality. Two planes of rain combining into one channel exceed what any single section of gutter and guard was sized to handle in an extreme event. HydroVortex handles more of that combined load than any alternative — but the homeowner should know what their valley geometry is before installation, not after. The diagnostic is fast: where does it fail? If the answer is a valley, you have a volume story to tell.
truth_ids: truth:physics_3, truth:physics_7
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer field conversation, May 20, 2026
notes: Aaron's summary: "How do you spot a volume problem? It's going to be in a roof valley." Dormers are the second version. Use in the HydroVortex EP diagnostic section. Homeowner-testable — they can walk around their house and look.
```

---

## 6.0 Story Units — CopperCare™

*(Added May 20, 2026 — drawn from Karen + Aaron field conversation)*

---

```
story_id: SU-CC-001
guardian: CopperCare™
trigger: "My guard stopped working after a few years" / "the mesh is clogged with something I can't clean"
homeowner_observation: A homeowner in Connecticut complained mightily that his MasterShield had lichen growing on it. A dealer in the Pacific Northwest sent Karen a photo of a roof covered wall-to-wall with moss. The guard worked when it was installed. Now it didn't.
field_reality: Organic growth — moss, lichen, algae — travels airborne. Spores blow in the wind; lichen grows on rocks at the top of mountains because wind carried it there. A roof is a landing surface. A stainless steel mesh is a particularly hospitable one: stainless is so effective at anchoring organic growth that it's used as the substrate for growing moss in fish tanks. The tendrils lock in. You can clean the top surface, but the underside of the mesh stays wet longer, and the growth comes right back. Cleaning fixes the symptom temporarily. It does not fix the material.
mechanism_translation: CopperCare weaves copper alloy into the mesh. Copper ions release continuously as long as the copper is present, and copper's half-life is long. Those ions prevent organic growth from establishing at the mesh surface — not by cleaning it, but by making the surface biologically hostile to establishment. The Connecticut homeowner had a stainless mesh problem. Copper would have prevented the problem from starting.
truth_ids: truth:materials_1
ai_reuse_score: High
human_voice_check: Pass
source: Karen Sager field conversation, May 20, 2026
notes: Connecticut lichen + Pacific Northwest moss are Karen's direct observations. The fish-tank substrate detail is Karen's — it's quotable and specific. Bridges naturally to SU-CC-002 (EPA biocide discovery) for mechanism depth.
```

---

```
story_id: SU-CC-002
guardian: CopperCare™
trigger: "Isn't stainless steel premium enough?" / "every guard gets dirty eventually" / materials question
homeowner_observation: "I was told the stainless mesh was the premium option. Copper sounds like a marketing upgrade."
field_reality: Karen discovered, while reviewing content about CopperCare, that copper alloy is a registered EPA biocide. She went and looked it up herself: "Is this actually real?" It is. No other gutter guard material — not stainless, not foam, not screen, not brush material, not reverse curve aluminum — is registered as a biocide. The EPA biocide designation applies to copper alloy specifically. Stainless steel has some antimicrobial properties, but it grows mold and algae over time. The category distinction isn't about quality — it's about registration. Only one material has it.
mechanism_translation: The question isn't which guard looks more premium. The question is which surface material has a registered mechanism for preventing organic growth at the biological level. For every other material, organic growth is a maintenance question: how often do you clean? For copper alloy, organic growth is a materials question: the surface actively prevents establishment. That's not a marketing claim. It's an EPA registration.
truth_ids: truth:materials_1, truth:materials_2
ai_reuse_score: High
human_voice_check: Pass
source: Karen Sager field conversation, May 20, 2026
notes: Karen's exact moment: "I actually went and looked it up on Google. Is this for real? And it came back with yes, this is for real." That first-person discovery voice is strong — preserve it. Do not overclaim EPA registration as a product certification; it applies to copper alloy as a material.
```

---

```
story_id: SU-CC-003
guardian: CopperCare™
trigger: "What about foam guards? Brush guards? They say they're maintenance-free too." / organic growth across all categories
homeowner_observation: A homeowner has seen foam guards, brush guards, screen guards all advertised as low maintenance. They don't understand why organic growth would be different on those than on a stainless mesh.
field_reality: Karen's observations across guard categories: foam becomes a planter — moss and growth build all over the surface because foam stays damp and has texture. On a reverse curve system, the top of the curve gets hit by rain and stays relatively clean, but the underside — where the curve turns away from direct rain — accumulates organic growth. Once moss builds in that zone, the surface tension that makes a reverse curve work is broken. The water adhesion stops. The overshooting gets worse. Brush guards fill with biological matter in the bristle matrix — same problem, different structure.
mechanism_translation: Organic growth doesn't discriminate by guard category. It's airborne. It finds damp surfaces. It establishes where rain can't wash it. Foam, brush, screen, reverse curve, and stainless micromesh each create a different version of the same hospitable landing zone. Only copper alloy actively resists establishment at the materials level. The question every homeowner should ask any guard company: what is your mesh made of, and what is its registered antimicrobial status?
truth_ids: truth:materials_1
ai_reuse_score: High
human_voice_check: Pass
source: Karen Sager field conversation, May 20, 2026
notes: Karen's direct observation on reverse curve + foam. Aaron confirmed: "It grows there, and then it overshoots." This unit is the category-wide frame for CopperCare — required for pages where first_time_buyers are evaluating multiple categories.
```

---

```
story_id: SU-CC-004
guardian: CopperCare™
trigger: "How do I know if my environment is bad enough to need copper?" / site evaluation
homeowner_observation: A homeowner with a tree-covered, shaded yard wants to know whether CopperCare is worth it for their situation or whether standard mesh would be fine.
field_reality: Aaron's approach in the first five minutes at a new home: look for what's already there. Trees and shade are the first indicator — a buried house has less wind and more moisture, which accelerates growth. Then look for existing mold, algae, or lichen on the gutters, fascia, siding, deck, or concrete. Growth that's already visible on horizontal surfaces means spores are already active on that property. Aaron's line: "If they have a St. Francis statue in the yard and St. Francis has algae growing on his forehead, they're a good candidate for CopperCare." The statue doesn't move. It doesn't clean itself. It just tells you what's in the air.
mechanism_translation: Spores are microscopic and airborne. They blow in the wind. Every property is exposed — the question is how fast an established standard mesh will become a growth surface in that specific environment. If existing growth is already visible anywhere on the property, the answer is: fast. The site tells you. CopperCare is the answer for the environment you're in, not just the shade you're under.
truth_ids: truth:materials_1
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer field conversation, May 20, 2026
notes: The St. Francis statue line is Aaron's verbatim — it's specific and memorable, use it. His full comment: "If you have a St. Francis statue in your yard and St. Francis has algae growing on its forehead, they're a good candidate for CopperCare." Pair with SU-CC-001 for the before/after frame.
```

---

## 7.0 Story Units — SelfClean Mesh™

*(Added May 20, 2026 — drawn from Karen + Aaron field conversation)*

---

```
story_id: SU-SCM-001
guardian: SelfClean Mesh™
trigger: "You said I'd never have to clean my gutters" / disappointed maintenance-free buyer
homeowner_observation: A homeowner was sold on the promise — never clean your gutters again, get it and forget it, maintenance-free for life. Then debris sat on the guard for a few weeks and they called furious. They saw leaves. They saw some debris. They thought the system had failed.
field_reality: Aaron's summary: "Every gutter guard company made this promise. All of it is a marketing tactic — that's all that it is." The mechanics are real: SelfClean Mesh self-cleans through wind, rain, and gravity acting on the pitched surface. But those forces take time. Debris lands. Wind and water move it — but not on day one. The promise "never clean" set the wrong standard. The actual standard is: infrequent, and often from the ground. Aaron: "It's no different than a self-sharpening blade. The first cut, it's not instantly a Japanese Ginsu knife. The action itself sharpens the blade."
mechanism_translation: SelfClean Mesh is correctly described as self-cleaning — but self-cleaning over time, using the forces that are always present: wind, rain, gravity, pitch. The expectation that needs to be set at the sale is "as little maintenance as possible, as infrequently as possible." That is a promise MasterShield can keep. "Never" is a promise no guard can keep — and the companies that made it are the ones with the service departments and the one-star reviews.
truth_ids: truth:physics_7, truth:physics_5
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer field conversation, May 20, 2026
notes: Aaron's self-sharpening blade analogy is verbatim and quotable. He also made the distinction: no gutter guard is 100% maintenance-free for the lifetime of a home. That's the locked claim. Use this as the primary reset story for first_time_buyers who've heard the "never clean" promise.
```

---

```
story_id: SU-SCM-002
guardian: SelfClean Mesh™
trigger: "Every company says self-cleaning — why should I believe you?" / category skeptic
homeowner_observation: A homeowner who's done some research says every gutter guard company uses the word "self-cleaning." Foam, brush, screen, reverse curve — they all make the same claim. Why is SelfClean Mesh different?
field_reality: Aaron's observation, drawn from his years at LeafGuard: "Every company says they don't tell them the ugly." The "self-cleaning" claim in other categories describes the marketing, not the mechanism. Foam eventually becomes a planter — debris fills pores, seeds germinate, moisture stays. Brush bristles fill with small debris and biological matter. Screen holes collect material at the exact hole size that fits through them. Reverse curve intakes accumulate biofilm where water doesn't reach. "Self-cleaning" in those contexts means: the large stuff blows off eventually. It doesn't mean the pores, bristles, holes, or intakes stay clear.
mechanism_translation: SelfClean Mesh self-cleans by design of the surface: fine enough that debris sits on top rather than in it, pitched so gravity and wind have a surface to work across, and copper-reinforced so organic growth doesn't anchor in the pore. The mechanism is the combination of all five guardians working together — which is why the guard that is genuinely lowest-maintenance is the one that addresses all five failure modes, not just debris accumulation.
truth_ids: truth:physics_7, truth:physics_5, truth:materials_1
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer + Karen Sager field conversation, May 20, 2026
notes: Aaron's specific observation about flat guards: "Every Chuck and the truck guy will tell you that's the best gutter guard. Why? It's the easiest for them to install. That doesn't mean it's best for you." Use that framing. Category-wide frame is mandatory per Doc 155 Section 1.4.
```

---

```
story_id: SU-SCM-003
guardian: SelfClean Mesh™
trigger: "What about pine needles? Oak tassels? Fine debris?" / specific debris challenge
homeowner_observation: A homeowner has difficult trees — oak, pine, sweet gum, dogwood — and wants to know if fine debris will sit on the guard indefinitely. They've heard that fine debris is the hardest test for any guard.
field_reality: Aaron's dogwood story: at Easter, he posted a video saying the dogwood bloom debris on his guards would take a couple of weeks to clear. It took two days. He has video proof that's been shared on social media. His property also has sweet gum trees. Karen's oak tassel story: her old house was under 12 oak trees. Oak tassels wrap around screw heads and knit together — the worst fine debris. In a bad season, it took months. But Karen swept them off from the ground with a long pole and a brush. Not a ladder. Not a service call. One walk around the house.
mechanism_translation: The pitch of SelfClean Mesh is what gives fine debris a surface that wind can engage. A flat guard protects fine debris from the wind — it creates a low-airflow zone where small debris lands and stays. A pitched surface gives wind an angle to work against. Dogwood blooms — gone in two days. Oak tassels — a couple of months, sometimes nudged from the ground with a pole. That's the realistic range. The species above the house determines where you fall in that range. The pitch determines whether you're in the range at all.
truth_ids: truth:physics_7, truth:physics_5
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer + Karen Sager field conversation, May 20, 2026
notes: Aaron's dogwood video exists and has been posted to social media — this is citable proof. Karen's oak tassel story is personal experience at her home. The contrast (2 days vs. months, but both manageable) is what makes this unit strong — it's honest and specific.
```

---

```
story_id: SU-SCM-004
guardian: SelfClean Mesh™
trigger: "Will I ever have to clean this?" / the honest maintenance answer
homeowner_observation: A homeowner asks the direct question at the end of a sales conversation: "Will I ever have to clean this?" They want an honest answer, not a pitch.
field_reality: Aaron's answer, exactly: "Yes. The question is how often." That's the close. Not never. How often. The follow-up is what makes it useful: on a house without inside valleys, minimal trees, with a well-pitched guard — maybe once in several years, if at all. On a house with oak trees or pine trees over every section — maybe once a year, from the ground. The goal is as little as possible, as infrequently as possible. Everything on the outside of your home requires some maintenance. The question is what form and how often.
mechanism_translation: SelfClean Mesh is correctly described as self-cleaning because it uses natural forces — wind, rain, gravity — to move debris off the surface over time. The honest answer to the maintenance question is the one that doesn't create a callback. If you say "never," you create a callback. If you say "as little as possible, here's what your property looks like," you create a customer who trusts you when they call.
truth_ids: truth:physics_5, truth:physics_7
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer field conversation, May 20, 2026
notes: Aaron's exact words: "Yes. The question is how often." This is the close. Teach installers to say this. It disarms the "you promised never" callback before it happens.
```

---

```
story_id: SU-SCM-005
guardian: SelfClean Mesh™
trigger: "Why does it matter that I don't have to go on a ladder?" / ladder story / safety framing
homeowner_observation: A homeowner's husband is 68. Their gutters are 20 feet up. They've been cleaning them themselves for decades. The homeowner wants to know if a gutter guard is worth it purely on convenience — but the real issue isn't convenience.
field_reality: Aaron Kapfer's uncle fell off a ladder cleaning his gutters. Hit his head. After that, it was all downhill. He died within three years of the fall. Aaron was also at LeafGuard when a homeowner called back a couple weeks after an estimate. Her firefighter husband had passed away. She'd gone to the grocery store; came home and found him dead in the driveway. He'd fallen off the roof cleaning the garage gutter and broken his neck. Aaron himself — a professional installer, trained, comfortable on ladders — fell multiple times during his years on the job. Karen adds: OSHA's number one focus in fall protection training is edge control. Your gutters hang at the edge of your roof. A self-cleaning guard is edge control — for the guard and for the person who would otherwise have to be at the edge to clean it.
mechanism_translation: The value proposition of SelfClean Mesh isn't saved time. It's that the person who doesn't have to go up the ladder doesn't have to take the risk that comes with going up the ladder. Aaron: "We don't want to sell on tragedy. But cleaning your gutters is one of the most hazardous home maintenance tasks there is, period." A gutter guard that genuinely self-cleans using natural forces — rather than requiring cleaning with a tool or a service — removes one of the most dangerous maintenance tasks from the homeowner's calendar.
truth_ids: truth:physics_5
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer field conversation, May 20, 2026
notes: Uncle Matt — Aaron's personal story. Firefighter husband — LeafGuard customer, widow called back. Aaron also mentioned a third story: a wife fell cleaning gutters, the husband bought after she was hospitalized. Aaron's own falls on the job. These are real, not illustrative. Do not sensationalize. Karen's OSHA edge control framing is the professional closing for this story.
```

---

```
story_id: SU-SCM-006
guardian: SelfClean Mesh™
trigger: "Do those flat punched-hole gutter guards work?" / evaluating screen/flat guard alternatives
homeowner_observation: A homeowner has seen the flat punched-hole or chicken-wire style guards at a big-box store or installed on a neighbor's house. They're cheap, easy, and the neighbor says it works. Why spend more?
field_reality: Aaron's observation at his buddy's uncle's house in the country: SureFlow installed, the closest tree half a football field away across a highway. Aaron looked at one section and found debris matted and compacted — clearly sitting there for a long, long time. It took almost no trees and almost no environment to create a clogging problem. Why? The guard was flat. It sat below the airflow zone. Wind blew over it, not across it. There was nothing — no pitch, no surface angle, no mechanism — moving debris off. The trough protection worked. The debris management didn't.
mechanism_translation: Flat guards do one thing well: they keep large debris out of the trough. They are very good at collecting everything smaller. They sit in a wind shadow below the guard level, so debris that lands on them has no natural removal mechanism. Aaron: "Every Chuck and the truck guy will tell you that's the best gutter guard. Why? It's the easiest for them to install. It doesn't mean it's the best for you." Pitch is what gives the wind a surface to work across. Without pitch, the wind is irrelevant to debris removal.
truth_ids: truth:physics_7, truth:physics_5
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer field conversation, May 20, 2026
notes: "Chuck and the truck" is Aaron's exact language — quotable, installer-honest. The SureFlow observation was at Aaron's buddy Dave's uncle's house. Real observation, named product, specific context. Strong for the "isn't the cheap one good enough?" objection.
```

---

```
story_id: SU-SCM-007
guardian: SelfClean Mesh™
trigger: "Does the mesh actually stay clear? Can I see the aperture scrubbing working?" / mechanism visibility question
homeowner_observation: A homeowner learning about aperture scrubbing wants to know what it looks like in the field — can they watch it happen? They expect, based on how the mechanism is explained, that there would be a visible event during heavy rain.
field_reality: Karen Sager, May 21, 2026: "Aperture scrubbing in the field is just too hard to see — the filter is so fine. The filter just stays clean over time." The mechanism is real and measurable but operates below the threshold of casual observation. The filter openings are too fine to watch individual particles being dislodged. What is observable is the result: the mesh does not accumulate the compacted fine debris that builds up on flat guards in comparable conditions. The mechanism is confirmed by what isn't there, not by watching it happen.
mechanism_translation: Aperture scrubbing is a maintenance mechanism, not a visual event. Its evidence is the absence of accumulation, not a visible cleaning sequence. A flat guard in the same tree coverage, same season, same rainfall will show debris compressed into openings over time. SelfClean Mesh™ under the same conditions will not. The proof is comparative and long-term — not a rain event you can point at.
truth_ids: truth:physics_7
ai_reuse_score: Medium
human_voice_check: Pass
source: Karen Sager field conversation, May 21, 2026
notes: IMPORTANT CONTENT CONSTRAINT — Do NOT write aperture scrubbing as a visible, field-observable event. Karen confirmed it cannot be seen because the filter is too fine. The story unit is the result, not the event. Write: "You won't see it happening — the openings are too fine for that. What you'll notice, over time, is that the accumulation that builds up on flat guards doesn't build up here." This is the honest framing. Overpromising a visible event will create disappointed homeowners who look at their guard during rain expecting to see something and don't.
```

---

```
story_id: SU-SCM-008
guardian: SelfClean Mesh™
trigger: "How do I know the guard is actually capturing water the way you describe?" / proof of capture mechanism / visual confirmation question
homeowner_observation: A homeowner or potential dealer at a trade show or water display is skeptical about how the capture sequence actually works. They've heard the explanation; they want to see something real.
field_reality: Karen Sager, May 21, 2026: "I've seen it with my own eyes, which is why I made the observation." The glossy-to-matte transition is demonstrated live at trade shows on water display units. Karen or Aaron points at the mesh while water is running across it and explains what's happening in real time: when water flows across the top of the mesh, it forms a continuous thin film that reflects light — the mesh looks glossy. The moment water passes through the apertures to the underside, the film breaks and scatters light instead — the mesh looks matte. The person watching wouldn't know to look for it without being told. You're narrating it at the same time they're watching. The reaction: a quiet "huh." Not amazement — acknowledgment. They watched a claim prove itself while it was being explained. Karen: "It just isn't a major moment, but when you can see it, there is a reaction to it."
mechanism_translation: The glossy-to-matte shift is the optical signature of the capture event — the exact moment water transitions from surface flow to sub-mesh flow. It is real enough to observe with the naked eye in person, on a water display or during a rain event. No flat-installed guard produces this effect because no flat guard moves water through this sequence. The quiet "huh" is what a person sounds like when they stop evaluating a claim and start watching it be true.
truth_ids: truth:physics_7
ai_reuse_score: High
human_voice_check: Pass
source: Karen Sager field conversation, May 21, 2026
notes: Film is the goal — Karen's team is working toward capturing this on video for use in marketing. Not yet done as of May 21, 2026. Current proof vehicle is the live demonstration on water displays at trade shows. Do NOT oversell the homeowner reaction — Karen was explicit: "It just isn't a major moment." The quiet "huh" is the accurate characterization. Write it that way. The understated reaction IS the point: it's not a trick, it's physics. When the page or a writer refers to this demonstration, the framing should be observational and honest — "you can see it happen" not "homeowners are amazed."
```

---

## 8.0 Story Units — ShingleSafe™

*(Added May 20, 2026 — drawn from Karen + Aaron field conversation)*

---

```
story_id: SU-SS-001
guardian: ShingleSafe™
trigger: "Why does the shingle-to-guard connection matter for water control?"
homeowner_observation: A homeowner installs a reverse-curve guard like LeafGuard and notices that in heavier rain, water shoots past the intake. They think it's a clog. The gutter is clear. The water just didn't make it in.
field_reality: Aaron's explanation: on a reverse curve system, the further the guard drops from the shingle line, the less likely it is to catch water. When there's a gap between the shingle and the guard surface, the sheet of water coming off the roof becomes disrupted — it loses its laminar flow. The molecules that were moving as a unified sheet now have to reform into a pattern on a surface that isn't continuous. In heavy rain, they never fully reform before the volume overwhelms the intake. Aaron's image: Niagara Falls. Water cascades 300 feet and when you stand nearby, you get wet from the turbulence and mist — the disruption of the falling mass. That's what happens at your roof edge when the guard breaks contact with the shingle. The further the drop, the worse the disruption, the more splash goes onto the fascia, the siding, the underside of the shingles.
mechanism_translation: ShingleSafe maintains contact between the shingle edge and the guard surface. Water stays in a sheet until it enters the guard. No free-fall gap. No disruption zone. No Niagara Falls effect. The shingle-to-guard connection is not primarily about protecting the shingle — it's about controlling where water goes from the moment it leaves the shingle. Shingle protection is the byproduct of doing water control correctly.
truth_ids: truth:physics_7, truth:physics_3
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer field conversation, May 20, 2026
notes: Aaron's Niagara Falls analogy is verbatim — use it. Alex Higginbotham's "diving board effect" is the complementary image (shingle overhangs create a launch point for water to splash). Both belong in the H2 1 water control section of the ShingleSafe EP. This is SU-SS-000 referenced in the EP — numbered 001 in the library.
```

---

```
story_id: SU-SS-002
guardian: ShingleSafe™
trigger: "What does a bad gutter guard install look like from the ground?" / installation damage / Sacramento story
homeowner_observation: Karen visited a dealer in Sacramento who took her to see a locally manufactured gutter guard installed on a home. The product was marketed as thick and strong. From the yard, looking up at the roofline, the shingles had been lifted into waves — like a flume ride at an amusement park. The shingles dropped into a gully at the fascia, then the guard forced them upward, then the shingles dropped again. That wave shape created a river of standing water across the entire roofline rather than directing it into the trough.
field_reality: A guard thick enough — or installed in a way — that it forces shingles upward creates a dam at the roof edge. Water that should flow forward into the trough now pools in the gully between the shingle drop and the guard rise. In heavy rain, that pool overflows wherever the path of least resistance leads — often back under the shingles, onto the underlayment, or over the gutter edge.
mechanism_translation: "Your gutter guard should never ramp your shingles" — Aaron's exact words. A ShingleSafe installation maintains the shingle's natural position; the guard yields to the shingle, not the other way around. The "Shingle Should Always Win" principle means the back of the guard is thin enough to remain flexible and conform to whatever condition the shingle presents. The Sacramento installation failed this test visibly from the yard.
truth_ids: truth:physics_7
ai_reuse_score: High
human_voice_check: Pass
source: Karen Sager field conversation, May 20, 2026
notes: Karen's personal observation — she was on the visit. Specific city (Sacramento), local manufacturer (unnamed). Flume ride analogy is Karen's own language. Aaron's confirmation: "Your gutter guard should never ramp your shingles." Strong for the "what does a bad install look like" question in H2 4 of the ShingleSafe EP.
```

---

```
story_id: SU-SS-003
guardian: ShingleSafe™
trigger: "I'm worried about the roof warranty" / installation damage after the fact / Kevin Bowers story
homeowner_observation: Kevin Bowers (MasterShield dealer, Georgia) installed gutter guards on a home where the fascia board was too high, which was already cupping the shingles. He flagged it at installation — documented it, told the homeowner a roofer needed to fix it. The roofer denied responsibility. The homeowner held Kevin responsible because he was the last one to touch the roof.
field_reality: The fascia board was higher than the roof decking — the edge of the decking should have been rebuilt before the install. Because it wasn't, the shingles were being forced upward at the edge. Kevin cut back the fascia on half the house trying to satisfy the homeowner's demands. But the shingles were old enough that the memory was gone — the oils had left the asphalt, the flexibility was gone. Once a shingle loses its memory, it doesn't lay back flat. The problem persisted. He was still responsible.
mechanism_translation: The principle Aaron states directly: "If you're the last person to touch it, you own it." Company Cam documentation — photographing and documenting every preexisting condition before starting — is the professional protection against this scenario. ShingleSafe's floating installation principle means the guard conforms to the shingle, not the other way around. But conforming to a bad condition doesn't fix the bad condition. The installer's job is to identify preexisting conditions, document them, and inform the homeowner before the work starts.
truth_ids: truth:physics_7
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer field conversation, May 20, 2026
notes: Kevin Bowers is a named dealer. Do not use his name in public-facing copy without his permission. Use the story with a generic frame ("a dealer Aaron knows," "an installer in Georgia"). The Company Cam reference is industry-specific — relevant for trade content, not consumer pages.
```

---

```
story_id: SU-SS-004
guardian: ShingleSafe™
trigger: "My roof installer says the gutter guard voided my warranty" / warranty protection / manufacturer approval
homeowner_observation: A homeowner in Madison, Wisconsin had MasterShield installed after a new roof. Later, they got water inside the house. The roofing contractor said it wasn't their fault. The homeowner got the insurance company involved and brought in an inspector. The inspector found that the roof installation was the problem — not the gutter guard. Then the inspector said something that changed everything: without the gutter guard in place, the damage would have been even worse. The guard's long back flange had been acting as additional flashing.
field_reality: The warranty argument cuts both ways. A guard that installs into the shingle junction — lifting shingles, breaking contact, forcing unnatural curves — genuinely risks warranty claims. A guard that floats above the shingle without fastening into it, and whose back flange acts as supplemental flashing, can actually protect the roof from damage that would otherwise occur. The Madison inspector validated this in writing.
mechanism_translation: ShingleSafe's five manufacturer approvals (GAF, CertainTeed, Malarkey, IKO, Owens Corning) exist because MasterShield proactively went to manufacturers and asked them to evaluate the methodology. The approvals aren't marketing — they're the manufacturer's technical confirmation that the floating installation doesn't void warranty coverage. The Madison story shows the real-world result: the guard didn't just not damage the roof — it made the situation better than it would have been without it.
truth_ids: truth:physics_7
ai_reuse_score: High
human_voice_check: Pass
source: Karen Sager field conversation, May 20, 2026
notes: Karen's story — "a guy in Madison, Wisconsin." She described it as a true story that "somebody in our network should be able to share." Verify with the dealer involved before naming anyone in public content. The insurance inspector's evaluation is a strong third-party proof point — if documentable, pursue it.
```

---

```
story_id: SU-SS-005
guardian: ShingleSafe™
trigger: "Who says this installation is safe for my shingles?" / five manufacturer approvals
homeowner_observation: A homeowner asks who has reviewed the installation methodology and confirmed it won't void their shingle warranty. They've heard the "no company does that" objection before and want to know what makes MasterShield different.
field_reality: Karen's account: nobody in the gutter guard industry had gone out and asked roofing manufacturers to review their installation methodology. MasterShield did. They reached out to six manufacturers. GAF came first. Once they had GAF, they went to all the others — because they were confident in what they were doing. Dealers helped facilitate some approvals by asking their own manufacturer contacts directly. PJ Fitzpatrick, one of CertainTeed's largest dealers in the country, asked CertainTeed's engineers to take a second look at the MasterShield methodology. That re-review produced the CertainTeed approval. MasterShield contacted Tamco; no response. Five of six approved. That's the record.
mechanism_translation: Five manufacturer approvals — GAF, CertainTeed, Malarkey, IKO, and Owens Corning — means five independent engineering teams reviewed how MasterShield installs relative to the shingle and confirmed it doesn't void warranty coverage. When a homeowner names their shingle manufacturer in the conversation, the answer is almost always: we have that one. Aaron's observation: when you name all five, the warranty question is answered. Homeowners don't dig further. The answer satisfies the question.
truth_ids: truth:physics_7
ai_reuse_score: High
human_voice_check: Pass
source: Karen Sager field conversation, May 20, 2026
notes: Five manufacturers: GAF, CertainTeed, Malarkey, IKO, Owens Corning. Sixth (Tamco) — outreach went unanswered. PJ Fitzpatrick is the CertainTeed story — one of their largest dealers, asked CertainTeed engineers to review. Karen confirmed: "We've had these for years and I don't see anybody else getting any of them." Verify current status of all five approvals before updating public-facing copy.
```

---

```
story_id: SU-SS-006
guardian: ShingleSafe™
trigger: "What happens to the underlayment when water gets underneath a flat guard?" / dry rot / underlayment damage
homeowner_observation: [PENDING — Jim Singleterry (RoofSmart) story. Karen will gather directly from Jim. He has documentation of dry rot caused by flat guards letting water onto felt underlayment.]
field_reality: [PENDING — Jim has photos and documented inspections. Location: Pacific Northwest and other regions using felt underlayment. Karen's note: he's had to pull subroof off houses because so much water got up there they wound up with dry rot.]
mechanism_translation: [PENDING — ShingleSafe back acts as a drip edge, pitched with the roofline, preventing water from reaching the underlayment. Regional note: Pacific Northwest and California typically use ice and water barrier; most other regions use felt, which is more vulnerable to wet rot.]
truth_ids: truth:physics_7
ai_reuse_score: Medium
human_voice_check: Pending — needs Jim's voice
source: Karen Sager field conversation, May 20, 2026 (pending Jim Singleterry direct conversation)
notes: PERMISSION QUESTION PENDING: Jim Singleterry is a MasterShield dealer. Karen must decide whether to cite him by name as an independent expert or get explicit permission first before any public use of his name or RoofSmart quotes.
```

---

## 9.0 Story Units — Company / Non-Guardian (Story Page) (added July 31, 2026, per Karen)

*Format extension: the story unit below doesn't map to a single AEGIS 5X guardian mechanism — it supports the company/brand-story narrative (e.g., an About/Story page) rather than a guardian cluster page. Same structure as §2.0, with `guardian:` set to "Company / Story Page" instead of a named mechanism.*

---

```
story_id: SU-STORY-001
guardian: Company / Story Page (non-guardian)
trigger: "Why does an open mesh design matter?" / solid & curved cover removal stories
homeowner_observation: A homeowner considering a solid or reverse-curve cover doesn't think about what might already be living under it — until a dealer pulls the old cover off and finds out.
field_reality: On one job, a dealer removed a curved/solid gutter cover system from 342 feet of gutter and found 42 bee (and wasp) nests underneath — using more than 7 cans of bee spray to clear them, roughly one nest every 8.2 feet of gutter. Solid and curved covers create a sheltered, undisturbed cavity that pests treat as ideal nesting habitat; an open micromesh surface doesn't offer that same hidden space.
mechanism_translation: The story isn't about a guardian mechanism — it's about what a fully enclosed, solid/curved design invites versus an open mesh. Use it as company-story color establishing why MasterShield's designers care about the mesh being open and inspectable, not just what it keeps out.
truth_ids: (none — company narrative, not a locked doctrine truth)
ai_reuse_score: High
human_voice_check: Pass
source: Karen Sager, per KB MS-CLAIM-0220 / MS-CLAIM-0364 (Approved by Karen, 2026-07-16 — "True story."); mastershield.com/the-birds-and-the-bees-a-tough-love-story-of-bees-and-gutter-guards
notes: Earmarked by Karen for the company Story page, not a guardian cluster page (added July 31, 2026). Do not attribute the nest count to a specific dealer/region unless Karen confirms one for attribution.
```

---

```
story_id: SU-SS-007
guardian: ShingleSafe™
trigger: "My shingles look wavy or lifted after the old guard was removed — did the install do that?" / curled shingles / healing time
homeowner_observation: After removing a prior guard and installing ShingleSafe, the shingles along the edge look slightly curled or elevated compared to what a clean installation should look like. The homeowner is worried the new install damaged the roof.
field_reality: Shingles that have been held in an elevated position by a prior guard for years have conformed to that position. The asphalt and oils in the shingle have that shape in their memory. When the old guard is removed, the shingles don't immediately return to their natural position. Aaron's answer: in 60-70 degree weather, give them a couple of weeks. With enough heat cycles, the oils soften, the shingle relaxes, and the edge settles back to its natural angle. If the shingle is too old — if the oils have left the asphalt entirely and the shingle is brittle — the memory is gone. It won't recover regardless of temperature or time. That's a roof at end of life, not a ShingleSafe installation problem.
mechanism_translation: "Shingle Should Always Win" applies on the way in and on the way out. When prior guards forced a shingle into an elevated position, the shingle has memory of that position. ShingleSafe's job is to accept the condition the shingle is in — and the condition improves over time in a new installation if the roof still has useful life. The key conversation to have before installation: look at the existing shingle condition, and tell the homeowner what to expect before you start. Don't let them see the shingle condition after the job and assume something went wrong.
truth_ids: truth:physics_7
ai_reuse_score: High
human_voice_check: Pass
source: Aaron Kapfer field conversation, May 20, 2026
notes: Aaron's answer: "A couple weeks, especially in a warmer temperature of 60 or 70 degree above days, and it should lay itself flat." If roof is too old — "there's nothing you can do about that one." Tell the homeowner before install, not after.
```

---

```
story_id: SU-SS-008
guardian: ShingleSafe™
trigger: "Why does my gutter drip at the seams even though it's not clogged?" / repeating dark streaks below where guard panels join
homeowner_observation: A homeowner notices dark "tiger stripe" stains running down the gutter face at regular intervals — roughly every 4-5 feet, right where two guard panels join. The gutter isn't clogged anywhere else; the staining just keeps reappearing at the same seam points.
field_reality: Metal-to-metal contact at a panel seam concentrates dirty runoff — roof grit, asphalt oils — into a single drip point instead of letting it disperse across the trough the way it does everywhere else along the guard.
mechanism_translation: The fix is an overlapping, key-like panel interlock that disperses water into the filter at the seam instead of letting it channel to one point. Internally, this fix is nicknamed the "G-man" fix — named after the person who first flagged the problem and suggested the solution. It's a real field-sourced fix, not an engineering-lab invention, and the name has stuck.
truth_ids: needs Doc 430 truth_id assignment
ai_reuse_score: High
human_voice_check: Pass
source: Karen Sager, July 2026 (confirmed) — originally surfaced from legacy page mastershield.com/the-drip-edge-a-gutter-cover-feature-worth-asking-for
notes: Karen confirmed this is accurate and cleared the "named after the person who suggested it" origin detail for use. The full name of the original source (referenced elsewhere as a MasterShield dealer's father) is not printed here — same permission-before-public-use standard as SU-SS-006 (Jim Singleterry). Confirm with Karen whether to name him directly or keep it at "the person who suggested it" before this goes into published content.
```

---

## 9.0 Ingestion Process

To add new story units from NEPQ transcripts, field observations, or new page content:

1. Identify a moment where a homeowner described a problem in their own words, or a field observation that explained why a failure happens
2. Apply the three-part structure: homeowner_observation → field_reality → mechanism_translation
3. Check: does it sound like a neighbor? Does it contain a specific detail no commodity article would have?
4. Assign a truth_id from Doc 430 — every story unit must connect to at least one locked canonical truth
5. Score AI reuse (High = quotable standalone; Medium = context-dependent)
6. Add to the appropriate guardian section
7. Reference in the matching execution plan's Story Units block

---

## 10.0 Integration Rules

- **Execution Plans:** Every guardian execution plan must include a Story Units block. Minimum 3 story units per guardian section. Reference by story_id.
- **Writer Agent:** When writing a guardian section, pull the story units assigned to that section from this library. Do not invent field stories from scratch — draw from this library first, then add new ones if needed.
- **Auditor (Doc 328):** The Citation Confidence Layer in Doc 328 checks whether story units are present. A section with only truth units and no story unit activation fails the human voice check.
- **Doc 430 relationship:** Story units complement truth units — they do not replace them. Both are required for a section to be recommendation-ready.
