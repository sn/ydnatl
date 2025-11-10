import csv
import json
import os
import tempfile
import unittest

from ydnatl.core.element import HTMLElement
from ydnatl.tags.table import (
    Table,
    TableFooter,
    TableHeaderCell,
    TableHeader,
    TableBody,
    TableDataCell,
    TableRow,
    Caption,
    Col,
    Colgroup,
)


class TestTableTags(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_table(self):
        """Test the creation of a table element."""
        table = Table()
        self.assertEqual(table.tag, "table")
        self.assertEqual(str(table), "<table></table>")

    def test_table_footer(self):
        """Test the creation of a table footer element."""
        tfoot = TableFooter()
        self.assertEqual(tfoot.tag, "tfoot")
        self.assertEqual(str(tfoot), "<tfoot></tfoot>")

    def test_table_header_cell(self):
        """Test the creation of a table header cell element."""
        th = TableHeaderCell("Header")
        self.assertEqual(th.tag, "th")
        self.assertEqual(str(th), "<th>Header</th>")

    def test_table_header(self):
        """Test the creation of a table header element."""
        thead = TableHeader()
        self.assertEqual(thead.tag, "thead")
        self.assertEqual(str(thead), "<thead></thead>")

    def test_table_body(self):
        """Test the creation of a table body element."""
        tbody = TableBody()
        self.assertEqual(tbody.tag, "tbody")
        self.assertEqual(str(tbody), "<tbody></tbody>")

    def test_table_data_cell(self):
        """Test the creation of a table data cell element."""
        td = TableDataCell("Data")
        self.assertEqual(td.tag, "td")
        self.assertEqual(str(td), "<td>Data</td>")

    def test_table_row(self):
        """Test the creation of a table row element."""
        tr = TableRow(TableDataCell("Cell 1"), TableDataCell("Cell 2"))
        self.assertEqual(tr.tag, "tr")
        self.assertEqual(str(tr), "<tr><td>Cell 1</td><td>Cell 2</td></tr>")

    def test_table_from_csv(self):
        """Test creating a table from a CSV file."""
        csv_file = os.path.join(self.temp_dir, "test.csv")
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Header 1", "Header 2"])
            writer.writerow(["Data 1", "Data 2"])

        table = Table.from_csv(csv_file)
        expected = (
            "<table>"
            "<tr><td>Header 1</td><td>Header 2</td></tr>"
            "<tr><td>Data 1</td><td>Data 2</td></tr>"
            "</table>"
        )
        self.assertEqual(str(table), expected)

    def test_table_from_csv_file_not_found(self):
        """Test error handling when CSV file is not found."""
        with self.assertRaises(ValueError) as context:
            Table.from_csv("non_existent_file.csv")
        self.assertTrue("File not found" in str(context.exception))

    def test_table_from_csv_encoding_error(self):
        """Test error handling for CSV file encoding errors."""
        csv_file = os.path.join(self.temp_dir, "test.csv")
        with open(csv_file, "wb") as f:
            f.write(b"\xff\xfe\x00\x00")  # UTF-32 LE BOM

        with self.assertRaises(ValueError) as context:
            Table.from_csv(csv_file, encoding="utf-8")
        self.assertTrue("Encoding error" in str(context.exception))

    def test_table_from_json(self):
        """Test creating a table from a JSON file."""
        json_file = os.path.join(self.temp_dir, "test.json")
        with open(json_file, "w") as f:
            json.dump([["Header 1", "Header 2"], ["Data 1", "Data 2"]], f)

        table = Table.from_json(json_file)
        expected = (
            "<table>"
            "<tr><td>Header 1</td><td>Header 2</td></tr>"
            "<tr><td>Data 1</td><td>Data 2</td></tr>"
            "</table>"
        )
        self.assertEqual(str(table), expected)

    def test_table_from_json_file_not_found(self):
        """Test error handling when JSON file is not found."""
        with self.assertRaises(ValueError) as context:
            Table.from_json("non_existent_file.json")
        self.assertTrue("File not found" in str(context.exception))

    def test_table_from_json_json_error(self):
        """Test error handling for JSON parsing errors."""
        json_file = os.path.join(self.temp_dir, "test.json")
        with open(json_file, "w") as f:
            f.write("Invalid JSON")

        with self.assertRaises(ValueError) as context:
            Table.from_json(json_file)
        self.assertTrue("JSON decoding error" in str(context.exception))

    def test_table_from_json_encoding_error(self):
        """Test error handling for JSON file encoding errors."""
        json_file = os.path.join(self.temp_dir, "test.json")
        with open(json_file, "wb") as f:
            f.write(b"\xff\xfe\x00\x00")  # UTF-32 LE BOM

        with self.assertRaises(ValueError) as context:
            Table.from_json(json_file, encoding="utf-8")
        self.assertTrue("Encoding error" in str(context.exception))

    def test_table_from_json_invalid_data(self):
        """Test error handling for invalid JSON data structure."""
        json_file = os.path.join(self.temp_dir, "test.json")
        with open(json_file, "w") as f:
            json.dump({"invalid": "data"}, f)

        with self.assertRaises(ValueError) as context:
            Table.from_json(json_file)
        self.assertTrue("JSON data must be a list of rows" in str(context.exception))

    def test_table_from_json_invalid_row(self):
        """Test error handling for invalid JSON row structure."""
        json_file = os.path.join(self.temp_dir, "test.json")
        with open(json_file, "w") as f:
            json.dump([["valid"], {"invalid": "row"}], f)

        with self.assertRaises(ValueError) as context:
            Table.from_json(json_file)
        self.assertTrue(
            "Each row in JSON data must be a list" in str(context.exception)
        )

    def test_attributes(self):
        """Test the addition of attributes to table elements."""
        table = Table(id="my-table", class_name="table-style")
        self.assertEqual(
            str(table), '<table id="my-table" class="table-style"></table>'
        )

    def test_caption(self):
        """Test the creation of a caption element."""
        caption = Caption("Table Title")
        self.assertEqual(caption.tag, "caption")
        self.assertEqual(str(caption), "<caption>Table Title</caption>")

    def test_table_with_caption(self):
        """Test table element with caption."""
        table = Table(
            Caption("Monthly Sales"),
            TableRow(TableHeaderCell("Month"), TableHeaderCell("Sales")),
        )
        self.assertIn("<caption>Monthly Sales</caption>", str(table))

    def test_col(self):
        """Test the creation of a col element."""
        col = Col(span="2", style="background-color: yellow")
        self.assertEqual(col.tag, "col")
        self.assertTrue(col.self_closing)
        self.assertIn('span="2"', str(col))

    def test_colgroup(self):
        """Test the creation of a colgroup element."""
        colgroup = Colgroup(Col(span="2"), Col(style="background-color: yellow"))
        self.assertEqual(colgroup.tag, "colgroup")
        self.assertIn("<col", str(colgroup))
        self.assertIn('span="2"', str(colgroup))

    def test_table_with_colgroup(self):
        """Test table element with colgroup."""
        table = Table(
            Colgroup(
                Col(style="background-color: #ddd"), Col(style="background-color: #fff")
            ),
            TableRow(TableDataCell("Data 1"), TableDataCell("Data 2")),
        )
        self.assertIn("<colgroup>", str(table))
        self.assertIn("<col", str(table))

    def test_inheritance(self):
        """Test that all table-related classes inherit from HTMLElement."""
        for cls in [
            Table,
            TableFooter,
            TableHeaderCell,
            TableHeader,
            TableBody,
            TableDataCell,
            TableRow,
            Caption,
            Col,
            Colgroup,
        ]:
            self.assertTrue(issubclass(cls, HTMLElement))


if __name__ == "__main__":
    unittest.main()
