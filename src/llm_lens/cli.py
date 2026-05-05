import time
from rich.console import Console
from llm_lens.core import track

console = Console()


@track
def fake_openai_call(prompt: str) -> str:
    time.sleep(0.12)
    return f"response to: {prompt}"


def main():
    console.print("[bold green]llm-lens[/bold green] is running!\n")
    result = fake_openai_call("what is 2+2?")
    console.print(f"got: {result}")
