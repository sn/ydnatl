from ydnatl.core.element import HTMLElement
from ydnatl.tags.tag_factory import simple_tag_class

Textarea = simple_tag_class("textarea")
BaseSelect = simple_tag_class("select")
Option = simple_tag_class("option")
Button = simple_tag_class("button")
Fieldset = simple_tag_class("fieldset")
Legend = simple_tag_class("legend")
Input = simple_tag_class("input", self_closing=True)
Optgroup = simple_tag_class("optgroup")
Output = simple_tag_class("output")
Progress = simple_tag_class("progress")
Meter = simple_tag_class("meter")


class Select(BaseSelect):
    @classmethod
    def with_items(cls, *items, **kwargs):
        opt = cls(**kwargs)
        for item in items:
            if isinstance(item, HTMLElement):
                opt.append(item)
            else:
                opt.append(Option(item))
        return opt


def label_extra_init(self, kwargs):
    if "for_element" in kwargs:
        kwargs["for"] = kwargs.pop("for_element")


Label = simple_tag_class("label", extra_init=label_extra_init)


class Form(HTMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{**kwargs, "tag": "form"})

    @staticmethod
    def with_fields(*items, **kwargs):
        form = Form(**kwargs)
        valid_types = (
            Input,
            Textarea,
            Select,
            Option,
            Button,
            Fieldset,
            Legend,
            Label,
            Optgroup,
            Output,
            Progress,
            Meter,
        )
        for item in items:
            if not isinstance(item, valid_types):
                raise TypeError(
                    f"Invalid form field: {item!r} (type {type(item).__name__})"
                )
            form.append(item)
        return form
