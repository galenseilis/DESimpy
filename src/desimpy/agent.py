"""Simulation agent class."""

from abc import ABC


class Agent(ABC):  # pylint: disable=R0903
    """Base class for all simulation-compatible agents."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"
