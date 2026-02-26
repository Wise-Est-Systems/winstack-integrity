from __future__ import annotations
import re
import time
from dataclasses import dataclass, asdict
from typing import Any, Dict, List

FABRICATION_PATTERNS = [
    r"\bmake up\b",
    r"\bpretend\b",
    r"\bfake sources?\b",
    r"\bfabricate\b",
    r"\binvent\b",
    r"\bmake it look real\b",
]

RISK_PATTERNS = [
    (r"\bmedical\b|\bdiagnos(e|is)\b|\btreatment\b", "MEDICAL"),
    (r"\blegal\b|\blawsuit\b|\bsue\b|\bcontract\b", "LEGAL"),
    (r"\binvestment\b|\bstocks?\b|\bcrypto\b|\bfinancial advice\b", "FINANCE"),
]

FACT_LINE = re.compile(r"^\s*(FACT|FACTS)\s*:\s*", re.IGNORECASE)
SOURCE_TAG = re.compile(r"\[source:\s*.+?\]", re.IGNORECASE)

@dataclass(frozen=True)
class Decision:
    schema: str
    tool: str
    version: str
    created_utc: int
    decision: str   # ALLOW | HALT | FLAG
    reason: str
    signals: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

def evaluate_text(text: str, tool: str, version: str) -> Decision:
    lines = text.splitlines()
    signals: List[Dict[str, Any]] = []

    for pat in FABRICATION_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            signals.append({"code": "FABRICATION_PRESSURE", "severity": "HIGH", "pattern": pat})

    for pat, domain in RISK_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            signals.append({"code": "RISK_DOMAIN", "severity": "MED", "domain": domain})

    for i, line in enumerate(lines, start=1):
        if FACT_LINE.search(line) and not SOURCE_TAG.search(line):
            signals.append({"code": "UNSOURCED_FACT", "severity": "HIGH", "line": i})

    if any(s["code"] == "FABRICATION_PRESSURE" for s in signals):
        return Decision("truthlock.decision.v1", tool, version, int(time.time()), "HALT",
                        "Fabrication pressure detected.", signals)

    if any(s["code"] in ("UNSOURCED_FACT", "RISK_DOMAIN") for s in signals):
        return Decision("truthlock.decision.v1", tool, version, int(time.time()), "FLAG",
                        "Governance signals detected.", signals)

    return Decision("truthlock.decision.v1", tool, version, int(time.time()), "ALLOW",
                    "No blocking signals detected.", signals)
