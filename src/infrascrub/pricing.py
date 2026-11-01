"""Price table for cost estimates.

v1 uses a bundled table instead of the AWS Pricing API (slow, complex, and
needs its own IAM permission). These are us-east-1 on-demand list prices and
are good enough to rank findings. Refresh them when you touch this file; the
source is https://aws.amazon.com/ebs/pricing/ and friends.

Last checked: 2026-11-01
"""

# USD per GB-month, by EBS volume type
EBS_GB_MONTH: dict[str, float] = {
    "gp3": 0.08,
    "gp2": 0.10,
    "io1": 0.125,
    "io2": 0.125,
    "st1": 0.045,
    "sc1": 0.015,
    "standard": 0.05,
}

# USD per GB-month for EBS snapshots (standard tier)
SNAPSHOT_GB_MONTH = 0.05

# USD per hour for an Elastic IP that is allocated but not attached to a running instance
ELASTIC_IP_IDLE_HOUR = 0.005

HOURS_PER_MONTH = 730


def ebs_volume_monthly(volume_type: str, size_gb: int) -> float:
    rate = EBS_GB_MONTH.get(volume_type, EBS_GB_MONTH["gp2"])
    return round(rate * size_gb, 2)
