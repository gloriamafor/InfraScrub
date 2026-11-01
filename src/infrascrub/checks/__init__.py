"""The registry. A check only runs if it is listed here.

When you finish a check, import it and add it to ALL_CHECKS. Keep the stubs
out until they pass their tests, or `infrascrub scan` will crash.
"""

from infrascrub.checks.base import Check
from infrascrub.checks.unattached_ebs import UnattachedEbs

ALL_CHECKS: list[type[Check]] = [
    UnattachedEbs,
    # OpenSecurityGroups,   <- add when step 7 is done
    # PublicS3,             <- add when step 8 is done
]
