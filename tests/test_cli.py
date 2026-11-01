"""End-to-end: the whole scan path from session to summary."""

from infrascrub.cli import run_scan
from infrascrub.models import ScanSummary
from tests.conftest import REGION


def test_run_scan_produces_summary(aws):
    ec2 = aws.client("ec2", region_name=REGION)
    ec2.create_volume(AvailabilityZone=f"{REGION}a", Size=50, VolumeType="gp2")
    ec2.create_volume(AvailabilityZone=f"{REGION}a", Size=20, VolumeType="gp3")

    findings = run_scan(aws, [REGION])
    summary = ScanSummary.from_findings(findings)

    assert summary.total_findings == 2
    assert summary.monthly_waste_usd == 6.6  # 50*0.10 + 20*0.08
    assert summary.critical_exposures == 0
