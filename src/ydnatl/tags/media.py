from ydnatl.tags.tag_factory import simple_tag_class

Image = simple_tag_class("img", self_closing=True)
Video = simple_tag_class("video")
Audio = simple_tag_class("audio")
Source = simple_tag_class("source", self_closing=True)
Picture = simple_tag_class("picture")
Figure = simple_tag_class("figure")
Figcaption = simple_tag_class("figcaption")
Canvas = simple_tag_class("canvas")
