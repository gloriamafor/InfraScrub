"""The shapes every part of InfraScrub agrees on.

A check produces Findings. The report renders Findings. Nothing else is shared,
so if you keep this file stable you can change anything on either side.
"""

from enum import Enum

from pydantic import BaseModel, Field


class Category(str, Enum):
    COST = "cost"
    SECURITY = "security"


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Finding(BaseModel):
    """One problem on one resource, plus how to fix it."""

    check_id: str = Field(description="Which check produced this, e.g. 'unattached-ebs'")
    category: Category
    severity: Severity
    title: str = Field(description="One line a human reads first")
    resource_id: str = Field(description="The AWS id: vol-..., i-..., sg-..., bucket name")
    region: str
    detail: str = Field(description="Why this is a finding, with the numbers that prove it")
    remediation: str = Field(description="The exact CLI command or console steps to fix it")
    monthly_cost_usd: float | None = Field(
        default=None, description="Estimated monthly waste. Cost checks set this; security checks leave it None"
    )


class ScanSummary(BaseModel):
    """The headline numbers at the top of every report."""

    total_findings: int
    monthly_waste_usd: float
    critical_exposures: int

    @classmethod
    def from_findings(cls, findings: list[Finding]) -> "ScanSummary":
        return cls(
            total_findings=len(findings),
            monthly_waste_usd=round(sum(f.monthly_cost_usd or 0.0 for f in findings), 2),
            critical_exposures=sum(1 for f in findings if f.severity == Severity.CRITICAL),
        )
