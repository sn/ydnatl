from ydnatl.core.element import HTMLElement
from ydnatl.tags.tag_factory import simple_tag_class

ListItem = simple_tag_class("li")
Datalist = simple_tag_class("datalist")
DescriptionDetails = simple_tag_class("dd")
DescriptionList = simple_tag_class("dl")
DescriptionTerm = simple_tag_class("dt")


class UnorderedList(HTMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{**kwargs, "tag": "ul"})

    @classmethod
    def with_items(cls, *items, **kwargs):
        ul = cls(**kwargs)
        for item in items:
            if isinstance(item, HTMLElement):
                ul.append(item)
            else:
                ul.append(ListItem(item))
        return ul


class OrderedList(HTMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{**kwargs, "tag": "ol"})

    @classmethod
    def with_items(cls, *items, **kwargs):
        ol = cls(**kwargs)
        for item in items:
            if isinstance(item, HTMLElement):
                ol.append(item)
            else:
                ol.append(ListItem(item))
        return ol
