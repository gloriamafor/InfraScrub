# InfraScrub

Scan an AWS account for wasted spend and security exposures. One report, both problems, and the exact command to fix each finding.

```
$ infrascrub scan -r us-east-1

╭──────────────────── InfraScrub ────────────────────╮
│ $248.00/month wasted  ·  2 critical exposures  ·  9 findings │
╰─────────────────────────────────────────────────────╯
```

Read-only. InfraScrub never changes anything in your account; it tells you what to run.

## Install

```bash
pip install infrascrub
```

Or from source:

```bash
git clone https://github.com/gloriamafor/ProjectGetOut.git
cd ProjectGetOut
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Use

```bash
infrascrub scan                              # default region, default credentials
infrascrub scan -r us-east-1 -r eu-west-1    # several regions
infrascrub scan --profile work -o json --out scan.json
infrascrub checks                            # list what runs
```

Credentials come from the normal AWS CLI chain (`~/.aws/credentials`, `AWS_PROFILE`, environment variables). The IAM policy in [`iam/infrascrub-readonly.json`](iam/infrascrub-readonly.json) is everything InfraScrub needs.

## Checks

| ID | Category | What it finds |
| --- | --- | --- |
| `unattached-ebs` | cost | EBS volumes not attached to any instance |

More are on the way. See the build guide for the order.

## How it is built

```
src/infrascrub/
  inventory.py      the only file that calls AWS; one call per API per region, cached
  checks/           one file per check; reads the inventory, returns Findings
  models.py         Finding and ScanSummary, the shapes everything shares
  pricing.py        bundled price table for cost estimates
  report/           terminal and JSON output
  cli.py            the `infrascrub` command
tests/              moto-backed tests, one file per check
iam/                the read-only policy
```

Adding a check: copy `checks/unattached_ebs.py`, change the four parts (get resources, decide, impact, fix), write its test, register it in `checks/__init__.py`.

## Develop

```bash
pytest -q          # run tests
ruff check src tests
```

## License

MIT
