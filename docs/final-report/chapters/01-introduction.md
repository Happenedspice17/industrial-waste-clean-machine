# Introduction

## Motivation and need

Facilities that work with raw materials, such as machining shops, foundries and metal-forming lines, routinely
accumulate a film of oil, grease, coolant and metal chips on their walking and working surfaces. This residue lowers
the quality of the working environment, accelerates the wear of equipment and, most seriously, turns ordinary floors
into slip hazards. Cleaning during production is impractical and unsafe, so contamination is often tolerated until a
scheduled stoppage, and the people who clean it are exposed to the same fluids and sharp chips.

The size of the problem is documented. Liberty Mutual's 2023 Workplace Safety Index for manufacturing ranks falls on
the same level as the second most costly cause of serious, non-fatal injury in the sector: about USD 1.20 billion, or
14.4 % of the USD 8.32 billion that U.S. manufacturers spend each year on injuries that cause more than five days away
from work [1]. Across all U.S. workplaces, National Safety Council data compiled from the Bureau of Labor Statistics
record 264,920 same-level-fall cases involving days away from work in 2023–2024 and 134 deaths in 2024 [2].
Slipperiness is governed by the friction available between shoe and floor, and liquid or oily contaminants are among
the main factors that reduce it [3]. The contaminants also carry a health burden: OSHA and NIOSH link skin contact and
mist from metalworking fluids to dermatitis, eye, nose and throat irritation, and respiratory disease [4], [5].

The Mexican context makes the need sharper. Manufacturing is close to 20 % of Mexico's GDP, Mexico is the ninth
largest manufacturing exporter and 85.9 % of its manufacturing exports go to the United States [44]. STPS and IMSS
recorded 290,527 work accidents and 340 deaths in 2023 [45]. Nearshoring brings more machining plants, and the
minimum wage rose 13 % in 2026 [40], which raises the value of every hour of manual cleaning that can be automated.
NOM-001-STPS-2008, numeral 7.4, requires that floors be free of liquids and greases that create slip or fall hazards
[47].

These figures define a specific and measurable need in metalworking plants: **to remove floor lubricants and metal
chips during windows when nobody is exposed, such as shift changes, and to hand the waste over already segregated so
that the oil is not diluted and the chips can be recycled or disposed of correctly.**

## What happens on the floor today

| Observation | Consequence |
|---|---|
| Cleaning waits for a stoppage | Oil films and sharp chips stay on walkways for whole shifts |
| Workers handle the fluids by hand | Exposure to metalworking fluids (dermatitis, respiratory disease) and cuts from chips |
| Granular absorbent is spread on spills | Oil, chips and absorbent become one mixed hazardous waste with no recycling value |
| Regulation asks for clean floors | NOM-001-STPS-2008 7.1.1 and 7.4: permanent order and cleanliness; no pooled liquids |

## Literature review

### Autonomous floor cleaning

Floor-cleaning robots are a mature research and commercial area, but mostly in domestic and commercial-hygiene
settings. Prassler et al. trace the evolution of cleaning robots and show that most systems target dust and debris on
dry floors [6]. Two enabling technologies are well established. Complete-coverage path planning lets a mobile platform
sweep a bounded area systematically, and differential-drive kinematics give the maneuverability to do so in tight
spaces; Le et al. demonstrate both in an energy-optimized, self-reconfigurable cleaning robot [7]. For localization,
simultaneous localization and mapping (SLAM) is the standard method for building a map and tracking the robot's pose;
Cadena et al. review its maturity and the open problems of operating in perceptually difficult environments such as
reflective industrial spaces [8].

### Separation and recovery of machining waste

Separating the collected waste draws on minerals processing and sustainable machining. Low-intensity magnetic
separation is the standard low-energy method for extracting ferrous particles from a mixed stream [9]. On the fluid
side, the recovery of spent cutting fluid is technically feasible and economically attractive: Debnath et al. review
environmentally friendly cutting fluids and cooling strategies [10], and Lee et al. review recycling technology for
both cutting fluids and metal chips, concluding that the two streams keep the most value when they are kept
segregated [11].

### Technological benchmark: commercial machines

| Solution | Autonomous | Recovers oil undiluted | Separates ferrous chips | Separate storage | Price |
|---|:-:|:-:|:-:|:-:|---|
| Manual cleaning + granular absorbent | ✘ | ✘ | ✘ | ✘ | Labor + absorbent + mixed-waste disposal |
| Kärcher KIRA B 50 autonomous scrubber | ✔ | ✘ (cleans with water) | ✘ | ✘ | ≈ MXN 2.0 million [42] |
| Tennant T380AMR autonomous scrubber | ✔ | ✘ (cleans with water) | ✘ | ✘ | ≈ USD 75,000 [43] |
| Patents reviewed (Table 1.3) | ◐ | ✘ | ◐ | ✘ | — |
| **This project** | **✔** | **✔** | **✔** | **✔** | **≈ MXN 31,600 unit cost; ≈ 60,000 proposed price (estimate)** |

Legend: ✔ yes · ◐ partial · ✘ no.

### Patent prior art

A search in Espacenet found related inventions that each cover only part of the problem.

| Patent | Focus | Gap with respect to this project |
|---|---|---|
| US2007271004A1 [12] | Household cleaning robot with edge/boundary sensors | No industrial route, no liquid recovery, no separation |
| CN112641396A [13] | Industrial cleaning robot with a pressurized-water dispenser | Adds water as a third stream; does not recover oil |
| CN114129101A [14] | Cleaning machine that decomposes oil with high-temperature steam | Destroys rather than recovers the lubricant |
| CN115319717A [15] | Robot that collects metal debris | Little attention to lubricants; no dual-stream storage |
| EP2808668A1 [16] | Detection and change of machine lubricant | Services machines; does not clean floors |

**Bounded gap statement.** In the literature and patents reviewed, no system was found that combines autonomous floor
collection with on-board separation of the liquid and ferrous fractions into independent containers. This is a gap in
the sources reviewed, not a claim of absolute novelty; a broader market search is part of the next steps. (The first
draft of the proposal made an absolute novelty claim; it was corrected in the improved proposal, see Chapter 2.)

## Problem formulation

Metalworking plants need a mobile robot that can work unattended during shift changes, recover liquid contaminants
(lubricant and oil) and solid contaminants (ferrous chips) from the same surface, and store them in separate
containers so that the lubricant is never mixed with metal and no water, steam or chemical is added. Solving this
requires three subsystems that the literature has developed separately:

- a mechanical and traction platform that stays stable and controllable on low-friction, oily floors;
- an on-board waste-processing chain that combines brush agitation and vacuum collection with mesh filtration,
  magnetic separation and compaction of the solids; and
- a perception and control system that navigates reflective, oily surroundings, stops safely and only runs when an
  authorized operator starts it.

**Constraints.** A 12 V battery-powered academic prototype; a component budget of about MXN 17,500 including tooling;
parts available in Mexico; demonstration in a controlled test area.

The real engineering challenge is not driving around: it is **picking up dense steel chips and oil with a 12 V
vacuum, separating them on board and never mixing the two streams, safely, with people and forklifts nearby.**

## Hypothesis

If a differential-drive, oil-compatible mobile platform integrates a rotary brush and squeegee that direct residues to
a vacuum nozzle, a sealed separation chamber (stainless mesh basket, neodymium magnets and a force-limited compactor)
and an independent liquid tank, controlled by an Arduino UNO Q with LiDAR, IMU and encoder localization and a hardware
emergency stop, then, on a controlled test floor with the reference lubricant and ferrous machining chips, the
prototype will:

- recover at least **85 %** of the spilled liquid and 85 % of the chips in a single pass over a 1 m² patch (metric M1);
- deliver a liquid stream with at least **95 %** purity (no solids larger than 1 mm) and a solid stream with at least
  **90 %** purity (no free oil) (metric M2); and
- cover at least **100 m² per hour** of a stored route with **zero safety incidents** (metric M3).

The hypothesis is rejected for a function if its metric falls below the threshold under the idealist test conditions
defined in Chapter 8.

## General objective

To develop and validate a compact autonomous mobile prototype that collects lubricant and metal chips from a
manufacturing floor during shift changes, separates the ferrous fraction and coarse solids from the liquid by
mechanical filtration and magnetic capture, compacts and drains the solids, and stores the two waste streams in
separate containers, with safe mobility, route mapping, a defined vision function and authorized operation controlled
by an Arduino UNO Q.

## Specific objectives

| ID | Specific objective | Indicator and target | Req. |
|---|---|---|---|
| OE1 | Design and integrate a suction collection system (brush, squeegee, nozzle, lubricant-resistant hose, vacuum unit with sensor) that picks up lubricant and chips from the floor | Recovered mass, collection time and residual liquid; M1 ≥ 85 % | R1 |
| OE2 | Design a module that retains coarse solids with a mesh filter, captures the ferrous fraction with magnets into a basket, and compacts and drains the solids with a force-limited linear actuator | Captured solids by size and material, volume reduction, drained liquid, actuator force ≤ 100 kgf; M2 solids ≥ 90 % | R2, R3 |
| OE3 | Implement separate liquid and solid storage with drain-valve emptying, leak tray and level cut-off | No mixing between streams, no leaks, cut-off acts before overflow; M2 liquid ≥ 95 % | R9, R5 |
| OE4 | Build an oil-compatible differential-drive platform that localizes with encoders, IMU and LiDAR, saves and repeats routes, and runs the defined vision task with camera and LED light | Traction, stopping distance, route-tracking error, speed ≤ 0.38 m/s; M3 ≥ 100 m²/h | R4, R6, R7, R8 |
| OE5 | Develop the Arduino UNO Q control architecture (MCU for real-time I/O, Linux for navigation and interface) with RFID and start-button authorization, status indicators and a relay e-stop independent of software | Authorized/unauthorized start, deliberate restart after a stop, e-stop cuts all actuators, watchdog response | R5, R10 |
| OE6 | Validate the complete prototype in a controlled test area with a protocol that fixes acceptance criteria before testing | All indicators recorded with lubricant, solids, floor and load conditions | All |

## Evaluation metrics

| Metric | Definition and test | Pass threshold |
|---|---|---|
| **M1 · Recovery efficiency** | Mass of lubricant and chips recovered ÷ mass spilled on a 1 m² patch, one pass; tank and basket weighed before and after | ≥ 85 % liquid and ≥ 85 % chips |
| **M2 · Stream purity** | Share of each stream free of the other: solids > 1 mm in the tank (filtered and weighed) and free oil drained from the compacted chips | ≥ 95 % liquid stream, ≥ 90 % solid stream |
| **M3 · Autonomous coverage** | Area cleaned per hour on a stored route with zero safety incidents | ≥ 100 m²/h, 0 incidents |

## Scope and boundaries

**In scope.** Supervised commissioning and autonomous-cycle demonstrations in a controlled test area, with shift
changes as the intended operating window; collection, separation, compaction and separate storage; safe mobility,
route storage and mapping; authorized operation; a defined, advisory vision function.

**Out of scope.** Alloy sorting, chemical decomposition of lubricant, mixed operation with people, fleet or cloud
analytics and manipulator tasks. The project does not claim certified industrial operation, guaranteed slip-free
floors or automatic lubricant reusability; filtering does not establish that the lubricant is suitable for reuse.

**Removed from the proposal on purpose.** Pressurized water, heating or steam outlets and the auxiliary-product
container (soap, acid): they would add a third waste stream and contaminate the recovered lubricant. Line sensors
(oil fouls floor markings), swerve drive, separate Wi-Fi and logging modules (the UNO Q has them), industrial vibrator
and brush-lifting motors.

## Project status at the time of this report

<div class="note">

**Initial design, not frozen (November 2026).** Requirements, component selection, conceptual design, nine modules,
priced bill of materials, scenarios, economics, simulations, risk analyses and the presentation are complete. A bench
software tool (AprilTag localization) runs on the UNO Q. **No physical prototype exists and no physical performance
test has been run.** The next gate is the suction rig test (ADR-0004), which decides the collection architecture
before the design is frozen.

</div>

## Structure of this report

Chapter 2 describes the methodology and the course activities that produced each part of the design. Chapters 3–5
follow the course structure: design analysis, theoretical framework and conceptual design. Chapter 6 details the
architecture, Chapter 7 the calculations and simulations, Chapter 8 the scenario analysis, Chapter 9 the risk,
quality and security analyses, and Chapter 10 the standards. Chapter 11 covers the software and tools in the
repository, Chapter 12 the decision records and Chapter 13 the validation plan and status. Chapters 14–16 evaluate
the technological impact, business model and sustainability. Chapter 17 lists the lessons learned, Chapter 18 the
project management and next-semester plan, and Chapter 19 the conclusions. The appendices hold the repository guide,
the full bill of materials, the full requirement text, the glossary, the change history and the credits.
