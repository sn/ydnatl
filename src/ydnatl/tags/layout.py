from ydnatl.tags.tag_factory import simple_tag_class

Div = simple_tag_class("div")
Section = simple_tag_class("section")
Header = simple_tag_class("header")
Nav = simple_tag_class("nav")
Footer = simple_tag_class("footer")
HorizontalRule = simple_tag_class("hr", self_closing=True)
Main = simple_tag_class("main")
