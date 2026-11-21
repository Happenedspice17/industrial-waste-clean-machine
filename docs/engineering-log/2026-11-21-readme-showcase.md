# Engineering log — 2026-11-21 README showcase (sumo-v-ia style)

- **Problem:** README did not show the validation work (DFMEA, SCCAF, WCCA, DFMA, economics) that makes the project
  stand out.
- **Change:** README restyled after the team's sumo-v-ia README: centered header, badges, concept image, status,
  team, documentation, problem, flow and state diagrams, architecture, modules, validation toolkit (DFMEA top risks,
  SCCAF table, WCCA table, DFMA, economics), decisions (ADR-0001–0006), coverage simulation image, validated vs
  pending, inherited lessons, layout, setup, workflow, roadmap, credits. Images extracted from the final
  presentation into `docs/img/`.
- **Evidence:** Every number copied from `tools/fmea.py`, `tools/wcca.py`, `tools/dfma.py`, `tools/econ.py` outputs
  and `docs/00-project-context.md`, with its evidence label; links checked; `python tools/check_all.py` passes.
- **Result:** Documentation only. Tables must be refreshed when DFMEA/SCCAF/WCCA change (lesson 17).
- **Commits:** branch `docs/readme-showcase`.
