"""Terminal output. Headline first, then one row per finding, then the fixes."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from infrascrub.models import Finding, ScanSummary, Severity

SEVERITY_STYLE = {
    Severity.CRITICAL: "bold red",
    Severity.HIGH: "red",
    Severity.MEDIUM: "yellow",
    Severity.LOW: "dim",
}

SEVERITY_ORDER = [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]


def render(findings: list[Finding], console: Console | None = None) -> None:
    console = console or Console()
    summary = ScanSummary.from_findings(findings)

    console.print(
        Panel(
            f"[bold]${summary.monthly_waste_usd:,.2f}/month wasted[/bold]  ·  "
            f"[bold]{summary.critical_exposures} critical exposures[/bold]  ·  "
            f"{summary.total_findings} findings",
            title="InfraScrub",
            expand=False,
        )
    )

    if not findings:
        console.print("[green]Nothing to fix. Clean account.[/green]")
        return

    ordered = sorted(
        findings,
        key=lambda f: (SEVERITY_ORDER.index(f.severity), -(f.monthly_cost_usd or 0)),
    )

    table = Table(show_lines=False, pad_edge=False)
    table.add_column("Severity")
    table.add_column("Finding")
    table.add_column("Resource")
    table.add_column("Region")
    table.add_column("$/month", justify="right")

    for f in ordered:
        cost = f"{f.monthly_cost_usd:,.2f}" if f.monthly_cost_usd is not None else ""
        table.add_row(
            f"[{SEVERITY_STYLE[f.severity]}]{f.severity.value}[/]",
            f.title,
            f.resource_id,
            f.region,
            cost,
        )
    console.print(table)

    console.print("\n[bold]How to fix[/bold]")
    for f in ordered:
        console.print(f"\n[dim]{f.resource_id}[/dim]  {f.detail}")
        for line in f.remediation.splitlines():
            console.print(f"  [cyan]$ {line}[/cyan]")
