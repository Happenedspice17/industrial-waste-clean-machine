# Engineering log — 2026-11-25 Talking points for final presentation v3

- **Problem:** Deck v3 has speaker notes per slide but no split by speaker; seven people present in a 10-minute slot.
- **Hypothesis:** One page per speaker (slides, time, opening, points, numbers, hand-off, likely questions) keeps the
  talk on time and keeps every number labelled as estimate, simulation or calculation.
- **Change:** New `docs/semester-1-deliverables/Talking_Points_Final_Presentation_v3.pdf` (9 pages): running order
  (≈ 9:55), shared rules, Q&A routing table, one page per team member, hard questions and a key-numbers sheet.
  Slide split is a proposal (team order on the cover); the team can reassign.
- **Evidence:** Content from deck v3 speaker notes, `docs/00-project-context.md` (§1–§12), ADR-0001…0004, 0006 and
  `docs/04-business.md`. No new numbers. Two paybacks kept apart: 6.6 months (owner, build cost) vs. ≈ 1.3 yr
  (customer, MXN 60 k price).
- **Reasoning:** Rule 4 (no claims without evidence): each speaker page has an "Avoid" box against presenting
  estimates or simulation as tests.
- **Result:** Documentation only; PDF rendered and checked visually (one page per speaker, glyphs OK).
- **Commits:** see branch `claude/clever-rubin-qbqid6`.
