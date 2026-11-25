# 03 · Standards matrix

Status: applicability analysis for an academic prototype. The prototype is **not certified**. Clause numbers for
ISO 3691-4 come from the published table of contents (full text is paywalled); NOM-001 numerals verified against the
official STPS text.

| Standard | Clause / numeral | Requirement (summary) | Design response | Evidence of implementation |
|---|---|---|---|---|
| ISO 3691-4:2023 | 4.3 Speed control (4.3.1 overspeed) | Limited speed, overspeed detection | ≤ 0.38 m/s, 0.15 cleaning; MCU compares PWM vs encoders | Speed log commanded vs measured; overspeed cut test (> 0.40 m/s) |
| ISO 3691-4:2023 | 4.2 Braking system | Stop within defined distance | Motor braking on H-bridge cut; ≤ 7.4 cm calc on oil | 10 braking tests on oiled floor vs calc |
| ISO 3691-4:2023 | 4.8.1 Emergency stop; 4.1.14 no automatic restart | E-stop overrides; deliberate restart | Hardware relay; RFID + button restart | Wiring diagram; cut test with software hung; stop time |
| ISO 3691-4:2023 | 4.8.2 Detection of persons; 5.2 tests | Detect persons in path | LiDAR stop zone + bumpers; cleared-zone operation | Test-object trials at speeds/angles; detection distance log |
| ISO 3691-4:2023 | Annex A zones; Clause 6 info for use | Prepare operating zones; instruction handbook | Delimited zone; user manual | Zone plan; manual in `docs/manual/` |
| NOM-001-STPS-2008 | 7.1.1 | Permanent order and cleanliness | Cleaning every shift change | Robot log (date, area, m²), M3 |
| NOM-001-STPS-2008 | 7.4 a), b) | No spilled liquids/greases causing slips | Recover oil + chips | M1 test on 1 m² patch |
| NOM-001-STPS-2008 | 7.1.2 | Delimited areas (yellow ≥ 5 cm) | Robot operates inside delimited zone | Zone plan, LiDAR map match |
| NOM-001-STPS-2008 | 5.2, 5.3 | Verifications + records kept 1 year | Exportable digital log | Log export |
| NOM-004-STPS-1999 | — | Guards and safety devices on machinery | Covered brush/compactor; lid interlock; e-stop | Interlock test |
| NOM-026-STPS-2008 | — | Safety colors: red stop, yellow caution, green safe, blue mandatory | Tower green/amber/red; red mushroom e-stop | Photo, HMI spec |
| NOM-029-STPS-2011 | — | Safe electrical maintenance | Fuses, lockable e-stop, battery disconnect | Maintenance procedure |
| NOM-010 / 011 / 017 / 035-STPS | — | Chemical agents / noise / PPE / psychosocial | Less fluid contact; water-based non-flammable degreaser (SR-025); noise test; gloves + glasses at refill (P-001); change management | Test reports, SDS, training record |
| NOM-018-STPS-2015 | — | Hazard communication for chemicals (GHS: SDS, labels) | Degreaser SDS and labels at the refill station; labeled solution and recovery tanks (P-002) | SDS on file, label photos |
| NOM-052-SEMARNAT-2005 + LGPGIR | — | Hazardous waste handling, management plans for used oil | Two labeled streams to authorized handlers; decanted oil + oily water from the degreaser (ADR-0008), never to drain (P-003) | Delivery records |
| ISO 12100:2010 | — | Risk assessment and reduction | DFMEA + 10 protection terms | `risk/dfmea.csv` |
| ISO 13849-1:2023 | — | Performance level of safety functions | Safety in hardware; certified version would need safety relay | PL estimate (future) |
| ISO 13850:2015 / IEC 60204-1 | — | E-stop design; electrical equipment | Category 0 stop via relay | Diagram |
| IEC 60529 | — | IP code | IP54 electronics bay; IPX4 below the deck (conductive solution, F-013) | Enclosure spec, spray test |
| ISO 45001:2018 | — | OH&S management | Robot logs feed plant OH&S indicators | — |
