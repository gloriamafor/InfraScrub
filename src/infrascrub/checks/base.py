"""What every check looks like.

A check is a class with three class attributes and one method. It reads from
the Inventory (never from boto3 directly) and returns Findings. That is the
whole contract. If a check needs data the Inventory does not have yet, add a
method to Inventory first.
"""

from abc import ABC, abstractmethod

from infrascrub.inventory import Inventory
from infrascrub.models import Category, Finding


class Check(ABC):
    id: str  # kebab-case, unique, shows up in reports: "unattached-ebs"
    category: Category
    title: str  # what the reader sees: "Unattached EBS volume"

    @abstractmethod
    def run(self, inventory: Inventory, region: str) -> list[Finding]:
        """Return one Finding per affected resource in this region. Empty list if none."""
