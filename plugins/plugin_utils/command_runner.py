"""Definitions for the command runner."""
import subprocess
import threading

from dataclasses import dataclass, field
from queue import Queue
from typing import Callable, Dict, List, Optional, TypeVar, Union


T = TypeVar("T")
JSONTypes = Union[bool, int, str, Dict, List]


@dataclass(frozen=False)
class Command:
    """Data structure for details of a command to be run.

    A ``Command`` is updated after instantiated with details from either
    ``stdout`` or ``stderr``.
    """

    # pylint: disable=too-many-instance-attributes
    identity: str
    command: str
    parse: Optional[Callable[["Command"], None]] = None
    return_code: int = -1
    stdout: str = ""
    stderr: str = ""
    details: Union[List[str], Dict[str, JSONTypes], str] = ""
    errors: List[str] = field(default_factory=list)

    @property
    def stderr_lines(self) -> List[str]:
        """Produce a list of stderr lines.

        :returns: A list of stderr lines
        """
        return self.stderr.splitlines()

    @property
    def stdout_lines(self) -> List[str]:
        """Produce a list of stdout lines.

        :returns: A list of stdout lines
        """
        return self.stdout.splitlines()


def run_command(command: Command) -> None:
    """Run a command using subprocess.

    :param command: Details of the command to run
    """
    try:
        proc_out = subprocess.run(
            command.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            universal_newlines=True,
            shell=True,
        )

        command.return_code = proc_out.returncode
        command.stdout = proc_out.stdout
        command.stderr = proc_out.stderr
    except subprocess.CalledProcessError as exc:
        command.stderr = str(exc.stderr)
        command.errors = [str(exc.stderr)]


def worker(pending_queue: Queue[Optional[Command]], completed_queue: Queue[Command]) -> None:
    """Run a command from pending, parse, and place in completed.

    :param pending_queue: A queue with plugins to process
    :param completed_queue: The queue in which extracted documentation will be placed
    """
    while True:
        command = pending_queue.get()
        if command is None:
            break
        run_command(command)
        if command.parse:
            try:
                command.parse(command)
            except Exception as exc:  # pylint: disable=broad-except
                command.errors = command.errors + [str(exc)]
        completed_queue.put(command)


class CommandRunner:
    """A command runner.

    Run commands using single or multiple processes.
    """

    def __init__(self) -> None:
        """Initialize the command runner."""
        self._completed_queue: Queue[Optional[Command]] = Queue()
        self._pending_queue: Queue[Optional[Command]] = Queue()

    def run_multi_thread(self, commands: List[Command]) -> List[Optional[Command]]:
        """Run commands with multiple threads.

        Workers are started to read from pending queue.
        Exit when the number of results is equal to the number
        of commands needing to be run.

        :param commands: All commands to be ru
        :returns: The results from running all commands
        """
        self.start_workers(commands)
        results: List[Optional[Command]] = []
        while len(results) != len(commands):
            results.append(self._completed_queue.get())
        return results

    def start_workers(self, jobs: List[Command]) -> None:
        """Start workers and submit jobs to pending queue.

        :param jobs: The jobs to be run
        """
        worker_count = len(jobs)
        processes = []
        for _proc in range(worker_count):
            proc = threading.Thread(
                target=worker,
                args=(self._pending_queue, self._completed_queue),
            )
            processes.append(proc)
            proc.start()
        for job in jobs:
            self._pending_queue.put(job)
        for _proc in range(worker_count):
            self._pending_queue.put(None)
        for proc in processes:
            proc.join()
