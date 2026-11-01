"""Your first security check: a security group open to the whole internet.

A security group rule with CidrIp "0.0.0.0/0" (or CidrIpv6 "::/0") on an
inbound port lets anyone on the internet reach it. On port 22 (SSH) or 3389
(RDP) that is critical. On 80/443 it is normal for a web server, so skip those.

What you need to know about the data shape (from describe_security_groups):

    group["GroupId"]                      -> "sg-0abc..."
    group["IpPermissions"]                -> list of inbound rules
    rule["FromPort"], rule["ToPort"]      -> port range (missing when IpProtocol is "-1", meaning all)
    rule["IpRanges"]                      -> list of {"CidrIp": "..."}
    rule["Ipv6Ranges"]                    -> list of {"CidrIpv6": "..."}

Fix command for one rule:

    aws ec2 revoke-security-group-ingress --group-id sg-... --protocol tcp --port 22 --cidr 0.0.0.0/0 --region us-east-1

Steps (build guide, step 7):
    a. implement Inventory.security_groups first
    b. loop groups, loop rules, loop IpRanges; flag CidrIp == "0.0.0.0/0" unless port is 80 or 443
    c. severity: CRITICAL for 22, 3389, or all ports (-1); HIGH for anything else
    d. one Finding per open rule, resource_id = the GroupId
    e. write tests/test_open_security_groups.py, then register the check in checks/__init__.py
"""

from infrascrub.checks.base import Check
from infrascrub.inventory import Inventory
from infrascrub.models import Category, Finding


class OpenSecurityGroups(Check):
    id = "open-security-group"
    category = Category.SECURITY
    title = "Security group open to the internet"

    def run(self, inventory: Inventory, region: str) -> list[Finding]:
        raise NotImplementedError("Build guide, step 7")
