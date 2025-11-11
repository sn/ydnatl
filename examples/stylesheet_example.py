"""Example demonstrating the StyleSheet system in YDNATL."""

from ydnatl import *
from ydnatl.styles import CSSStyle, StyleSheet, Theme


def basic_stylesheet_example():
    """Basic example of using StyleSheet."""
    print("=== Basic StyleSheet Example ===\n")

    # Create stylesheet
    stylesheet = StyleSheet()

    # Register button styles
    btn_primary = stylesheet.register(
        "btn-primary",
        CSSStyle(
            background_color="#007bff",
            color="white",
            padding="10px 20px",
            border_radius="5px",
            border="none",
            font_weight="600",
            cursor="pointer",
            _hover=CSSStyle(background_color="#0056b3"),
        ),
    )

    btn_secondary = stylesheet.register(
        "btn-secondary",
        CSSStyle(
            background_color="#6c757d",
            color="white",
            padding="10px 20px",
            border_radius="5px",
            border="none",
            font_weight="600",
            cursor="pointer",
            _hover=CSSStyle(background_color="#5a6268"),
        ),
    )

    # Create HTML using the registered classes
    page = HTML(
        Head(Title("StyleSheet Example"), Style(stylesheet.render())),
        Body(
            Div(
                H1("Button Examples"),
                Button("Primary Button", class_name=btn_primary),
                Button("Secondary Button", class_name=btn_secondary),
            )
        ),
    )

    print(page.render(pretty=True))


def theme_example():
    """Example using preset themes."""
    print("\n\n=== Theme Example ===\n")

    # Use a preset theme
    theme = Theme.modern()

    # Create stylesheet with theme
    stylesheet = StyleSheet(theme=theme)

    # Register styles that use theme variables
    btn = stylesheet.register(
        "btn",
        CSSStyle(
            background_color="var(--color-primary)",
            color="var(--color-white)",
            padding="var(--spacing-md)",
            border_radius="6px",
            font_family="var(--font-body)",
            border="none",
            cursor="pointer",
            _hover=CSSStyle(background_color="var(--color-primary-dark)"),
        ),
    )

    card = stylesheet.register(
        "card",
        CSSStyle(
            background_color="var(--color-white)",
            padding="var(--spacing-lg)",
            border_radius="8px",
            box_shadow="0 1px 3px rgba(0, 0, 0, 0.1)",
            margin="var(--spacing-md)",
        ),
    )

    # Create HTML
    page = HTML(
        Head(Title("Theme Example"), Style(stylesheet.render())),
        Body(
            Div(
                H2("Welcome"),
                Paragraph("This card uses theme variables."),
                Button("Click Me", class_name=btn),
                class_name=card,
            ),
            Div(
                H2("Another Card"),
                Paragraph("Consistent styling across components."),
                Button("Learn More", class_name=btn),
                class_name=card,
            ),
        ),
    )

    print(page.render(pretty=True))


def bem_example():
    """Example using BEM naming convention."""
    print("\n\n=== BEM Example ===\n")

    stylesheet = StyleSheet()

    # Register BEM styles
    card = stylesheet.register_bem(
        "card",
        style=CSSStyle(
            background="white",
            border_radius="8px",
            box_shadow="0 2px 4px rgba(0,0,0,0.1)",
            overflow="hidden",
        ),
    )

    card_header = stylesheet.register_bem(
        "card",
        element="header",
        style=CSSStyle(
            padding="20px",
            background="#f8f9fa",
            border_bottom="1px solid #dee2e6",
            font_weight="bold",
        ),
    )

    card_body = stylesheet.register_bem(
        "card", element="body", style=CSSStyle(padding="20px")
    )

    card_footer = stylesheet.register_bem(
        "card",
        element="footer",
        style=CSSStyle(
            padding="20px", background="#f8f9fa", border_top="1px solid #dee2e6"
        ),
    )

    card_featured = stylesheet.register_bem(
        "card", modifier="featured", style=CSSStyle(border="3px solid #007bff")
    )

    # Create HTML using BEM classes
    page = HTML(
        Head(Title("BEM Example"), Style(stylesheet.render())),
        Body(
            H1("BEM Card Examples"),
            # Regular card
            Div(
                Div("Card Header", class_name=card_header),
                Div(Paragraph("Card body content goes here."), class_name=card_body),
                Div("Card Footer", class_name=card_footer),
                class_name=card,
            ),
            # Featured card
            Div(
                Div("Featured Card", class_name=card_header),
                Div(
                    Paragraph("This is a featured card with special styling."),
                    class_name=card_body,
                ),
                Div("Footer", class_name=card_footer),
                class_name=f"{card} {card_featured}",
            ),
        ),
    )

    print(page.render(pretty=True))


def responsive_example():
    """Example with responsive breakpoints."""
    print("\n\n=== Responsive Example ===\n")

    stylesheet = StyleSheet()

    # Register responsive styles
    container = stylesheet.register(
        "container",
        CSSStyle(
            padding="10px",
            margin="0 auto",
            _sm=CSSStyle(padding="15px", max_width="640px"),
            _md=CSSStyle(padding="20px", max_width="768px"),
            _lg=CSSStyle(padding="30px", max_width="1024px"),
        ),
    )

    grid = stylesheet.register(
        "grid",
        CSSStyle(
            display="grid",
            grid_template_columns="1fr",
            gap="10px",
            _md=CSSStyle(grid_template_columns="1fr 1fr"),
            _lg=CSSStyle(grid_template_columns="1fr 1fr 1fr"),
        ),
    )

    # Create HTML
    page = HTML(
        Head(
            Title("Responsive Example"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Style(stylesheet.render()),
        ),
        Body(
            Div(
                H1("Responsive Grid"),
                Div(
                    Div("Item 1"),
                    Div("Item 2"),
                    Div("Item 3"),
                    Div("Item 4"),
                    Div("Item 5"),
                    Div("Item 6"),
                    class_name=grid,
                ),
                class_name=container,
            )
        ),
    )

    print(page.render(pretty=True))


def combined_with_inline_example():
    """Example combining stylesheet classes with inline styles."""
    print("\n\n=== Combined Stylesheet + Inline Example ===\n")

    stylesheet = StyleSheet()

    # Register base button style
    btn = stylesheet.register(
        "btn",
        CSSStyle(
            padding="10px 20px",
            border_radius="5px",
            border="none",
            font_weight="600",
            cursor="pointer",
        ),
    )

    # Create HTML using both class and inline styles
    page = HTML(
        Head(Title("Combined Example"), Style(stylesheet.render())),
        Body(
            H1("Combining Stylesheet and Inline Styles"),
            # Base class + inline override
            Button("Blue Button", class_name=btn).add_styles(
                {"background-color": "#007bff", "color": "white"}
            ),
            # Same base class, different inline styles
            Button("Green Button", class_name=btn).add_styles(
                {"background-color": "#28a745", "color": "white"}
            ),
            # Same base class, more inline overrides
            Button("Large Red Button", class_name=btn).add_styles(
                {
                    "background-color": "#dc3545",
                    "color": "white",
                    "padding": "15px 30px",
                    "font-size": "18px",
                }
            ),
        ),
    )

    print(page.render(pretty=True))


if __name__ == "__main__":
    basic_stylesheet_example()
    theme_example()
    bem_example()
    responsive_example()
    combined_with_inline_example()
