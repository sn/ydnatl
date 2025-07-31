def render_c(html) -> str:
    """Renders the HTML element and its children to a string."""
    html.on_before_render()
    attributes = html._render_attributes()
    tag_start = f"<{html._tag}{attributes}"

    if html._self_closing:
        result = f"{tag_start} />"
    else:
        children_html = "".join(child.render() for child in html._children)
        result = f"{tag_start}>{html._text}{children_html}</{html._tag}>"

    if hasattr(html, "_prefix") and html._prefix:
        result = f"{html._prefix}{result}"

    html.on_after_render()
    return result