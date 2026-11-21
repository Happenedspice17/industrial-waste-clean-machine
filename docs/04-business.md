# 04 · Business and evaluation artifacts

## Business Model Canvas (proposed, validate with customers)

| Block | Content |
|---|---|
| Key partners | Component suppliers in Mexico (UNIT, Sandorobotics, Steren); authorized waste handlers; scrap recyclers; university labs |
| Key activities | Design, assembly, firmware; commissioning + route mapping; maintenance and support |
| Key resources | Robot design and software; engineering team; local supply chain |
| Value proposition | Clean floor every shift change; oil and chips in two separate streams; no worker contact with fluids; ≈ 1/30 price of an autonomous scrubber |
| Customer relationships | Plant pilot before purchase; operator training; service plan with visits |
| Channels | Direct B2B sales; automation distributors; industrial trade fairs |
| Customer segments | Machining shops; auto-parts suppliers Tier 1/2; Bajío, Estado de México, Nuevo León; buyers: EHS and maintenance managers |
| Cost structure | Unit ≈ MXN 31.6k (parts, assembly, commissioning); service ≈ 6.7k/yr per robot; development ≈ 75.6k one-time |
| Revenue streams | Robot ≈ MXN 60k (47 % margin); service ≈ 1.5k/month; rental option; customer payback ≈ 1.3 yr |

## Economic evaluation

Reproduce with `python tools/econ.py` (parameters and results in `docs/00-project-context.md` §9). Rubric
expectations used in class: explicit calculations shown separately; realistic parameters with sources; no missing
costs (hardware, tooling, contingency, assembly, commissioning, energy, battery, consumables, maintenance, operator
time, oil collection, residual hazardous waste, NRE share); scenarios and sensitivity (tornado).

## Other business/design tools used in the course (templates in `docs/templates/`)

- SWOT (strengths/weaknesses internal; opportunities/threats external).
- Technological impact matrix: economic (calculations, viability), social, cultural (dimensions in problem solving,
  cultural empathy), safety & health (national/international regulations, national public-health strategies: IMSS
  ELSSA, STPS PASST, NOM-035), ethical (decisions, perspectives, codes NSPE/IEEE, laws incl. LFPDPPP 2025), impact
  (global, economic, environmental, social context).
- Goal tree (logical framework): means → specific objectives → general objective → ends → end.
- Quality matrix (house of quality 0/1/3/9) and pairwise comparison (AHP-style).
- Black box / white boxes (functional and component), morphological matrix, scenario analysis (idealist/pessimist,
  protection terms, metrics, evaluation, strengths/weaknesses).
- Value proposition canvas and Lean Canvas (templates provided for next semester's customer interviews).
