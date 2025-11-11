"""Tests for YDNATL styling system."""

from ydnatl.styles import CSSStyle, StyleSheet, Theme


class TestCSSStyle:
    """Tests for CSSStyle class."""

    def test_basic_style_creation(self):
        """Test creating a basic CSS style."""
        style = CSSStyle(background_color="#007bff", color="white", padding="10px 20px")

        assert style._styles["background-color"] == "#007bff"
        assert style._styles["color"] == "white"
        assert style._styles["padding"] == "10px 20px"

    def test_snake_case_to_kebab_case(self):
        """Test conversion of snake_case to kebab-case."""
        style = CSSStyle(background_color="blue", font_size="14px", border_radius="5px")

        assert "background-color" in style._styles
        assert "font-size" in style._styles
        assert "border-radius" in style._styles

    def test_pseudo_selectors(self):
        """Test pseudo-selector support."""
        style = CSSStyle(
            background_color="#007bff",
            _hover=CSSStyle(background_color="#0056b3"),
            _active=CSSStyle(transform="scale(0.98)"),
        )

        assert "hover" in style._pseudo
        assert style._pseudo["hover"]._styles["background-color"] == "#0056b3"
        assert "active" in style._pseudo
        assert style._pseudo["active"]._styles["transform"] == "scale(0.98)"

    def test_breakpoints(self):
        """Test responsive breakpoint support."""
        style = CSSStyle(
            padding="10px", _sm=CSSStyle(padding="15px"), _md=CSSStyle(padding="20px")
        )

        assert "sm" in style._breakpoints
        assert style._breakpoints["sm"]._styles["padding"] == "15px"
        assert "md" in style._breakpoints
        assert style._breakpoints["md"]._styles["padding"] == "20px"

    def test_to_inline(self):
        """Test inline style generation."""
        style = CSSStyle(background_color="blue", color="white", padding="10px")

        inline = style.to_inline()
        assert "background-color: blue" in inline
        assert "color: white" in inline
        assert "padding: 10px" in inline

    def test_merge(self):
        """Test merging two styles."""
        style1 = CSSStyle(background_color="blue", color="white")
        style2 = CSSStyle(color="black", padding="10px")

        merged = style1.merge(style2)
        assert merged._styles["background-color"] == "blue"
        assert merged._styles["color"] == "black"  # Overridden
        assert merged._styles["padding"] == "10px"

    def test_has_pseudo_or_breakpoints(self):
        """Test detection of pseudo-selectors and breakpoints."""
        style1 = CSSStyle(background_color="blue")
        assert not style1.has_pseudo_or_breakpoints()

        style2 = CSSStyle(
            background_color="blue", _hover=CSSStyle(background_color="red")
        )
        assert style2.has_pseudo_or_breakpoints()

        style3 = CSSStyle(padding="10px", _md=CSSStyle(padding="20px"))
        assert style3.has_pseudo_or_breakpoints()

    def test_is_complex(self):
        """Test complexity detection."""
        simple = CSSStyle(color="blue")
        assert not simple.is_complex(threshold=3)

        complex_style = CSSStyle(
            color="blue", background_color="white", padding="10px", margin="5px"
        )
        assert complex_style.is_complex(threshold=3)

    def test_to_dict_and_from_dict(self):
        """Test serialization and deserialization."""
        original = CSSStyle(
            background_color="blue",
            color="white",
            _hover=CSSStyle(background_color="red"),
        )

        data = original.to_dict()
        restored = CSSStyle.from_dict(data)

        assert restored._styles == original._styles
        assert "hover" in restored._pseudo
        assert restored._pseudo["hover"]._styles["background-color"] == "red"

    def test_equality(self):
        """Test style equality comparison."""
        style1 = CSSStyle(color="blue", padding="10px")
        style2 = CSSStyle(color="blue", padding="10px")
        style3 = CSSStyle(color="red", padding="10px")

        assert style1 == style2
        assert style1 != style3


class TestStyleSheet:
    """Tests for StyleSheet class."""

    def test_register_style(self):
        """Test registering a style."""
        stylesheet = StyleSheet()
        style = CSSStyle(background_color="blue", color="white")

        class_name = stylesheet.register("btn-primary", style)

        assert class_name == "btn-primary"
        assert stylesheet.has_class("btn-primary")
        assert stylesheet.get_style("btn-primary") == style

    def test_auto_generate_class_name(self):
        """Test auto-generation of class names."""
        stylesheet = StyleSheet()
        style = CSSStyle(color="blue")

        class_name = stylesheet.register(style=style)

        assert class_name.startswith("s-")
        assert stylesheet.has_class(class_name)

    def test_register_bem(self):
        """Test BEM naming convention."""
        stylesheet = StyleSheet()
        style = CSSStyle(color="blue")

        # Block only
        block_class = stylesheet.register_bem("button", style=style)
        assert block_class == "button"

        # Block + Element
        element_class = stylesheet.register_bem("button", element="icon", style=style)
        assert element_class == "button__icon"

        # Block + Modifier
        modifier_class = stylesheet.register_bem(
            "button", modifier="primary", style=style
        )
        assert modifier_class == "button--primary"

        # Block + Element + Modifier
        full_class = stylesheet.register_bem(
            "button", element="icon", modifier="large", style=style
        )
        assert full_class == "button__icon--large"

    def test_render_basic_styles(self):
        """Test rendering basic CSS."""
        stylesheet = StyleSheet()
        stylesheet.register("test", CSSStyle(color="blue", padding="10px"))

        css = stylesheet.render()

        assert ".test {" in css
        assert "color: blue;" in css
        assert "padding: 10px;" in css

    def test_render_with_pseudo_selectors(self):
        """Test rendering with pseudo-selectors."""
        stylesheet = StyleSheet()
        stylesheet.register("btn", CSSStyle(color="blue", _hover=CSSStyle(color="red")))

        css = stylesheet.render()

        assert ".btn {" in css
        assert ".btn:hover {" in css
        assert "color: red;" in css

    def test_render_with_breakpoints(self):
        """Test rendering with responsive breakpoints."""
        stylesheet = StyleSheet()
        stylesheet.register(
            "container", CSSStyle(padding="10px", _md=CSSStyle(padding="20px"))
        )

        css = stylesheet.render()

        assert ".container {" in css
        assert "padding: 10px;" in css
        assert "@media (min-width: 768px)" in css
        assert "padding: 20px;" in css

    def test_render_with_theme(self):
        """Test rendering with theme CSS variables."""
        theme = Theme(colors={"primary": "#007bff"}, spacing={"md": "16px"})
        stylesheet = StyleSheet(theme=theme)

        css = stylesheet.render()

        assert ":root {" in css
        assert "--color-primary: #007bff;" in css
        assert "--spacing-md: 16px;" in css

    def test_to_style_tag(self):
        """Test generating a complete style tag."""
        stylesheet = StyleSheet()
        stylesheet.register("test", CSSStyle(color="blue"))

        tag = stylesheet.to_style_tag()

        assert tag.startswith("<style>")
        assert tag.endswith("</style>")
        assert ".test {" in tag

    def test_unregister(self):
        """Test removing a registered class."""
        stylesheet = StyleSheet()
        stylesheet.register("test", CSSStyle(color="blue"))

        assert stylesheet.has_class("test")
        result = stylesheet.unregister("test")
        assert result is True
        assert not stylesheet.has_class("test")

        # Try removing non-existent class
        result = stylesheet.unregister("non-existent")
        assert result is False

    def test_clear(self):
        """Test clearing all classes."""
        stylesheet = StyleSheet()
        stylesheet.register("test1", CSSStyle(color="blue"))
        stylesheet.register("test2", CSSStyle(color="red"))

        assert stylesheet.count_classes() == 2
        stylesheet.clear()
        assert stylesheet.count_classes() == 0

    def test_get_all_class_names(self):
        """Test getting all class names."""
        stylesheet = StyleSheet()
        stylesheet.register("test1", CSSStyle(color="blue"))
        stylesheet.register("test2", CSSStyle(color="red"))

        names = stylesheet.get_all_class_names()
        assert "test1" in names
        assert "test2" in names
        assert len(names) == 2

    def test_to_dict_and_from_dict(self):
        """Test stylesheet serialization."""
        original = StyleSheet()
        original.register("btn", CSSStyle(color="blue", _hover=CSSStyle(color="red")))

        data = original.to_dict()
        restored = StyleSheet.from_dict(data)

        assert restored.has_class("btn")
        assert restored.get_style("btn")._styles["color"] == "blue"


class TestTheme:
    """Tests for Theme class."""

    def test_create_custom_theme(self):
        """Test creating a custom theme."""
        theme = Theme(
            name="Custom", colors={"primary": "#007bff"}, spacing={"md": "16px"}
        )

        assert theme.name == "Custom"
        assert theme.colors["primary"] == "#007bff"
        assert theme.spacing["md"] == "16px"

    def test_get_css_variables(self):
        """Test CSS variable generation."""
        theme = Theme(
            colors={"primary": "#007bff", "secondary": "#6c757d"},
            spacing={"sm": "8px", "md": "16px"},
        )

        variables = theme.get_css_variables()

        assert variables["--color-primary"] == "#007bff"
        assert variables["--color-secondary"] == "#6c757d"
        assert variables["--spacing-sm"] == "8px"
        assert variables["--spacing-md"] == "16px"

    def test_get_component_style(self):
        """Test getting component styles."""
        theme = Theme(
            components={
                "button": {
                    "primary": CSSStyle(background_color="blue"),
                    "secondary": CSSStyle(background_color="gray"),
                }
            }
        )

        primary = theme.get_component_style("button", "primary")
        assert primary._styles["background-color"] == "blue"

        secondary = theme.get_component_style("button", "secondary")
        assert secondary._styles["background-color"] == "gray"

    def test_modern_preset(self):
        """Test modern preset theme."""
        theme = Theme.modern()

        assert theme.name == "Modern"
        assert "primary" in theme.colors
        assert "body" in theme.typography
        assert "md" in theme.spacing
        assert "button" in theme.components

    def test_classic_preset(self):
        """Test classic preset theme."""
        theme = Theme.classic()

        assert theme.name == "Classic"
        assert "primary" in theme.colors
        assert theme.typography["body"] == "Georgia, 'Times New Roman', Times, serif"

    def test_minimal_preset(self):
        """Test minimal preset theme."""
        theme = Theme.minimal()

        assert theme.name == "Minimal"
        assert theme.colors["primary"] == "#000000"

    def test_to_dict_and_from_dict(self):
        """Test theme serialization."""
        original = Theme(
            name="Test",
            colors={"primary": "#007bff"},
            components={"button": CSSStyle(color="blue")},
        )

        data = original.to_dict()
        restored = Theme.from_dict(data)

        assert restored.name == "Test"
        assert restored.colors["primary"] == "#007bff"
        assert "button" in restored.components


class TestIntegration:
    """Integration tests for the styling system."""

    def test_complete_workflow(self):
        """Test complete styling workflow."""
        # Create theme
        theme = Theme.modern()

        # Create stylesheet with theme
        stylesheet = StyleSheet(theme=theme)

        # Register component styles
        btn_primary = stylesheet.register(
            "btn-primary",
            CSSStyle(
                background_color="var(--color-primary)",
                color="white",
                padding="12px 24px",
                border_radius="6px",
                _hover=CSSStyle(background_color="var(--color-primary-dark)"),
            ),
        )

        # Render CSS
        css = stylesheet.render()

        # Verify output
        assert ":root {" in css
        assert "--color-primary:" in css
        assert ".btn-primary {" in css
        assert ".btn-primary:hover {" in css

    def test_bem_workflow(self):
        """Test BEM naming workflow."""
        stylesheet = StyleSheet()

        # Register BEM classes
        stylesheet.register_bem(
            "card", style=CSSStyle(background="white", padding="20px")
        )
        stylesheet.register_bem(
            "card", element="header", style=CSSStyle(font_weight="bold")
        )
        stylesheet.register_bem("card", element="body", style=CSSStyle(padding="10px"))
        stylesheet.register_bem(
            "card", modifier="featured", style=CSSStyle(border="2px solid blue")
        )

        css = stylesheet.render()

        assert ".card {" in css
        assert ".card__header {" in css
        assert ".card__body {" in css
        assert ".card--featured {" in css
