import asyncio
from typing import List, AsyncGenerator
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from collections import deque
from funcchain import achain


async def run_subprocess(
    command: List[str], layout: Layout, buffer: deque[str]
) -> None:
    """Run the subprocess and update the left panel."""
    layout["left"].update(Panel("Initializing ...", title="Coder", border_style="blue"))
    process = await asyncio.create_subprocess_exec(
        *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
    )

    assert process.stdout is not None
    async for line in process.stdout:
        decoded_line = line.decode().strip()
        buffer.append(decoded_line)
        layout["left"].update(
            Panel("\n".join(buffer), title="Coder", border_style="blue")
        )
        await asyncio.sleep(0)

    await process.wait()


async def right_panel(layout: Layout, buffer: deque[str], task: str) -> None:
    """Print buffer content to the right panel."""
    async for chunk in read_left_output(buffer):
        layout["right"].update(
            Panel(
                "\n".join(await supervisor(chunk, task)),
                title="Superviser",
                border_style="green",
            )
        )
        await asyncio.sleep(0.5)


async def supervisor(observation: str, task: str) -> tuple[str, str]:
    """
    Supervise the software developer implementing the task.
    Respond with a tuple of the healthyness and a summary of the current state.
    """
    return await achain()


async def read_left_output(buffer: deque[str]) -> AsyncGenerator[List[str], None]:
    """Read the console output of the left terminal as an async generator."""
    while True:
        chunk: List[str] = []
        while buffer and len(chunk) < 10:
            chunk.append(buffer.popleft())
        if chunk:
            yield chunk
        else:
            await asyncio.sleep(0.1)


async def main() -> None:
    import sys

    if len(sys.argv) < 2:
        print("Usage: python main.py <task>")
        sys.exit(1)
    task: str = sys.argv[1]
    console = Console()
    layout = Layout()
    layout.split_row(Layout(name="left", ratio=1), Layout(name="right", ratio=1))
    buffer: deque[str] = deque()

    with Live(layout, console=console, screen=True, refresh_per_second=4):
        subprocess_task = asyncio.create_task(
            run_subprocess(
                [
                    "aider",
                    "--sonnet",
                    "--no-auto-commits",
                    "--map-tokens",
                    "2048",
                    "--yes",
                    "--message",
                    task + " always focus on the test_codebase",
                ],
                layout,
                buffer,
            )
        )
        console_task = asyncio.create_task(right_panel(layout, buffer, task))

        await asyncio.gather(subprocess_task, console_task)


if __name__ == "__main__":
    asyncio.run(main())
