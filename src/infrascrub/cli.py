"""The `infrascrub` command.

    infrascrub scan                       scan the default region with your default credentials
    infrascrub scan -r us-east-1 -r us-west-2
    infrascrub scan --profile work --output json --out scan.json
    infrascrub checks                     list the registered checks
"""

import json
from pathlib import Path

import boto3
import typer
from rich.console import Console

from infrascrub.checks import ALL_CHECKS
from infrascrub.inventory import Inventory
from infrascrub.models import Finding
from infrascrub.report import json_out, terminal

app = typer.Typer(help="Find wasted spend and security exposures in an AWS account, with the fix for each.")
console = Console()


def run_scan(session: boto3.Session, regions: list[str]) -> list[Finding]:
    """Run every registered check in every region. Kept separate from the CLI so tests can call it."""
    inventory = Inventory(session, regions)
    findings: list[Finding] = []
    for check_cls in ALL_CHECKS:
        check = check_cls()
        for region in regions:
            findings.extend(check.run(inventory, region))
    return findings


@app.command()
def scan(
    region: list[str] = typer.Option(None, "--region", "-r", help="Region to scan. Repeat for several."),
    profile: str = typer.Option(None, "--profile", help="AWS CLI profile name."),
    output: str = typer.Option("table", "--output", "-o", help="table or json"),
    out: Path = typer.Option(None, "--out", help="Write the report to this file instead of stdout."),
) -> None:
    """Scan an AWS account and print what to fix."""
    session = boto3.Session(profile_name=profile)
    regions = region or [session.region_name or "us-east-1"]

    with console.status(f"Scanning {', '.join(regions)}..."):
        findings = run_scan(session, regions)

    if output == "json":
        if out:
            json_out.write(findings, out)
            console.print(f"Wrote {len(findings)} findings to {out}")
        else:
            print(json.dumps(json_out.to_dict(findings), indent=2))
    else:
        terminal.render(findings, console)


@app.command()
def checks() -> None:
    """List the checks that will run."""
    for check_cls in ALL_CHECKS:
        console.print(f"[bold]{check_cls.id}[/bold]  ({check_cls.category.value})  {check_cls.title}")


if __name__ == "__main__":
    app()
