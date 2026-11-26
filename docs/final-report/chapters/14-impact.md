# Technological impact

Source: *RA1000 ACT.06 Technological impact analysis* (30 Oct 2026). Reference case for the evaluation: one robot
serving a machining cell in a Mexican plant with three shifts a day, 300 working days a year and three shift changes
a day (900 cleaning cycles a year). Each cycle the floor collects about 1.5 kg of chips and 1 L of lubricant. Today
the area is cleaned by hand with granular absorbent during the shift change. All values in MXN; parameters marked
assumption must be replaced with the plant's own quotes.

## Impact matrix

| Dimension | Rubric criterion | Evidence in our project | Indicator / example of consequence |
|---|---|---|---|
| 1. Economic | a. Calculations | Separate economic evaluation (Section 14.2): investment, annual benefits, operating costs, net cash flow, payback and NPV, every formula shown. Academic prototype cost: MXN 97,260 including valued engineering hours | Base case: net benefit MXN 56,968/yr, payback 6.6 months, 3-year NPV at 12 % MXN 105,269. Pessimistic: payback 2.1 years, NPV MXN 7,928 (still ≥ 0) |
| | b. Viability | Each robot removes 2 h/day of manual cleaning (≈ 0.25 of a full-time position), worth MXN 38,041/yr, 60 % of the gross benefit. Every parameter defined with value, unit and source. No missing costs: hardware, tooling, contingency, assembly, commissioning and training, electricity, battery, consumables, maintenance, operator time, oil collection, residual hazardous waste and NRE share | Waste segregation alone (MXN 25,769/yr) already pays back the investment; break-even holds with half the waste benefit, half the labor saving, +30 % opex and +50 % investment |
| 2. Social | Clear implications with examples | Worker safety: the robot removes oil and chips during shift changes, when nobody is in the area. Health and less tedious work: cleaners no longer scrub oil and pick up sharp chips by hand. Employees affected (cleaning staff): fewer cleaning hours, some positions shrink or change. New positions: technicians who operate, empty, program routes and maintain robots. Environment and compliance: streams delivered segregated, undiluted, ready for authorized recyclers | Fewer slips when the next shift starts. 600 h/yr of tedious manual cleaning and 450 kg/yr of oil-soaked absorbent removed per robot. Negative consequence: job loss if the plant only cuts staff → mitigation: retrain cleaners as RFID-authorized operators and reassign freed hours to 5S/inspection. ≈ 2.6 t/yr of mixed hazardous waste avoided; 1.3 t/yr of chips to recycling |
| 3. Cultural | a. Cultural dimensions in problem solving | Adjustment of our own attitudes: we first framed the robot as a replacement for cleaning staff (efficiency view); after considering the operators' perspective we redesigned it as an assistant. Respect for the machine: workers must treat it with care (kicks, carts, forklifts); we protect it with bumpers, n ≥ 3 at bump points, a slipping belt and a watchdog, while training builds a culture of care. Integration of other cultures: the Japanese lean principle *Seiso* (5S: cleaning is inspection) led us to log where oil appears so leaking machines are detected. Bilingual team work; plant experience of a team member (Ford) and FIRST robotics experience shaped safety and modularity | Design changes traced to these perspectives: RFID authorization, human-in-the-loop emptying, protection terms against external forces, oil-location log, cleared-area operation. Next step: interviews with an operator, a maintenance technician and an EHS supervisor |
| | b. Cultural empathy | Attitudes toward the robot: after the initial interest, workers may turn to apathy and stop using it well. Groups: shop-floor operators (Spanish-speaking, varied schooling) → icon/color HMI, Spanish interface, hands-on training; engineers and corporate management → English documentation, KPIs M1–M3, cost data; maintenance and EHS → fault messages, logs, lockable e-stop; unions and supervisors → clear message that the robot reassigns, not eliminates, work | Involve workers before deployment, name responsible operators, show visible results on the LCD and web UI (area cleaned, kg recovered). Indicator: operators can start, pause and empty the robot after a 30-min training without reading English |
| | Broader technological culture | If the robot succeeds it could start a boom of similar machines for other dirty or hazardous floors (food processing, warehouses, workshops) | More automation of dirty and hazardous tasks; need for technicians trained to operate and maintain them in Mexico |
| 4. Safety and health | National/international regulation; public-health strategies | Sections 14.3–14.4 and Chapter 10 | — |
| 5. Ethical | Decisions, perspectives, codes, laws | Section 14.5 | — |
| 6. Impact | Global, economic, environmental, social context | Section 14.6 | — |

## Economic evaluation — explicit calculations

### Parameters

| Parameter | Value | Basis / source |
|---|---|---|
| Operating calendar | 300 days/yr · 3 shift changes/day = 900 cycles/yr | Reference case |
| Waste per cycle | 1.5 kg chips + 1 L lubricant (0.88 kg/L) | Assumption, measure in plant |
| Cleaning labor cost | MXN 315.04 × 1.15 (industrial wage) × 1.40 (employer burden: IMSS, INFONAVIT, SAR, ISN, aguinaldo, vacations) = MXN 507.21/day → MXN 63.40/h | Minimum wage 2026 [40]; factors are assumptions |
| Manual cleaning time (today) | 1.0 h per shift change = 3 h/day | Assumption |
| Operator time with robot | 20 min per cycle (authorize, empty, touch up corners) = 1 h/day → 2 h/day saved | Design cycle |
| Hazardous-waste disposal | MXN 6.00/kg (range 2–10) | Assumption; survey lower bound 1.5–3 MXN/kg [41] |
| Granular absorbent | 0.5 kg/cycle at MXN 20/kg | Assumption |
| Used-oil collection (segregated) | MXN 2.00/kg | Assumption |
| Drained chips sold as scrap | MXN 2.50/kg (below the MXN 4.00/kg HMS reference because of residual oil) | Scrap reference Oct 2026 [46] |
| Electricity | 0.15 kWh/cycle from the grid at MXN 1.347/kWh | CFE GDMTO, Jul 2026 [49] |
| Battery replacement | SLA ≈ 450 cycles at 50 % DoD → 2 batteries/yr × MXN 1,290 | BOM |
| Consumables / maintenance | MXN 1,200/yr (brushes, gaskets, filters, hose) + 24 h/yr × MXN 120/h technician | Assumption |
| Investment per robot | Hardware MXN 20,160 + assembly 60 h + commissioning/training 16 h at MXN 150/h | BOM; hours assumed |
| Horizon / discount rate | 3 years / 12 % per year (annuity factor 2.402) | Assumption |

### Calculations — base case (MXN per year unless noted)

| Item | Calculation | Result |
|---|---|--:|
| **A. Investment (one robot)** | | |
| Hardware incl. tooling and contingency | 15,849.50 + 1,681.00 + 0.15 × 17,530.50 | 20,160 |
| Assembly | 60 h × 150 | 9,000 |
| Commissioning and training | 16 h × 150 | 2,400 |
| **Total investment I₀** | | **31,560** |
| **B. Annual benefits** | | |
| Labor saved | 2 h/day × 300 days × 63.40/h | 38,041 |
| Waste today (manual) | (1,350 kg chips + 792 kg oil + 450 kg absorbent) × 6 + 450 kg × 20 | 24,552 |
| Waste with robot | 792 kg oil × 2 + 5 % fines 67.5 kg × 6 − 1,282.5 kg scrap × 2.50 | −1,217 (net income) |
| Waste benefit | 24,552 − (−1,217) | 25,769 |
| **C. Annual operating costs** | | |
| Electricity | 0.15 kWh × 900 × 1.347 | 182 |
| Battery replacement | 2 × 1,290 | 2,580 |
| Consumables | brushes, gaskets, filters, hose | 1,200 |
| Maintenance labor | 24 h × 120 | 2,880 |
| **Total opex** | | **6,842** |
| **D. Results** | | |
| Net annual benefit | 38,041 + 25,769 − 6,842 | **56,968** |
| Simple payback | 31,560 / 56,968 | **0.55 yr ≈ 6.6 months** |
| NPV (3 yr, 12 %) | 56,968 × 2.402 − 31,560 | **105,269** |
| Prototype project cost (academic, one-time) | Hardware 20,160 + engineering 7 students × 8 h/wk × 9 wk = 504 h × 150 = 75,600 + test lubricant and samples 1,500 | 97,260 |

The annuity factor is $\frac{1-(1+i)^{-n}}{i} = \frac{1 - 1.12^{-3}}{0.12} = 2.402$.

### Scenarios

| Scenario | Changes vs base | Net benefit/yr | Investment | Payback | NPV 3 yr |
|---|---|--:|--:|--:|--:|
| Optimistic | 2.5 h/day saved; waste benefit +20 % | 71,633 | 31,560 | 5.3 months | 140,489 |
| **Base** | Parameters above | **56,968** | **31,560** | **6.6 months** | **105,269** |
| Pessimistic | 1 h/day saved; waste benefit −50 %; opex +30 %; investment +50 % | 23,011 | 47,340 | 2.1 years | 7,928 |
| Pessimistic + NRE | Pessimistic + development cost shared over 10 robots (MXN 7,560 each) | 23,011 | 54,900 | 2.4 years | 368 (break-even) |

`tools/econ.py` reproduces the base and pessimistic cases exactly. Its built-in optimistic case changes only the hours
saved (2.5 h/day, waste benefit unchanged), so it reports MXN 66,479/yr, 5.7 months and NPV MXN 128,111; the table
above (Activity 06) also raises the waste benefit by 20 %.

### Sensitivity (tornado, NPV change from base)

| Parameter | Low | High |
|---|--:|--:|
| Hours saved per day | −45,684 | +22,842 |
| Disposal price (MXN/kg) | −24,254 | +24,254 |
| Hardware cost | −10,080 | +6,048 |
| Scrap price (MXN/kg) | −4,621 | +4,621 |

**Reading.** The project is viable as long as the robot saves at least about 1 h of manual cleaning per day and the
plant pays for hazardous-waste disposal. Injury savings are not included in any scenario; they would only improve the
result. The main uncertainty is the disposal price, which must be quoted with the plant's authorized waste
contractor. All figures are **estimates**.

## Safety and health regulations applied to the design

| Regulation | Basic aspects | How it is applied |
|---|---|---|
| Ley Federal del Trabajo and Reglamento Federal de Seguridad y Salud en el Trabajo | Employer must prevent work risks, provide training, keep safe conditions | Robot delivered with an operator training program and a risk assessment for the plant |
| NOM-001-STPS-2008 | Permanent order and cleanliness; floors must not let liquids pool [47] | The main need the robot answers |
| NOM-004-STPS-1999 | Guards, safety devices and stop controls; lockout for maintenance | Covered brush and compactor, hardware e-stop, compactor runs only with suction stopped and lid closed |
| NOM-010-STPS-2014 | Evaluation and control of exposure to airborne chemical agents | Less manual handling of fluids and absorbent; vacuum exhaust is clean air after the sealed chamber |
| NOM-011-STPS-2001 | Noise exposure limits | Robot noise to be measured; it runs while the area is empty |
| NOM-017-STPS-2008 | PPE selection and use | Nitrile gloves and safety glasses when emptying the tank and chip basket |
| NOM-026-STPS-2008 | Safety colors: red stop, yellow caution, green safe, blue mandatory [48] | Red mushroom e-stop; tower green = running, amber = paused or full, red = fault/e-stop; yellow zone marking |
| NOM-029-STPS-2011 | Safe electrical maintenance, lockout | Main fuse, one fuse per branch, lockable e-stop; maintenance only with battery disconnected |
| NOM-035-STPS-2018 | Psychosocial risk factors, including job insecurity | Communicate early that the robot reassigns work; involve cleaning staff |
| NOM-052-SEMARNAT-2005 and LGPGIR | Hazardous-waste classification and authorized disposal; used oil requires a management plan [50] | Two separate labeled streams to authorized handlers; lead-acid battery returned for recycling |
| ISO 12100:2010 | Hazard identification, risk estimation and reduction | Method for the ten protection terms |
| ISO 3691-4:2023 | Speed, personnel detection, braking, e-stop, zones | ≤ 0.38 m/s, LiDAR + bumpers, cleared zone |
| ISO 13850:2015 and IEC 60204-1 | E-stop overrides all functions; deliberate reset | Relay e-stop; card + button restart |
| ISO 13849-1:2023 | Performance level of safety functions | Safety functions in hardware; certified version would need a safety relay/PLC |
| IEC 60529 | IP code | IP54 electronics bay |
| ISO 45001:2018 | PDCA OH&S management | Robot logs feed plant OH&S indicators |

## National public-health strategies in the implementation methodology

| Step | Strategy (institution) | How it enters the deployment |
|---|---|---|
| 1 | ELSSA — Entornos Laborales Seguros y Saludables (IMSS, 2022) [51] | Include slip hazards and fluid exposure in the plant's ELSSA risk diagnosis; the robot is one control measure, measured by incidents before and after |
| 2 | PASST — Programa de Autogestión en Seguridad y Salud en el Trabajo (STPS, May 2024) [52] | Register the robot procedure (authorization, emptying, maintenance) in the safety management system and its internal audits |
| 3 | NOM-035 well-being policy (STPS) | Change-management plan: inform, train and involve cleaning staff to prevent job insecurity and rejection |
| 4 | LGPGIR management plans (SEMARNAT) | Deliver segregated oil and chips under the plant's management plan; record kg recovered per month |
| 5 | Workplace training obligation (LFT) | 30-min hands-on training for operators; refresher after any fault or near-miss |

## Ethical choices in engineering decisions

| Engineering decision | Ethical issue | Perspectives | Codes and laws | Our choice |
|---|---|---|---|---|
| Replace manual cleaning with a robot | Job loss vs removing a hazardous, tedious task | Owner: cost. Worker: job security. Union: employment terms. Society: safer work | LFT training obligation; NOM-035; NSPE: hold paramount the welfare of the public [53] | Design the robot as an assistant; recommend retraining and reassignment rather than layoffs |
| Hardware e-stop and safety devices vs lower cost | Cutting safety hardware would lower cost but shift risk to people | Student budget vs safety of future users | NOM-004-STPS; ISO 13850; IEEE Code [54] | Keep the relay e-stop, bumpers, fuses and force limit even though they add cost |
| Camera and RFID logs | Privacy: the camera could record workers; the RFID log identifies who started each cycle | Accountability needs to know who operated; workers may feel monitored | LFPDPPP (DOF 20 Mar 2025) [55] | Camera aimed at the floor; no image storage of people; log keeps operator ID and time with a privacy notice and limited retention |
| Performance claims | Over-claiming ("slip-free floor", "reusable oil") could mislead buyers and endanger users | Pressure to sell vs honesty about a prototype | NSPE: statements only in an objective and truthful manner [53] | Report only measured results; the first draft's absolute claims were removed |
| Waste destination | Cheaper illegal dumping would harm the environment and community | Plant cost vs environmental and legal responsibility | NOM-052-SEMARNAT-2005, LGPGIR [50] | Deliver both streams only to authorized handlers; recycle the battery |
| Autonomous operation | Who is responsible if the robot injures someone? | Designer, plant, operator and supervisor share responsibility | ISO 3691-4 (information for use); LFT | Cleared zones only, authorized start, clear manual, logs that support investigation |
| Accessibility of the interface | An English-only or text-heavy HMI would exclude operators | Corporate culture vs shop-floor reality | IEEE Code: treat all persons fairly [54] | Spanish interface, colors and icons; training without reading English |
| Software and design reuse | Using open-source software or others' designs without respecting licenses | Speed vs intellectual property | Open-source licenses; Ley Federal del Derecho de Autor | Use libraries under their licenses and credit all sources; repository under MIT |
| Use of AI tools | Authorship and accuracy of AI-assisted work | Speed vs responsibility for content | University academic-integrity rules; IEEE Code | AI output treated as a draft reviewed by the team; AI use disclosed (Appendix F) |

## Impact in the global, economic, environmental and social context

| Context | Relevant information | Implication for our solution |
|---|---|---|
| Global | Almost 200,000 professional service robots sold in 2024 (+9 %); professional cleaning robots exceeded 25,000 units (+34 %), floor cleaning being the main application; staff shortages are a key reason companies buy them [56] | Growing market and acceptance; our niche (oily industrial floors with waste separation) is not covered by typical commercial scrubbers |
| Economic (Mexico) | Manufacturing ≈ 20 % of GDP; Mexico is the 9th largest manufacturing exporter; 85.9 % of manufacturing exports go to the U.S. [44]; minimum wage +13 % in 2026 [40] | Nearshoring brings more machining plants; rising labor costs increase the value of the 2 h/day saved |
| Social (Mexico) | STPS/IMSS: 290,527 work accidents and 340 deaths in 2023 [45] | Removing oil and chips attacks an everyday cause of industrial accidents and supports NOM-001 compliance |
| Health | Metalworking fluids linked to dermatitis and respiratory disease [4] | Less manual contact with fluids and oil-soaked absorbent |
| Environmental | Used oil is hazardous waste [50]; each ton of recycled steel conserves ≈ 2,500 lb iron ore, 1,400 lb coal and 120 lb limestone [57]; segregated chips and oil keep more value [11] | Separation at the source turns ≈ 1.3 t/yr of chips per robot into recyclable scrap and avoids ≈ 2.6 t/yr of mixed hazardous waste |

## Conclusion of the impact analysis

The robot is economically viable for a plant that pays for hazardous-waste disposal and spends at least about 1 h a
day cleaning a machining area by hand: in the base case it pays back in 6.6 months and stays at or above break-even in
the pessimistic case. Socially, it removes slip hazards and tedious, hazardous work, but it directly affects cleaning
staff; the responsible deployment retrains them as operators and creates technician positions. Culturally, its
success depends on acceptance: workers must care for it, and the initial interest must not turn into apathy. The
design follows Mexican STPS and SEMARNAT standards and international machine-safety standards, and its deployment is
built on national strategies (ELSSA, PASST, NOM-035). The main ethical choices — keeping people in the loop,
protecting privacy, keeping safety hardware despite its cost, reporting only measured results and delivering waste
only to authorized handlers — respond to the NSPE and IEEE codes and to Mexican law.
