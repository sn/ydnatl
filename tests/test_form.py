import unittest

from ydnatl.core.element import HTMLElement
from ydnatl.tags.form import (
    Textarea,
    Select,
    Option,
    Button,
    Fieldset,
    Legend,
    Form,
    Input,
    Label,
    Optgroup,
    Output,
    Progress,
    Meter,
)


class TestFormTags(unittest.TestCase):

    def test_textarea(self):
        """Test the creation of a textarea element with text content."""
        textarea = Textarea("Hello, World!")
        self.assertEqual(textarea.tag, "textarea")
        self.assertEqual(str(textarea), "<textarea>Hello, World!</textarea>")

    def test_select(self):
        """Test the creation of an empty select element."""
        select = Select()
        self.assertEqual(select.tag, "select")
        self.assertEqual(str(select), "<select></select>")

    def test_select_with_items(self):
        """Test the creation of a select element with multiple options."""
        select = Select.with_items("Option 1", "Option 2", Option("Option 3"))
        self.assertEqual(select.tag, "select")
        self.assertEqual(
            str(select),
            "<select><option>Option 1</option><option>Option 2</option><option>Option 3</option></select>",
        )

    def test_option(self):
        """Test the creation of an option element with text content."""
        option = Option("Choose me!")
        self.assertEqual(option.tag, "option")
        self.assertEqual(str(option), "<option>Choose me!</option>")

    def test_button(self):
        """Test the creation of a button element with text content."""
        button = Button("Click me")
        self.assertEqual(button.tag, "button")
        self.assertEqual(str(button), "<button>Click me</button>")

    def test_fieldset(self):
        """Test the creation of an empty fieldset element."""
        fieldset = Fieldset()
        self.assertEqual(fieldset.tag, "fieldset")
        self.assertEqual(str(fieldset), "<fieldset></fieldset>")

    def test_form(self):
        """Test the creation of an empty form element."""
        form = Form()
        self.assertEqual(form.tag, "form")
        self.assertEqual(str(form), "<form></form>")

    def test_form_with_fields(self):
        """Test the creation of a form element with multiple fields."""
        form = Form.with_fields(
            Input(type="text", name="username"),
            Input(type="password", name="password"),
            Button("Submit"),
        )
        self.assertEqual(form.tag, "form")
        expected = '<form><input type="text" name="username" /><input type="password" name="password" /><button>Submit</button></form>'
        self.assertEqual(str(form), expected)

    def test_input(self):
        """Test the creation of an input element with attributes."""
        input_field = Input(type="text", name="username")
        self.assertEqual(input_field.tag, "input")
        self.assertTrue(input_field.self_closing)
        self.assertEqual(str(input_field), '<input type="text" name="username" />')

    def test_label(self):
        """Test the creation of a label element with a for attribute."""
        label = Label("Username:", for_element="username")
        self.assertEqual(label.tag, "label")
        self.assertEqual(str(label), '<label for="username">Username:</label>')

    def test_optgroup(self):
        """Test the creation of an optgroup element with options."""
        optgroup = Optgroup(label="Group 1")
        optgroup.append(Option("Option 1"))
        optgroup.append(Option("Option 2"))
        self.assertEqual(optgroup.tag, "optgroup")
        self.assertEqual(
            str(optgroup),
            '<optgroup label="Group 1"><option>Option 1</option><option>Option 2</option></optgroup>',
        )

    def test_legend(self):
        """Test the creation of a legend element."""
        legend = Legend("Personal Information")
        self.assertEqual(legend.tag, "legend")
        self.assertEqual(str(legend), "<legend>Personal Information</legend>")

    def test_fieldset_with_legend(self):
        """Test fieldset element with legend and fields."""
        fieldset = Fieldset(
            Legend("Contact Details"),
            Input(type="email", name="email"),
        )
        expected = '<fieldset><legend>Contact Details</legend><input type="email" name="email" /></fieldset>'
        self.assertEqual(str(fieldset), expected)

    def test_output(self):
        """Test the creation of an output element."""
        output = Output("42", for_attr="calculation")
        self.assertEqual(output.tag, "output")
        self.assertIn("42", str(output))

    def test_progress(self):
        """Test the creation of a progress element."""
        progress = Progress(value="70", max="100")
        self.assertEqual(progress.tag, "progress")
        self.assertIn('value="70"', str(progress))
        self.assertIn('max="100"', str(progress))

    def test_meter(self):
        """Test the creation of a meter element."""
        meter = Meter(value="6", min="0", max="10")
        self.assertEqual(meter.tag, "meter")
        self.assertIn('value="6"', str(meter))
        self.assertIn('min="0"', str(meter))
        self.assertIn('max="10"', str(meter))

    def test_inheritance(self):
        """Test that all form-related classes inherit from HTMLElement."""
        for cls in [
            Textarea,
            Select,
            Option,
            Button,
            Fieldset,
            Legend,
            Form,
            Input,
            Label,
            Optgroup,
            Output,
            Progress,
            Meter,
        ]:
            self.assertTrue(issubclass(cls, HTMLElement))


if __name__ == "__main__":
    unittest.main()
