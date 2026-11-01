"""JSON output, for piping into other tools or saving a scan to compare later."""

import json
from pathlib import Path

from infrascrub.models import Finding, ScanSummary


def to_dict(findings: list[Finding]) -> dict:
    return {
        "summary": ScanSummary.from_findings(findings).model_dump(),
        "findings": [f.model_dump(mode="json") for f in findings],
    }


def write(findings: list[Finding], path: Path) -> None:
    path.write_text(json.dumps(to_dict(findings), indent=2))
