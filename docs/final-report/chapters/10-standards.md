# Standards and regulation

**Status:** applicability analysis for an academic prototype. The prototype is **not certified**. Clause numbers for
ISO 3691-4 come from the published table of contents (the full text is paywalled); NOM-001 numerals were verified
against the official STPS text. Proper names of Mexican standards stay in Spanish.

## Core standards in the course table format

### ISO 3691-4:2023 — Industrial trucks: driverless industrial trucks and their systems

International standard (2nd edition, 2023) on safety requirements and verification for driverless industrial trucks
(AGV/AMR) and their systems. It replaces the 2020 edition and covers braking, speed, emergency stop, person
detection, operating modes and operating zones [38].

| Feature | Description of the feature in our design | Implementation evidence |
|---|---|---|
| 1. Speed control (Cl. 4.3, 4.3.1 overspeed) | Limited speed with overspeed detection: max 0.38 m/s, 0.15 m/s while cleaning; the MCU limits the PWM and compares it with the encoders | Log of commanded vs encoder-measured speed, overspeed test (cut-off > 0.40 m/s) and video (SR-004, SR-013) |
| 2. Braking system (Cl. 4.2) | Stop within a defined distance, even on an oily floor: motor braking when the H-bridge is cut; calculation ≤ 7.4 cm at 0.38 m/s with μ = 0.1 | Braking test on an oiled floor (10 repetitions), measured vs calculated distance and report (SR-005) |
| 3. Emergency stop (Cl. 4.8.1 and 4.1.14) | Mushroom button that opens the main relay and cuts every actuator in hardware; no automatic restart: an RFID card + start button are required | Relay wiring diagram, cut-off test with the software frozen, measured stopping time and restart checklist (SR-006, SR-014) |
| 4. Person detection (Cl. 4.8.2 and 5.2) | 360° LiDAR with a stop zone and bumpers with limit switches as backup; operation only in a cleared zone during the shift change. A webcam is **not** a safety sensor (ADR-0006) | Tests with a test obstacle at different speeds and angles, recorded detection distance and a log of bumper events |
| 5. Operating zones and information for use (Annex A, Cl. 6) | Delimited operating zone; instruction handbook | Zone plan; user manual (`docs/manual/`, to write) |

### NOM-001-STPS-2008 — Edificios, locales, instalaciones y áreas en los centros de trabajo

Mexican Official Standard of the STPS (DOF 24 Nov 2008) on safety conditions of buildings, premises, installations
and areas of workplaces; it requires the employer to keep them free of risks to workers [47].

| Feature | Description of the feature in our design | Implementation evidence |
|---|---|---|
| 1. Permanent order and cleanliness (Num. 7.1.1) | Permanent order and cleanliness in work areas and aisles; the robot cleans the area at every shift change | Robot log (date, area, m² cleaned), before/after photos and metric M3 result |
| 2. Floors free of hazardous substances (Num. 7.4 a and b) | No spilled liquids or greases that cause slips or falls; the robot recovers oil and chips from the floor | M1 test on a 1 m² patch (mass recovered / spilled), measured residual oil and photos |
| 3. Area delimitation (Num. 7.1.2) | Delimited work and traffic areas (yellow stripes ≥ 5 cm); the robot operates only inside its delimited zone | Plan of the operating zone with stripes, saved LiDAR map that matches the delimitation, and signage |
| 4. Inspections and records (Num. 5.2 and 5.3) | Inspections every 12 months and after events, recorded in a logbook or electronic medium and kept for one year | Robot records (faults, stops, areas, spills) exportable as a digital log, and corrective actions |

## Full standards matrix

| Standard | Clause / numeral | Requirement (summary) | Design response | Evidence of implementation |
|---|---|---|---|---|
| ISO 3691-4:2023 | 4.3 Speed control (4.3.1 overspeed) | Limited speed, overspeed detection | ≤ 0.38 m/s, 0.15 cleaning; MCU compares PWM vs encoders | Speed log commanded vs measured; overspeed cut test (> 0.40 m/s) |
| ISO 3691-4:2023 | 4.2 Braking system | Stop within defined distance | Motor braking on H-bridge cut; ≤ 7.4 cm calc on oil | 10 braking tests on oiled floor vs calc |
| ISO 3691-4:2023 | 4.8.1 E-stop; 4.1.14 no automatic restart | E-stop overrides; deliberate restart | Hardware relay; RFID + button restart | Wiring diagram; cut test with software hung; stop time |
| ISO 3691-4:2023 | 4.8.2 Detection of persons; 5.2 tests | Detect persons in path | LiDAR stop zone + bumpers; cleared-zone operation | Test-object trials at speeds/angles; detection distance log |
| ISO 3691-4:2023 | Annex A zones; Clause 6 info for use | Prepare operating zones; instruction handbook | Delimited zone; user manual | Zone plan; manual |
| NOM-001-STPS-2008 | 7.1.1 | Permanent order and cleanliness | Cleaning every shift change | Robot log (date, area, m²), M3 |
| NOM-001-STPS-2008 | 7.4 a), b) | No spilled liquids/greases causing slips | Recover oil + chips | M1 test on 1 m² patch |
| NOM-001-STPS-2008 | 7.1.2 | Delimited areas (yellow ≥ 5 cm) | Robot operates inside delimited zone | Zone plan, LiDAR map match |
| NOM-001-STPS-2008 | 5.2, 5.3 | Verifications + records kept 1 year | Exportable digital log | Log export |
| NOM-004-STPS-1999 | — | Guards and safety devices on machinery | Covered brush/compactor; lid interlock; e-stop | Interlock test |
| NOM-010-STPS-2014 | — | Chemical agents in the work environment | Less manual handling of fluids; vacuum exhaust is clean air after the sealed chamber; water-based, non-flammable degreaser (SR-025) | Exposure reduction (hours avoided), SDS |
| NOM-011-STPS-2001 | — | Noise exposure limits | Robot runs while the area is empty | Noise test |
| NOM-017-STPS-2008 | — | Personal protective equipment | Nitrile gloves + safety glasses when emptying and when refilling the solution tank (P-001) | Training record |
| NOM-018-STPS-2015 | — | Hazard communication for chemicals (GHS: safety data sheets, labels) | Degreaser SDS and labels at the refill station; labeled, differently colored solution and recovery tanks (P-002) | SDS on file, label photos |
| NOM-026-STPS-2008 | — | Safety colors: red stop, yellow caution, green safe, blue mandatory | Tower green/amber/red; red mushroom e-stop; yellow zone marking | Photo, HMI spec |
| NOM-029-STPS-2011 | — | Safe electrical maintenance | Fuses, lockable e-stop, battery disconnect | Maintenance procedure |
| NOM-035-STPS-2018 | — | Psychosocial risk factors | Change management: inform, train and involve cleaning staff | Training and communication record |
| NOM-052-SEMARNAT-2005 + LGPGIR | — | Hazardous-waste classification, handling, management plans for used oil | Two labeled streams to authorized handlers; decanted oil and oily water from the degreaser, never to drain (P-003, SC-011); battery returned for recycling | Delivery records |
| ISO 12100:2010 | — | Risk assessment and reduction | DFMEA + 10 protection terms | `risk/dfmea.csv` |
| ISO 13849-1:2023 | — | Performance level of safety functions | Safety in hardware; a certified version would need a safety relay with monitored contacts | PL estimate (future) |
| ISO 13850:2015 / IEC 60204-1 | — | E-stop design; electrical equipment of machines | Category 0 stop via relay | Diagram |
| IEC 60529 | — | IP code | IP54 electronics bay; IPX4 below the deck (conductive solution, F-013) | Enclosure spec, spray test |
| ISO 45001:2018 | — | OH&S management | Robot logs feed plant OH&S indicators | — |
| IEEE 7000-2021 | — | Value-based engineering (ethics by design) | EVR-01–EVR-03 (Section 3.4) | Requirements, presentation |
| IEC 62443 (series) | — | Industrial cybersecurity | Threat model, target SL 1–2 | `docs/security/threat-model.md` |
| LFPDPPP (DOF 20 Mar 2025) | — | Protection of personal data held by private parties | No images of people stored; operator ID and time only, privacy notice, limited retention | SR-020; threat model T-01 |

## Laws and national programs

| Instrument | Basic aspects | How it is applied |
|---|---|---|
| Ley Federal del Trabajo + Reglamento Federal de Seguridad y Salud en el Trabajo | Employer must prevent work risks, provide training and keep safe conditions | The robot is delivered with operator training and a risk assessment for the plant |
| LGPGIR (SEMARNAT) | Management plans for wastes such as used lubricating oil | Segregated oil and chips delivered under the plant's plan; kg recovered per month recorded |
| ELSSA — Entornos Laborales Seguros y Saludables (IMSS, 2022) | Culture of prevention in workplaces [51] | Include slip hazards and fluid exposure in the plant's ELSSA diagnosis; robot as a control measure |
| PASST (STPS, guidelines May 2024) | Voluntary OH&S self-management program [52] | Register the robot procedure (authorization, emptying, maintenance) in the safety management system |
| NOM-035 well-being policy | Psychosocial risk prevention | Change-management plan for cleaning staff |
