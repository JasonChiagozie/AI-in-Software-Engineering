from typing import Any, Callable, Iterable, List, Sequence, Union

def sort_dicts(
    data: Sequence[dict],
    sort_key: Union[str, Iterable[str]],
    reverse: bool = False,
    missing: str = "last",
    key_func: Callable[[Any], Any] = None,
) -> List[dict]:
    """
    Return a new list of dictionaries sorted by a specific key.

    - data: sequence of dicts (input is not mutated).
    - sort_key: a single key name (str), a dotted path ("a.b.c"), or an iterable of keys for nested lookups.
    - reverse: sort descending when True.
    - missing: behavior for missing keys: "last" (default), "first", or "raise".
    - key_func: optional function applied to the extracted value before comparison.

    Examples:
        sort_dicts(list_of_dicts, "name")
        sort_dicts(list_of_dicts, "address.city")
        sort_dicts(list_of_dicts, ["address", "city"], missing="first")
    """
    if missing not in {"last", "first", "raise"}:
        raise ValueError('missing must be one of "last", "first", "raise"')

    # Normalize sort_key to a list of path segments
    if isinstance(sort_key, str) and "." in sort_key:
        key_path = tuple(sort_key.split("."))
    elif isinstance(sort_key, str):
        key_path = (sort_key,)
    else:
        key_path = tuple(sort_key)

    def _extract(d: dict):
        cur = d
        for k in key_path:
            if not isinstance(cur, dict) or k not in cur:
                raise KeyError(k)
            cur = cur[k]
        return cur

    def _key(d: dict):
        try:
            val = _extract(d)
            is_missing = 0 if missing == "last" else 1  # present: 0 (last) or 1 (first)
        except KeyError:
            if missing == "raise":
                raise
            val = None
            is_missing = 1 if missing == "last" else 0  # missing: 1 (last) or 0 (first)

        if key_func is not None:
            val = key_func(val)
        return (is_missing, val)

    return sorted(list(data), key=_key, reverse=reverse)


if __name__ == "__main__":
    # quick demo
    people = [
        {"name": "Alice", "age": 30},
        {"name": "bob", "age": 25},
        {"name": "Charlie"},  # missing age
        {"name": "dan", "age": 35},
    ]

    print("by age (missing last):")
    print(sort_dicts(people, "age"))

    print("by age (missing first):")
    print(sort_dicts(people, "age", missing="first"))

    print("by name (case-insensitive):")
    print(sort_dicts(people, "name", key_func=lambda s: (s or "").lower()))


def manual_sort_by_key(data, key):
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i][key] > data[j][key]:
                data[i], data[j] = data[j], data[i]
    return data


if __name__ == "__main__":
    items = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
        {"name": "Charlie", "age": 20}
    ]

    print("Copilot result:", sort_dicts(items, "age"))
    print("Manual result:", manual_sort_by_key(items.copy(), "age"))
