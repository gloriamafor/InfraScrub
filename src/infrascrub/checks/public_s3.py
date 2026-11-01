"""Your second security check: an S3 bucket the public can read.

Two things make a bucket public: a bucket policy that grants "*" access, or
Public Access Block being turned off with a public ACL. The simplest reliable
signal for v1 is Public Access Block: if any of its four flags is False, flag
the bucket.

Calls you need (add a method to Inventory for the first one; the second is a
per-bucket call you make inside the check):

    s3.list_buckets()["Buckets"]                            -> [{"Name": "..."}]
    s3.get_public_access_block(Bucket=name)                 -> {"PublicAccessBlockConfiguration": {
                                                                  "BlockPublicAcls": bool,
                                                                  "IgnorePublicAcls": bool,
                                                                  "BlockPublicPolicy": bool,
                                                                  "RestrictPublicBuckets": bool}}

get_public_access_block raises a ClientError with code
"NoSuchPublicAccessBlockConfiguration" when nothing is configured. Treat that
as all four flags False.

Fix command:

    aws s3api put-public-access-block --bucket NAME --public-access-block-configuration \
      BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

Note: S3 is global. This check should only run once, not once per region.
Look at how cli.py calls checks and decide how to handle that. (Hint: a
class attribute `global_scope = True` on the check, and cli.py only runs it
for the first region.)

Steps (build guide, step 8).
"""

from infrascrub.checks.base import Check
from infrascrub.inventory import Inventory
from infrascrub.models import Category, Finding


class PublicS3(Check):
    id = "public-s3-bucket"
    category = Category.SECURITY
    title = "S3 bucket allows public access"

    def run(self, inventory: Inventory, region: str) -> list[Finding]:
        raise NotImplementedError("Build guide, step 8")
