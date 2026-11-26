# Appendix F · Credits and use of AI tools {.unnumbered}

**Authors.** The design, requirements, component selection, calculations, simulations, course deliverables and every
engineering decision belong to the seven team members listed on the cover, under the supervision of
Dr. Hiram Eredín Ponce Espinosa. The team is responsible for all content of this report and of the repository.

**Prior work.** The lessons learned, the MCU/Linux split and the vision approach come from the team's previous Arduino
UNO Q robot, a maze solver for *Microcontroladores 2* (second place) [77].

**AI assistance.** Since August 2026 the team has used **Claude** (Anthropic) [79] as a chat assistant during the
design phase. In November 2026 the team started using **Claude Code** (Anthropic) [78] on the repository. Under the
team's direction it set up the repository from the team's kit, translated the Spanish deliverables to English,
drafted ADR-0006 (vision role) from the maze-robot history, requirements SR-015–SR-017, test protocol TP-V01, the
glossary, the internal SCCAF and its check in `tools/fmea.py`, the README and the cybersecurity agent, the AprilTag
bench app (ADR-0007, TP-V02, threat model), the ten-slide final presentation with the IEEE 7000 EVRs, and the
compilation and typesetting of this report from the repository and the course deliverables. Commits it helped write
carry a `Co-Authored-By: Claude` trailer.

**Rules for AI output in this project.**

- AI output is a draft: a team member reviews every change before it is merged or submitted.
- Numbers keep their evidence label (estimate, calculation, simulation, measured); AI never turns a simulation into a
  test result.
- Safety functions, thresholds and sign-offs (SCCAF, test reports) are decided and approved by people.

**License.** Repository released under the MIT License. Third-party libraries (OpenCV, NumPy, PyYAML, pytest, ruff)
are used under their own licenses.
