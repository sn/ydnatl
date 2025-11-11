import unittest

from ydnatl.core.element import HTMLElement
from ydnatl.tags.layout import Div
from ydnatl.tags.text import Span, Paragraph


class TestHTMLElement(unittest.TestCase):

    def test_prepend(self):
        """Test the prepend() method."""
        element = HTMLElement(tag="div")
        div = HTMLElement(tag="div")
        element.prepend(div)
        self.assertEqual(len(element.children), 1)
        self.assertEqual(str(element.children[0]), "<div></div>")

    def test_append(self):
        """Test the append() method."""
        element = HTMLElement(tag="div")
        div = HTMLElement(tag="div")
        element.append(div)
        self.assertEqual(len(element.children), 1)
        self.assertEqual(str(element.children[0]), "<div></div>")

    def test_filter(self):
        """Test the filter() method."""
        element = HTMLElement(tag="div")
        span = Span("Child 1")
        p = Paragraph("Child 2")
        div = Div("Child 3")
        element.append(span, p, div)

        filtered = list(element.filter(lambda x: x.tag == "span"))
        self.assertEqual(len(filtered), 1)
        self.assertEqual(str(filtered[0]), "<span>Child 1</span>")

    def test_remove_all(self):
        """Test the remove_all() method."""
        element = HTMLElement(tag="div")
        child1 = HTMLElement(tag="span")
        child2 = HTMLElement(tag="p")
        child3 = HTMLElement(tag="div")
        element.append(child1, child2, child3)

        element.remove_all(lambda x: x.tag == "span")
        self.assertEqual(len(element.children), 2)
        self.assertEqual(str(element.children[0]), "<p></p>")
        self.assertEqual(str(element.children[1]), "<div></div>")

    def test_clear(self):
        """Test the clear() method."""
        element = HTMLElement(tag="div")
        element.append(HTMLElement(tag="span"), HTMLElement(tag="p"))
        element.clear()
        self.assertEqual(len(element.children), 0)

    def test_pop(self):
        """Test the pop() method."""
        element = HTMLElement(tag="div")
        child1 = HTMLElement(tag="span")
        child2 = HTMLElement(tag="p")
        element.append(child1, child2)

        popped = element.pop(0)
        self.assertEqual(str(popped), "<span></span>")
        self.assertEqual(len(element.children), 1)
        self.assertEqual(str(element.children[0]), "<p></p>")

    def test_first_last(self):
        """Test the first() and last() methods."""
        element = HTMLElement(tag="div")
        child1 = HTMLElement(tag="span")
        child2 = HTMLElement(tag="p")
        element.append(child1, child2)

        self.assertEqual(str(element.first()), "<span></span>")
        self.assertEqual(str(element.last()), "<p></p>")

    def test_add_remove_attribute(self):
        """Test the add_attribute() and remove_attribute() methods."""
        element = HTMLElement(tag="div")
        element.add_attribute("id", "my-div")
        self.assertEqual(element.attributes, {"id": "my-div"})

        element.remove_attribute("id")
        self.assertEqual(element.attributes, {})

    def test_get_has_attribute(self):
        """Test the get_attribute() and has_attribute() methods."""
        element = HTMLElement(tag="div", id="my-div", class_name="container")
        self.assertEqual(element.get_attribute("id"), "my-div")
        self.assertEqual(element.get_attribute("class_name"), "container")
        self.assertTrue(element.has_attribute("id"))
        self.assertFalse(element.has_attribute("style"))

    def test_generate_id(self):
        """Test the generate_id() method."""
        element = HTMLElement(tag="div")
        element.generate_id()
        self.assertTrue(element.has_attribute("id"))
        self.assertTrue(element.get_attribute("id").startswith("el-"))

    def test_clone(self):
        """Test the clone() method."""
        element = HTMLElement(tag="div", id="my-div", text="Hello")
        child = HTMLElement(tag="span")
        element.append(child)

        cloned = element.clone()
        self.assertEqual(str(cloned), str(element))
        self.assertIsNot(cloned, element)
        self.assertIsNot(cloned.children[0], child)

    def test_find_by_attribute(self):
        """Test the find_by_attribute() method."""
        element = HTMLElement(tag="div")
        child1 = HTMLElement(tag="span", id="child1")
        child2 = HTMLElement(tag="p", id="child2")
        child3 = HTMLElement(tag="div", id="child3")
        element.append(child1, child2, child3)

        found = element.find_by_attribute("id", "child2")
        self.assertEqual(str(found), '<p id="child2"></p>')

        nested_child = HTMLElement(tag="span", id="nested")
        child3.append(nested_child)
        found_nested = element.find_by_attribute("id", "nested")
        self.assertEqual(str(found_nested), '<span id="nested"></span>')

    def test_get_attributes(self):
        """Test the get_attributes() method."""
        element = HTMLElement(
            tag="div", id="my-div", class_name="container", style="color: red"
        )
        self.assertEqual(
            element.get_attributes("id", "class_name"),
            {"id": "my-div", "class_name": "container"},
        )
        self.assertEqual(
            element.get_attributes(),
            {"id": "my-div", "class_name": "container", "style": "color: red"},
        )

    def test_count_children(self):
        """Test the count_children method."""
        element = HTMLElement(tag="div")
        element.append(HTMLElement(tag="span"), HTMLElement(tag="p"))
        self.assertEqual(element.count_children(), 2)

    def test_replace_child(self):
        """Test the replace_child() method."""
        element = HTMLElement(tag="div")
        element.append(HTMLElement(tag="span"), HTMLElement(tag="p"))
        self.assertEqual(element.count_children(), 2)
        self.assertEqual(str(element.children[0]), "<span></span>")
        self.assertEqual(str(element.children[1]), "<p></p>")
        element.replace_child(0, HTMLElement(tag="h1"))
        self.assertEqual(element.count_children(), 2)
        self.assertEqual(str(element.children[0]), "<h1></h1>")

    def test_callbacks(self):
        """Test the callback methods."""

        class TestElement(HTMLElement):
            def on_load(self):
                self.loaded = True

            def on_before_render(self):
                self.before_render_called = True

            def on_after_render(self):
                self.after_render_called = True

        element = TestElement(tag="div")
        self.assertTrue(hasattr(element, "loaded"))
        self.assertTrue(element.loaded)

        element.render()
        self.assertTrue(hasattr(element, "before_render_called"))
        self.assertTrue(element.before_render_called)

        self.assertTrue(hasattr(element, "after_render_called"))
        self.assertTrue(element.after_render_called)

    def test_add_attributes(self):
        """Test the add_attributes method."""
        element = HTMLElement(tag="div")
        element.add_attributes([("id", "my-div"), ("class", "container")])
        self.assertEqual(element.attributes, {"id": "my-div", "class": "container"})

        element.add_attributes([("id", "new-id"), ("style", "color: red")])
        self.assertEqual(
            element.attributes,
            {"id": "new-id", "class": "container", "style": "color: red"},
        )

    def test_to_dict(self):
        el1 = HTMLElement(tag="span", text="Child 1")
        el1.append(HTMLElement(tag="span", text="Child 2"))
        should_be = {
            "tag": "span",
            "self_closing": False,
            "attributes": {"text": "Child 1"},
            "text": "",
            "children": [
                {
                    "tag": "span",
                    "self_closing": False,
                    "attributes": {"text": "Child 2"},
                    "text": "",
                    "children": [],
                }
            ],
        }
        self.assertIsNotNone(el1.to_dict())
        self.assertIsInstance(el1.to_dict(), dict)
        self.assertEqual(el1.to_dict(), should_be)

    def test_html_escaping_text_content(self):
        """Test that text content is properly escaped to prevent XSS."""
        malicious_text = '<script>alert("XSS")</script>'
        element = HTMLElement(malicious_text, tag="div")
        rendered = str(element)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn("&lt;/script&gt;", rendered)
        self.assertNotIn("<script>", rendered)
        self.assertNotIn("</script>", rendered)

    def test_html_escaping_attribute_values(self):
        """Test that attribute values are properly escaped to prevent XSS."""
        malicious_attr = '"><script>alert("XSS")</script><div id="'
        element = HTMLElement(tag="div", id=malicious_attr)
        rendered = str(element)
        self.assertIn("&quot;", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertNotIn('"><script>', rendered)

    def test_html_escaping_normal_content(self):
        """Test that normal content is not affected by escaping."""
        normal_text = "Hello, World!"
        element = HTMLElement(normal_text, tag="p")
        rendered = str(element)
        self.assertEqual(rendered, f"<p>{normal_text}</p>")

    def test_to_json_simple_element(self):
        """Test serialization of a simple element to JSON."""
        import json

        element = HTMLElement("Hello", tag="div", id="test", class_name="container")
        json_str = element.to_json()
        self.assertIsInstance(json_str, str)
        data = json.loads(json_str)
        self.assertEqual(data["tag"], "div")
        self.assertEqual(data["text"], "Hello")
        self.assertEqual(data["attributes"]["id"], "test")

    def test_to_json_with_indent(self):
        """Test JSON serialization with indentation."""
        element = HTMLElement("Test", tag="p")
        json_str = element.to_json(indent=2)
        self.assertIn("\n", json_str)  # Should have newlines with indentation
        self.assertIn("  ", json_str)  # Should have spaces for indentation

    def test_to_json_nested_elements(self):
        """Test serialization of nested elements to JSON."""
        parent = HTMLElement(tag="div", id="parent")
        child1 = HTMLElement("Child 1", tag="span")
        child2 = HTMLElement("Child 2", tag="span")
        parent.append(child1, child2)

        json_str = parent.to_json()
        import json

        data = json.loads(json_str)

        self.assertEqual(len(data["children"]), 2)
        self.assertEqual(data["children"][0]["text"], "Child 1")
        self.assertEqual(data["children"][1]["text"], "Child 2")

    def test_from_dict_simple_element(self):
        """Test reconstruction of a simple element from dictionary."""
        data = {
            "tag": "div",
            "self_closing": False,
            "attributes": {"id": "test", "class": "container"},
            "text": "Hello",
            "children": [],
        }
        element = HTMLElement.from_dict(data)

        self.assertEqual(element.tag, "div")
        self.assertEqual(element.text, "Hello")
        self.assertEqual(element.get_attribute("id"), "test")
        self.assertEqual(element.get_attribute("class"), "container")
        self.assertFalse(element.self_closing)

    def test_from_dict_self_closing_element(self):
        """Test reconstruction of a self-closing element."""
        data = {
            "tag": "br",
            "self_closing": True,
            "attributes": {},
            "text": "",
            "children": [],
        }
        element = HTMLElement.from_dict(data)

        self.assertEqual(element.tag, "br")
        self.assertTrue(element.self_closing)
        self.assertEqual(str(element), "<br />")

    def test_from_dict_nested_elements(self):
        """Test reconstruction of nested elements from dictionary."""
        data = {
            "tag": "div",
            "self_closing": False,
            "attributes": {"id": "parent"},
            "text": "",
            "children": [
                {
                    "tag": "span",
                    "self_closing": False,
                    "attributes": {},
                    "text": "Child 1",
                    "children": [],
                },
                {
                    "tag": "span",
                    "self_closing": False,
                    "attributes": {},
                    "text": "Child 2",
                    "children": [],
                },
            ],
        }
        element = HTMLElement.from_dict(data)

        self.assertEqual(element.tag, "div")
        self.assertEqual(len(element.children), 2)
        self.assertEqual(element.children[0].text, "Child 1")
        self.assertEqual(element.children[1].text, "Child 2")

    def test_from_dict_invalid_input(self):
        """Test from_dict with invalid input."""
        with self.assertRaises(ValueError) as context:
            HTMLElement.from_dict("not a dict")
        self.assertIn("must be a dictionary", str(context.exception))

    def test_from_dict_missing_tag(self):
        """Test from_dict with missing tag key."""
        data = {"attributes": {}, "text": "Test"}
        with self.assertRaises(ValueError) as context:
            HTMLElement.from_dict(data)
        self.assertIn("must contain 'tag' key", str(context.exception))

    def test_from_json_simple_element(self):
        """Test reconstruction from JSON string."""
        json_str = '{"tag": "p", "self_closing": false, "attributes": {"id": "test"}, "text": "Hello", "children": []}'
        element = HTMLElement.from_json(json_str)

        self.assertEqual(element.tag, "p")
        self.assertEqual(element.text, "Hello")
        self.assertEqual(element.get_attribute("id"), "test")

    def test_from_json_invalid_json(self):
        """Test from_json with invalid JSON string."""
        invalid_json = "{invalid json}"
        with self.assertRaises(ValueError) as context:
            HTMLElement.from_json(invalid_json)
        self.assertIn("Invalid JSON string", str(context.exception))

    def test_round_trip_serialization(self):
        """Test that serialization and deserialization preserve element structure."""
        original = HTMLElement(tag="div", id="container", class_name="wrapper")
        section = HTMLElement(tag="section")
        section.append(
            HTMLElement("Paragraph 1", tag="p"),
            HTMLElement("Paragraph 2", tag="p", class_name="highlight"),
        )
        original.append(HTMLElement("Header", tag="h1"), section)

        json_str = original.to_json()

        restored = HTMLElement.from_json(json_str)

        self.assertEqual(original.tag, restored.tag)
        self.assertEqual(original.get_attribute("id"), restored.get_attribute("id"))
        self.assertEqual(len(original.children), len(restored.children))
        self.assertEqual(original.children[0].text, restored.children[0].text)

        self.assertEqual(str(original), str(restored))

    def test_round_trip_with_attributes(self):
        """Test round-trip serialization with various attributes."""
        original = HTMLElement(
            tag="input",
            self_closing=True,
            type="text",
            name="username",
            placeholder="Enter username",
            data_validation="required",
        )

        json_str = original.to_json()
        restored = HTMLElement.from_json(json_str)

        self.assertEqual(original.get_attribute("type"), restored.get_attribute("type"))
        self.assertEqual(original.get_attribute("name"), restored.get_attribute("name"))
        self.assertEqual(
            original.get_attribute("placeholder"), restored.get_attribute("placeholder")
        )
        self.assertEqual(
            original.get_attribute("data-validation"),
            restored.get_attribute("data-validation"),
        )
        self.assertEqual(str(original), str(restored))

    def test_serialization_deeply_nested(self):
        """Test serialization of deeply nested structures."""
        root = HTMLElement(tag="div", id="root")
        level1 = HTMLElement(tag="div", id="level1")
        level2 = HTMLElement(tag="div", id="level2")
        level3 = HTMLElement("Deep content", tag="span")

        level2.append(level3)
        level1.append(level2)
        root.append(level1)

        json_str = root.to_json()
        restored = HTMLElement.from_json(json_str)

        self.assertEqual(
            restored.children[0].children[0].children[0].text, "Deep content"
        )
        self.assertEqual(str(root), str(restored))

    def test_render_pretty_simple(self):
        """Test pretty printing with simple nested structure."""
        element = HTMLElement(tag="div", id="container")
        element.append(HTMLElement("Hello", tag="h1"), HTMLElement("World", tag="p"))

        # Test compact (default)
        compact = element.render(pretty=False)
        self.assertNotIn("\n", compact)
        self.assertEqual(
            compact, '<div id="container"><h1>Hello</h1><p>World</p></div>'
        )

        # Test pretty
        pretty = element.render(pretty=True)
        self.assertIn("\n", pretty)
        self.assertIn("  ", pretty)  # Should have indentation

    def test_render_pretty_deeply_nested(self):
        """Test pretty printing with deeply nested structure."""
        root = HTMLElement(tag="div")
        level1 = HTMLElement(tag="section")
        level2 = HTMLElement(tag="article")
        level2.append(HTMLElement("Content", tag="p"))
        level1.append(level2)
        root.append(level1)

        pretty = root.render(pretty=True)
        lines = pretty.strip().split("\n")

        # Should have multiple indentation levels
        self.assertTrue(any(line.startswith("    ") for line in lines))
        self.assertTrue(any(line.startswith("  ") for line in lines))

    def test_render_pretty_self_closing(self):
        """Test pretty printing with self-closing tags."""
        element = HTMLElement(tag="br", self_closing=True)
        pretty = element.render(pretty=True)
        self.assertEqual(pretty, "<br />\n")

    def test_add_style_single(self):
        """Test adding a single CSS style."""
        element = HTMLElement(tag="div")
        element.add_style("color", "red")

        self.assertEqual(element.get_attribute("style"), "color: red")
        rendered = str(element)
        self.assertIn('style="color: red"', rendered)

    def test_add_styles_multiple(self):
        """Test adding multiple CSS styles at once."""
        element = HTMLElement(tag="div")
        element.add_styles({"color": "blue", "font-size": "14px", "margin": "10px"})

        style = element.get_attribute("style")
        self.assertIn("color: blue", style)
        self.assertIn("font-size: 14px", style)
        self.assertIn("margin: 10px", style)

    def test_add_style_updates_existing(self):
        """Test that adding styles updates existing style attribute."""
        element = HTMLElement(tag="div", style="color: red")
        element.add_style("font-size", "16px")

        style = element.get_attribute("style")
        self.assertIn("color: red", style)
        self.assertIn("font-size: 16px", style)

    def test_get_style(self):
        """Test getting individual CSS style values."""
        element = HTMLElement(tag="div")
        element.add_styles({"color": "green", "padding": "5px"})

        self.assertEqual(element.get_style("color"), "green")
        self.assertEqual(element.get_style("padding"), "5px")
        self.assertIsNone(element.get_style("margin"))

    def test_remove_style(self):
        """Test removing CSS styles."""
        element = HTMLElement(tag="div")
        element.add_styles({"color": "red", "font-size": "14px", "margin": "10px"})

        element.remove_style("margin")

        style = element.get_attribute("style")
        self.assertNotIn("margin", style)
        self.assertIn("color: red", style)
        self.assertIn("font-size: 14px", style)

    def test_remove_style_last_one(self):
        """Test that removing the last style removes the style attribute."""
        element = HTMLElement(tag="div")
        element.add_style("color", "red")

        self.assertTrue(element.has_attribute("style"))

        element.remove_style("color")

        self.assertFalse(element.has_attribute("style"))

    def test_parse_styles(self):
        """Test the _parse_styles static method."""
        styles_dict = HTMLElement._parse_styles(
            "color: red; font-size: 14px; margin: 10px"
        )

        self.assertEqual(styles_dict["color"], "red")
        self.assertEqual(styles_dict["font-size"], "14px")
        self.assertEqual(styles_dict["margin"], "10px")

    def test_parse_styles_empty(self):
        """Test parsing empty style string."""
        styles_dict = HTMLElement._parse_styles("")
        self.assertEqual(styles_dict, {})

    def test_format_styles(self):
        """Test the _format_styles static method."""
        styles_dict = {"color": "blue", "font-size": "16px"}
        formatted = HTMLElement._format_styles(styles_dict)

        self.assertIn("color: blue", formatted)
        self.assertIn("font-size: 16px", formatted)

    def test_context_manager(self):
        """Test using HTMLElement as a context manager."""
        with HTMLElement(tag="div", id="test") as element:
            element.append(HTMLElement("Child", tag="span"))
            self.assertEqual(element.count_children(), 1)

        # Should render correctly after context exit
        self.assertEqual(str(element), '<div id="test"><span>Child</span></div>')

    def test_context_manager_nested(self):
        """Test nested context managers."""
        with HTMLElement(tag="div") as outer:
            with HTMLElement(tag="section") as inner:
                inner.append(HTMLElement("Text", tag="p"))
            outer.append(inner)

        self.assertEqual(outer.count_children(), 1)
        self.assertEqual(outer.children[0].count_children(), 1)

    def test_method_chaining_append(self):
        """Test that append returns self for chaining."""
        element = HTMLElement(tag="div")
        result = element.append(HTMLElement(tag="span"))

        self.assertIs(result, element)

        # Test actual chaining
        element = (
            HTMLElement(tag="div")
            .append(HTMLElement(tag="h1"))
            .append(HTMLElement(tag="p"))
        )

        self.assertEqual(element.count_children(), 2)

    def test_method_chaining_prepend(self):
        """Test that prepend returns self for chaining."""
        element = HTMLElement(tag="div")
        result = element.prepend(HTMLElement(tag="span"))

        self.assertIs(result, element)

    def test_method_chaining_add_attribute(self):
        """Test that add_attribute returns self for chaining."""
        element = HTMLElement(tag="div")
        result = element.add_attribute("id", "test")

        self.assertIs(result, element)

        # Test actual chaining
        element = (
            HTMLElement(tag="div")
            .add_attribute("id", "main")
            .add_attribute("class", "container")
        )

        self.assertEqual(element.get_attribute("id"), "main")
        self.assertEqual(element.get_attribute("class"), "container")

    def test_method_chaining_add_attributes(self):
        """Test that add_attributes returns self for chaining."""
        element = HTMLElement(tag="div")
        result = element.add_attributes([("id", "test")])

        self.assertIs(result, element)

    def test_method_chaining_remove_attribute(self):
        """Test that remove_attribute returns self for chaining."""
        element = HTMLElement(tag="div", id="test")
        result = element.remove_attribute("id")

        self.assertIs(result, element)

    def test_method_chaining_add_style(self):
        """Test that add_style returns self for chaining."""
        element = HTMLElement(tag="div")
        result = element.add_style("color", "red")

        self.assertIs(result, element)

        # Test actual chaining
        element = (
            HTMLElement(tag="div")
            .add_style("color", "blue")
            .add_style("font-size", "14px")
        )

        self.assertEqual(element.get_style("color"), "blue")
        self.assertEqual(element.get_style("font-size"), "14px")

    def test_method_chaining_add_styles(self):
        """Test that add_styles returns self for chaining."""
        element = HTMLElement(tag="div")
        result = element.add_styles({"color": "red"})

        self.assertIs(result, element)

    def test_method_chaining_remove_style(self):
        """Test that remove_style returns self for chaining."""
        element = HTMLElement(tag="div")
        element.add_style("color", "red")
        result = element.remove_style("color")

        self.assertIs(result, element)

    def test_method_chaining_clear(self):
        """Test that clear returns self for chaining."""
        element = HTMLElement(tag="div")
        element.append(HTMLElement(tag="span"))
        result = element.clear()

        self.assertIs(result, element)

    def test_method_chaining_remove_all(self):
        """Test that remove_all returns self for chaining."""
        element = HTMLElement(tag="div")
        element.append(HTMLElement(tag="span"))
        result = element.remove_all(lambda x: x.tag == "span")

        self.assertIs(result, element)

    def test_method_chaining_complex(self):
        """Test complex method chaining scenario."""
        element = (
            HTMLElement(tag="div")
            .add_attribute("id", "container")
            .add_attribute("class", "wrapper")
            .add_style("background", "#f0f0f0")
            .add_styles({"padding": "20px", "margin": "10px"})
            .append(HTMLElement("Title", tag="h1"))
            .append(HTMLElement("Content", tag="p"))
        )

        self.assertEqual(element.get_attribute("id"), "container")
        self.assertEqual(element.get_attribute("class"), "wrapper")
        self.assertEqual(element.get_style("background"), "#f0f0f0")
        self.assertEqual(element.get_style("padding"), "20px")
        self.assertEqual(element.count_children(), 2)


if __name__ == "__main__":
    unittest.main()
