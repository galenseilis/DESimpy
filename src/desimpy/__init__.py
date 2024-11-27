from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final


from .core import Event, EventScheduler

__all__: Final[list[str]] = ["Event", "EventScheduler"]
