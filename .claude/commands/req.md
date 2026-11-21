---
description: Create or refine a requirement with traceability (R → SR → test)
argument-hint: <feature or need in plain words>
---
Use the `requirements-engineer` subagent to turn this need into one or more singular, verifiable system requirements:

$ARGUMENTS

Add them to `requirements/requirements.yaml` (status: draft), link parent R1–R10, propose verification method and
acceptance criterion, list TBD measurements, then run `python tools/check_traceability.py` and report.
