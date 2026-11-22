# Engineering log — 2026-11-22 Final presentation v2 (10 slides, IEEE 7000 EVRs)

- **Problem:** The final presentation had 19 dense slides; the course asks for ≤ 10 min and the proposal structure
  (proposal, design analysis, theory, conceptual design, next steps). The IEEE 7000-2021 ethical-design template
  asked for ethical value requirements (EVRs).
- **Change:** New `docs/semester-1-deliverables/Final_Presentation_Waste_Robot_v2.pptx`: 10 slides with speaker
  notes (≈ 30 s–1 min 15 s each). Figures reused from the improved proposal (goal tree, black box, white boxes A/B,
  concept sketch) and the coverage simulation. Requirements slide adds EVR-01 worker safety, EVR-02 environmental
  responsibility, EVR-03 privacy and accountability, the value conflict (coverage speed vs. safety → safety prevails)
  and the stakeholder list.
- **Evidence:** All numbers copied from `docs/00-project-context.md` and the improved proposal with their labels
  (estimate / simulation); no physical test claimed. File validated with the pptx schema checker and rendered for
  visual QA.
- **Result:** Documentation only. EVRs are a team draft (deduced from existing SR/protection terms); they are not
  yet in `requirements/requirements.yaml` — add them with `/req` once the team approves.
- **Commits:** branch `claude/elegant-bardeen-eyqw0a`.
- **Update (same day):** slides simplified to reference style (short phrases, redrawn goal tree and black/white boxes); detail moved to speaker notes.
