from ydnatl.core.element import HTMLElement
from ydnatl.tags.tag_factory import simple_tag_class


class HTML(HTMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **{
                **kwargs | {"lang": "en", "dir": "ltr"},
                "tag": "html",
                "self_closing": False,
            },
        )
        self._prefix = "<!DOCTYPE html>"


Head = simple_tag_class("head")
Body = simple_tag_class("body")
Title = simple_tag_class("title")
Meta = simple_tag_class("meta", self_closing=True)
Base = simple_tag_class("base", self_closing=True)
Link = simple_tag_class("link", self_closing=True)
Script = simple_tag_class("script")
Style = simple_tag_class("style")
Noscript = simple_tag_class("noscript")
IFrame = simple_tag_class("iframe")
