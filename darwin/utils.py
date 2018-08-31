from collections import deque
from functools import wraps


def recorded(method):

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._history.append((method.__name__, args, kwargs))
        return method(self, *args, **kwargs)

    return wrapper


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
        self._history = deque()

    def apply_changes(self, parent_list):
        """Apply the recorded changes on the given list."""

        for method, args, kwargs in self._history:
            getattr(parent_list, method)(*args, **kwargs)

    @recorded
    def append(self, obj):
        super().append(obj)

    @recorded
    def extend(self, iterable):
        super().extend(iterable)

    @recorded
    def pop(self, index=None):
        return super().pop(index)

    def clear(self):
        for element in self[:]:
            self.remove(element)

    @recorded
    def insert(self, index, obj):
        super().insert(index, obj)

    @recorded
    def remove(self, obj):
        super().remove(obj)

    def __delitem__(self, i):
        raise NotImplementedError("Low-level delitem is not supported.")
