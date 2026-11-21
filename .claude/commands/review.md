---
description: Pre-PR review (code safety, traceability, git hygiene, docs)
---
Run in parallel: `embedded-safety-reviewer` on changed code, `git-gatekeeper` on the branch, and check that docs and
requirements were updated. Then run `python tools/check_all.py`. Output one ranked findings list and the filled PR
description from `.github/pull_request_template.md`. Do not commit.
