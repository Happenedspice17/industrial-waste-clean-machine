# Engineering log — 2026-11-25 Talking points for final presentation v3

- **Problem:** Deck v3 has speaker notes per slide but no split by speaker; seven people present in a 10-minute slot.
- **Hypothesis:** One page per speaker (slides, time, opening, points, numbers, hand-off, likely questions) keeps the
  talk on time and keeps every number labelled as estimate, simulation or calculation.
- **Change:** New `docs/semester-1-deliverables/Talking_Points_Final_Presentation_v3.pdf` (9 pages, 10 after the update): running order
  (≈ 9:55), shared rules, Q&A routing table, one page per team member, hard questions and a key-numbers sheet.
  Slide split is a proposal (team order on the cover); the team can reassign.
- **Update (same day):** Speaker split changed at the team's request: María takes slide 2 (problem) and slide 10
  (Business Model Canvas); Juan Manuel takes slide 3; Franco opens (slide 1) and closes (slide 11). FMEA / DFMEA /
  SCCAF questions routed to Carlos with María as backup (both work with Ford's process). Problem and business
  framed as safety and waste, never as staff reduction (new shared rule and a "replace workers?" answer). 10 pages.
- **Evidence:** Content from deck v3 speaker notes, `risk/dfmea.csv`, `risk/sccaf.csv`, `docs/08-sccaf.md`, `docs/00-project-context.md` (§1–§12), ADR-0001…0004, 0006 and
  `docs/04-business.md`. No new numbers. Two paybacks kept apart: 6.6 months (owner, build cost) vs. ≈ 1.3 yr
  (customer, MXN 60 k price).
- **Reasoning:** Rule 4 (no claims without evidence): each speaker page has an "Avoid" box against presenting
  estimates or simulation as tests.
- **Result:** Documentation only; PDF rendered and checked visually (one page per speaker, glyphs OK).
- **Commits:** see branch `claude/clever-rubin-qbqid6`.
