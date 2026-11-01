"""Worked example: an EBS volume nobody is using.

Read this file top to bottom before writing your own check. Every check you
write will have the same four parts:

    1. ask the Inventory for the resources
    2. decide which ones are a problem
    3. work out the impact (dollars or severity)
    4. write the exact fix command

An EBS volume whose State is "available" is not attached to any instance.
You pay for it every month anyway.
"""

from infrascrub import pricing
from infrascrub.checks.base import Check
from infrascrub.inventory import Inventory
from infrascrub.models import Category, Finding, Severity


class UnattachedEbs(Check):
    id = "unattached-ebs"
    category = Category.COST
    title = "Unattached EBS volume"

    def run(self, inventory: Inventory, region: str) -> list[Finding]:
        findings: list[Finding] = []

        # 1. get the resources
        for volume in inventory.ebs_volumes(region):
            # 2. is it a problem?
            if volume["State"] != "available":
                continue

            # 3. impact
            volume_id = volume["VolumeId"]
            size_gb = volume["Size"]
            volume_type = volume.get("VolumeType", "gp2")
            monthly = pricing.ebs_volume_monthly(volume_type, size_gb)

            # 4. the fix. Snapshot first so the user can undo it.
            remediation = (
                f"aws ec2 create-snapshot --volume-id {volume_id} --region {region} "
                f"--description 'infrascrub backup before delete'\n"
                f"aws ec2 delete-volume --volume-id {volume_id} --region {region}"
            )

            findings.append(
                Finding(
                    check_id=self.id,
                    category=self.category,
                    severity=Severity.MEDIUM,
                    title=self.title,
                    resource_id=volume_id,
                    region=region,
                    detail=f"{size_gb} GB {volume_type} volume is not attached to any instance.",
                    remediation=remediation,
                    monthly_cost_usd=monthly,
                )
            )

        return findings
