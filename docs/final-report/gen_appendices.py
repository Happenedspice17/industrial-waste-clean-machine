"""Generate appendices C (requirements), D (glossary) and E (history) from the repository sources.

Run from docs/final-report/ (build.sh does it). The output files are overwritten on every build so the report never
drifts from requirements.yaml, docs/07-glossary.md, CHANGELOG.md and docs/engineering-log/.
"""

import re
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "chapters"


def cell(text: object) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def appendix_c() -> str:
    data = yaml.safe_load((ROOT / "requirements/requirements.yaml").read_text(encoding="utf-8"))
    lines = [
        "# Appendix C · Requirements: full text {.unnumbered}",
        "",
        "Generated from `requirements/requirements.yaml` (single source of truth). Status values: draft → approved →"
        " verified; a requirement is verified only when its test report is committed.",
        "",
        "## C.1 Stakeholder requirements {.unnumbered}",
        "",
        "| ID | Requirement | Importance (1-10) |",
        "|---|---|:-:|",
    ]
    lines += [f"| {r['id']} | {cell(r['text'])} | {r['importance']} |" for r in data["stakeholder"]]
    lines += ["", "## C.2 System requirements {.unnumbered}", ""]
    for r in data["system"]:
        lines += [
            f"### {r['id']} · parent {r['parent']} · module {r['module']} · {r['priority']} {{.unnumbered}}",
            "",
            f"> {r['text']}",
            "",
            "| Field | Value |",
            "|---|---|",
            f"| Rationale | {cell(r.get('rationale', ''))} |",
        ]
        if r.get("standard"):
            lines.append(f"| Standard | {cell(r['standard'])} |")
        lines += [
            f"| Verification | {cell(r['verification'])} |",
            f"| Acceptance | {cell(r['acceptance'])} |",
            f"| Status | {cell(r['status'])} |",
            f"| Verified by | {cell(', '.join(r.get('verified_by') or []) or '—')} |",
            "",
        ]
    return "\n".join(lines)


def shift_headings(md: str, by: int) -> str:
    return re.sub(r"^(#+) ", lambda m: "#" * (len(m.group(1)) + by) + " ", md, flags=re.M)


def appendix_d() -> str:
    src = (ROOT / "docs/07-glossary.md").read_text(encoding="utf-8")
    body = src.split("\n", 1)[1]  # drop the source title
    body = re.sub(r"^## (.+)$", r"## \1 {.unnumbered}", body, flags=re.M)
    return "# Appendix D · Glossary and project lingo {.unnumbered}\n\nFrom `docs/07-glossary.md`.\n" + body


def appendix_e() -> str:
    lines = [
        "# Appendix E · Change history and engineering log {.unnumbered}",
        "",
        "## E.1 Engineering log entries {.unnumbered}",
        "",
        "One entry per stage in `docs/engineering-log/` (problem, hypothesis, change, evidence, reasoning, result,"
        " commits).",
        "",
        "| Date | Entry |",
        "|---|---|",
    ]
    for f in sorted((ROOT / "docs/engineering-log").glob("20*.md")):
        title = f.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        title = re.sub(r"^Engineering log\s*[—-]\s*\d{4}-\d{2}-\d{2}\s*", "", title)
        lines.append(f"| {f.name[:10]} | {cell(title)} |")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8").split("\n", 1)[1]
    changelog = re.sub(
        r"^(#{2,}) (.+)$", lambda m: m.group(1) + "# " + m.group(2) + " {.unnumbered}", changelog, flags=re.M
    )
    lines += ["", "## E.2 Changelog {.unnumbered}", "", "From `CHANGELOG.md`.", changelog]
    return "\n".join(lines)


if __name__ == "__main__":
    (OUT / "23-appendix-c-requirements.md").write_text(appendix_c() + "\n", encoding="utf-8")
    (OUT / "24-appendix-d-glossary.md").write_text(appendix_d() + "\n", encoding="utf-8")
    (OUT / "25-appendix-e-history.md").write_text(appendix_e() + "\n", encoding="utf-8")
    print("appendices C, D, E generated")
