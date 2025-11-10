from ydnatl.core.element import HTMLElement


# Factory function to create simple tag classes
def simple_tag_class(tag, self_closing=False, extra_init=None):
    if not isinstance(tag, str):
        raise TypeError(f"tag must be a string, got {type(tag)}")

    if extra_init is not None and not callable(extra_init):
        raise TypeError("extra_init must be callable")

    class _Tag(HTMLElement):
        def __init__(self, *args, **kwargs):
            if extra_init:
                extra_init(self, kwargs)
            super().__init__(
                *args,
                **{
                    **kwargs,
                    "tag": tag,
                    **({"self_closing": True} if self_closing else {}),
                },
            )

    # @NOTE __qualname__ for serialization
    class_name = tag.capitalize() if tag.islower() else tag
    _Tag.__name__ = class_name
    _Tag.__qualname__ = class_name
    return _Tag
