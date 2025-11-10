from ydnatl.tags.tag_factory import simple_tag_class

Div = simple_tag_class("div")
Section = simple_tag_class("section")
Article = simple_tag_class("article")
Aside = simple_tag_class("aside")
Header = simple_tag_class("header")
Nav = simple_tag_class("nav")
Footer = simple_tag_class("footer")
HorizontalRule = simple_tag_class("hr", self_closing=True)
Main = simple_tag_class("main")
Details = simple_tag_class("details")
Summary = simple_tag_class("summary")
Dialog = simple_tag_class("dialog")
