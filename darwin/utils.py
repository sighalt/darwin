from collections import deque
from contextlib import suppress


class HistoryList(list):
    """List-like object which saves content changes for later application on
    another list.

    .. warning:
        The order of items is ignored and not kept track of.

    The intended use case is to keep track of changes on a slice of a greater
    'parent list'. With `apply_changes` the recorded changes can get executed on
    that 'parent list'.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._append_history = deque()
        self._remove_history = deque()
        self._was_cleared = False

    def apply_changes(self, parent_list):
        """Apply the recorded changes on the given list."""
        for obj_to_remove in self._remove_history:
            with suppress(ValueError):
                parent_list.remove(obj_to_remove)

        if self._was_cleared:
            parent_list.extend(self)
        else:
            parent_list.extend(self._append_history)

    def append(self, obj):
        self._append_history.append(obj)
        super().append(obj)

    def extend(self, iterable):
        self._append_history.extend(iterable)
        super().extend(iterable)

    def pop(self, index=None):
        element = super().pop(index)
        self._remove_history.append(element)
        return element

    def clear(self):
        self._remove_history.extend(self)
        super().clear()

    def insert(self, index, obj):
        self._append_history.append(obj)
        super().insert(index, obj)

    def remove(self, obj):
        self._remove_history.append(obj)
        super().remove(obj)
