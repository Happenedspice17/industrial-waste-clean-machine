---
description: Add an engineering log entry for the current stage
argument-hint: <stage or topic>
---
Use the `docs-writer` subagent. Create `docs/engineering-log/YYYY-MM-DD-<topic>.md` from `docs/templates/engineering-log.md` for:
$ARGUMENTS. Pull commits with `git log --oneline`, verify facts against code, mark "(deduced)" where needed.
