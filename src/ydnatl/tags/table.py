import csv
import json

from ydnatl.core.element import HTMLElement
from ydnatl.tags.tag_factory import simple_tag_class

TableFooter = simple_tag_class("tfoot")
TableHeaderCell = simple_tag_class("th")
TableHeader = simple_tag_class("thead")
TableBody = simple_tag_class("tbody")
TableDataCell = simple_tag_class("td")
TableRow = simple_tag_class("tr")
Caption = simple_tag_class("caption")
Col = simple_tag_class("col", self_closing=True)
Colgroup = simple_tag_class("colgroup")


class Table(HTMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{**kwargs, "tag": "table"})

    @classmethod
    def from_csv(cls, file_path: str, encoding: str = "utf-8") -> "Table":
        table = cls()
        try:
            with open(file_path, mode="r", encoding=encoding) as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    table_row = TableRow()
                    for cell in row:
                        table_row.append(TableDataCell(cell))
                    table.append(table_row)
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except csv.Error as e:
            raise ValueError(f"CSV error occurred: {e}")
        except UnicodeDecodeError:
            raise ValueError(f"Encoding error: {encoding} is not suitable for the file")
        return table

    @classmethod
    def from_json(cls, file_path: str, encoding: str = "utf-8") -> "Table":
        table = cls()
        try:
            with open(file_path, mode="r", encoding=encoding) as file:
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValueError("JSON data must be a list of rows")
                for row in data:
                    if not isinstance(row, list):
                        raise ValueError("Each row in JSON data must be a list")
                    table_row = TableRow()
                    for cell in row:
                        table_row.append(TableDataCell(str(cell)))
                    table.append(table_row)
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON decoding error: {e}")
        except UnicodeDecodeError:
            raise ValueError(f"Encoding error: {encoding} is not suitable for the file")
        return table
