import unittest

from ydnatl.core.element import HTMLElement
from ydnatl.tags.lists import (
    UnorderedList,
    OrderedList,
    ListItem,
    Datalist,
    DescriptionDetails,
    DescriptionList,
    DescriptionTerm,
)


class TestListTags(unittest.TestCase):

    def test_unordered_list(self):
        """Test the creation of an empty unordered list."""
        ul = UnorderedList()
        self.assertEqual(ul.tag, "ul")
        self.assertEqual(str(ul), "<ul></ul>")

    def test_unordered_list_with_items(self):
        """Test the creation of an unordered list with items."""
        ul = UnorderedList.with_items("Item 1", "Item 2", ListItem("Item 3"))
        self.assertEqual(ul.tag, "ul")
        self.assertEqual(
            str(ul), "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
        )

    def test_ordered_list(self):
        """Test the creation of an empty ordered list."""
        ol = OrderedList()
        self.assertEqual(ol.tag, "ol")
        self.assertEqual(str(ol), "<ol></ol>")

    def test_ordered_list_with_items(self):
        """Test the creation of an ordered list with items."""
        ol = OrderedList.with_items("Item 1", "Item 2", ListItem("Item 3"))
        self.assertEqual(ol.tag, "ol")
        self.assertEqual(
            str(ol), "<ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol>"
        )

    def test_list_item(self):
        """Test the creation of a list item."""
        li = ListItem("List item")
        self.assertEqual(li.tag, "li")
        self.assertEqual(str(li), "<li>List item</li>")

    def test_datalist(self):
        """Test the creation of an empty datalist."""
        datalist = Datalist()
        self.assertEqual(datalist.tag, "datalist")
        self.assertEqual(str(datalist), "<datalist></datalist>")

    def test_description_details(self):
        """Test the creation of a description details element."""
        dd = DescriptionDetails("Description")
        self.assertEqual(dd.tag, "dd")
        self.assertEqual(str(dd), "<dd>Description</dd>")

    def test_description_list(self):
        """Test the creation of an empty description list."""
        dl = DescriptionList()
        self.assertEqual(dl.tag, "dl")
        self.assertEqual(str(dl), "<dl></dl>")

    def test_description_term(self):
        """Test the creation of a description term element."""
        dt = DescriptionTerm("Term")
        self.assertEqual(dt.tag, "dt")
        self.assertEqual(str(dt), "<dt>Term</dt>")

    def test_nested_lists(self):
        """Test the creation of a nested unordered list."""
        ul = UnorderedList.with_items("Item 1", "Item 3")
        expected = "<ul>" "<li>Item 1</li>" "<li>Item 3</li>" "</ul>"
        self.assertEqual(str(ul), expected)

    def test_description_list_with_terms_and_details(self):
        """Test the creation of a description list with terms and details."""
        dl = DescriptionList(
            DescriptionTerm("Term 1"),
            DescriptionDetails("Description 1"),
            DescriptionTerm("Term 2"),
            DescriptionDetails("Description 2"),
        )
        expected = (
            "<dl>"
            "<dt>Term 1</dt>"
            "<dd>Description 1</dd>"
            "<dt>Term 2</dt>"
            "<dd>Description 2</dd>"
            "</dl>"
        )
        self.assertEqual(str(dl), expected)

    def test_attributes(self):
        """Test the addition of attributes to an unordered list."""
        ul = UnorderedList(id="my-list", class_name="list-style")
        self.assertEqual(str(ul), '<ul id="my-list" class="list-style"></ul>')

    def test_inheritance(self):
        """Test that all list-related classes inherit from HTMLElement."""
        for cls in [
            UnorderedList,
            OrderedList,
            ListItem,
            Datalist,
            DescriptionDetails,
            DescriptionList,
            DescriptionTerm,
        ]:
            self.assertTrue(issubclass(cls, HTMLElement))


if __name__ == "__main__":
    unittest.main()
