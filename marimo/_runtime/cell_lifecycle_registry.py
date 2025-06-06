# Copyright 2024 Marimo. All rights reserved.
from __future__ import annotations

import dataclasses

from marimo._runtime.cell_lifecycle_item import CellLifecycleItem
from marimo._types.ids import CellId_t


@dataclasses.dataclass
class CellLifecycleRegistry:
    registry: dict[CellId_t, set[CellLifecycleItem]] = dataclasses.field(
        default_factory=dict
    )

    def inject(self, cell_id: CellId_t, item: CellLifecycleItem) -> None:
        """Add a provisioned lifecycle item for a specific cell.

        Prefer using `add` to add lifecycle items.
        """
        if cell_id not in self.registry:
            self.registry[cell_id] = set()
        self.registry[cell_id].add(item)

    def add(self, item: CellLifecycleItem) -> None:
        """Add a lifecycle item for the currently running cell.

        Calls the item's create method upon adding. No-op if no cell
        is running.
        """
        from marimo._runtime.context import get_context

        ctx = get_context()

        cell_id = ctx.cell_id
        if cell_id is None:
            return

        item.create(ctx)
        return self.inject(cell_id, item)

    def dispose(self, cell_id: CellId_t, deletion: bool) -> None:
        """Dispose lifecycle items associated with `cell_id`

        Calls `dispose` hooks and clears items from the registry.

        If `deletion` is `True`, the cell is being removed from the graph.
        """
        from marimo._runtime.context import get_context

        ctx = get_context()
        # LifecycleItems can request that their `dispose` method is retried in
        # the next cell lifecycle; these items are persisted.
        persisted_lifecycle_items = set()
        if cell_id in self.registry:
            for lifecycle_item in self.registry[cell_id]:
                if not lifecycle_item.dispose(context=ctx, deletion=deletion):
                    persisted_lifecycle_items.add(lifecycle_item)

            if persisted_lifecycle_items:
                self.registry[cell_id] = persisted_lifecycle_items
            else:
                del self.registry[cell_id]
