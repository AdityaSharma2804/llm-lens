import time
from rich.console import Console
from rich.table import Table
from llm_lens.core import track, get_records

console = Console()


@track
def fake_openai_call(prompt: str) -> str:
    time.sleep(0.12)
    return f"response to: {prompt}"


@track
def failing_call():
    time.sleep(0.05)
    raise ConnectionError("API unreachable")


def main():
    console.print("[bold green]llm-lens[/bold green] is running!\n")

    # calls karo
    fake_openai_call("what is 2+2?")
    fake_openai_call("explain recursion")
    try:
        failing_call()
    except ConnectionError:
        pass

    # records fetch karo
    records = get_records()

    # rich table mein dikhao
    table = Table(title="Tracked Calls")
    table.add_column("Function", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Latency (ms)", justify="right")
    table.add_column("Error")
    table.add_column("Timestamp")

    for r in records:
        status_color = "green" if r.status == "ok" else "red"
        table.add_row(
            r.func_name,
            f"[{status_color}]{r.status}[/{status_color}]",
            str(r.latency_ms),
            r.error or "-",
            r.timestamp,
        )

    console.print(table)
    console.print(f"\n[bold]Total calls:[/bold] {len(records)}")

    