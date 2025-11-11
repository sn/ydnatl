"""Theme class for YDNATL styling system."""

from typing import Dict, Optional, Any

from .style import CSSStyle


class Theme:
    """
    Represents a design theme with colors, typography, spacing, and component styles.

    Usage:
        # Create custom theme
        theme = Theme(
            name="Custom",
            colors={
                "primary": "#007bff",
                "secondary": "#6c757d"
            }
        )

        # Use with stylesheet
        stylesheet = StyleSheet(theme=theme)

        # Or use preset themes
        theme = Theme.modern()
        theme = Theme.classic()
        theme = Theme.minimal()
    """

    def __init__(
        self,
        name: str = "Default",
        colors: Optional[Dict[str, str]] = None,
        typography: Optional[Dict[str, Any]] = None,
        spacing: Optional[Dict[str, str]] = None,
        components: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a Theme.

        Args:
            name: Theme name
            colors: Color palette (e.g., {"primary": "#007bff"})
            typography: Font settings (e.g., {"body": "Arial, sans-serif"})
            spacing: Spacing scale (e.g., {"sm": "8px", "md": "16px"})
            components: Pre-styled component definitions
        """
        self.name = name
        self.colors = colors or {}
        self.typography = typography or {}
        self.spacing = spacing or {}
        self.components = components or {}

    def get_css_variables(self) -> Dict[str, str]:
        """
        Generate CSS variables from theme properties.

        Returns:
            Dictionary of CSS variable names and values
        """
        variables = {}

        # Color variables
        for key, value in self.colors.items():
            variables[f"--color-{key}"] = value

        # Spacing variables
        for key, value in self.spacing.items():
            variables[f"--spacing-{key}"] = value

        # Typography variables
        if isinstance(self.typography, dict):
            for key, value in self.typography.items():
                if isinstance(value, str):
                    variables[f"--font-{key}"] = value
                elif isinstance(value, dict):
                    # Handle nested typography settings
                    for sub_key, sub_value in value.items():
                        variables[f"--font-{key}-{sub_key}"] = str(sub_value)

        return variables

    def get_component_style(
        self, component: str, variant: str = "default"
    ) -> Optional[CSSStyle]:
        """
        Get a component style from the theme.

        Args:
            component: Component name (e.g., "button", "card")
            variant: Variant name (e.g., "primary", "secondary")

        Returns:
            CSSStyle object or None if not found
        """
        if component not in self.components:
            return None

        comp_styles = self.components[component]

        if isinstance(comp_styles, CSSStyle):
            return comp_styles
        elif isinstance(comp_styles, dict) and variant in comp_styles:
            return comp_styles[variant]

        return None

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize theme to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "colors": self.colors.copy(),
            "typography": self.typography.copy(),
            "spacing": self.spacing.copy(),
            "components": {
                name: (
                    style.to_dict()
                    if isinstance(style, CSSStyle)
                    else {
                        k: v.to_dict() if isinstance(v, CSSStyle) else v
                        for k, v in style.items()
                    }
                )
                for name, style in self.components.items()
            },
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Theme":
        """
        Deserialize theme from dictionary.

        Args:
            data: Dictionary representation

        Returns:
            New Theme object
        """
        # Reconstruct components
        components = {}
        if "components" in data:
            for name, comp_data in data["components"].items():
                if isinstance(comp_data, dict):
                    # Check if it's a style dict or variants dict
                    if "styles" in comp_data:
                        components[name] = CSSStyle.from_dict(comp_data)
                    else:
                        # It's variants
                        components[name] = {
                            k: CSSStyle.from_dict(v) if isinstance(v, dict) else v
                            for k, v in comp_data.items()
                        }

        return cls(
            name=data.get("name", "Default"),
            colors=data.get("colors", {}),
            typography=data.get("typography", {}),
            spacing=data.get("spacing", {}),
            components=components,
        )

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Theme(name='{self.name}')"

    # Preset themes

    @classmethod
    def modern(cls) -> "Theme":
        """
        Modern theme with clean, contemporary design.

        Returns:
            Modern Theme object
        """
        return cls(
            name="Modern",
            colors={
                "primary": "#3b82f6",
                "primary-dark": "#2563eb",
                "secondary": "#8b5cf6",
                "secondary-dark": "#7c3aed",
                "neutral": "#6b7280",
                "success": "#10b981",
                "danger": "#ef4444",
                "warning": "#f59e0b",
                "info": "#3b82f6",
                "light": "#f3f4f6",
                "dark": "#1f2937",
                "white": "#ffffff",
                "black": "#000000",
            },
            typography={
                "body": "Inter, system-ui, -apple-system, sans-serif",
                "heading": "Inter, system-ui, -apple-system, sans-serif",
                "mono": "Consolas, Monaco, 'Courier New', monospace",
                "sizes": {
                    "xs": "12px",
                    "sm": "14px",
                    "base": "16px",
                    "lg": "18px",
                    "xl": "20px",
                    "2xl": "24px",
                    "3xl": "30px",
                    "4xl": "36px",
                },
            },
            spacing={
                "xs": "4px",
                "sm": "8px",
                "md": "16px",
                "lg": "24px",
                "xl": "32px",
                "2xl": "48px",
                "3xl": "64px",
            },
            components={
                "button": {
                    "primary": CSSStyle(
                        background_color="var(--color-primary)",
                        color="var(--color-white)",
                        padding="12px 24px",
                        border_radius="6px",
                        border="none",
                        font_weight="600",
                        cursor="pointer",
                        transition="background-color 0.2s ease",
                        _hover=CSSStyle(background_color="var(--color-primary-dark)"),
                    ),
                    "secondary": CSSStyle(
                        background_color="var(--color-secondary)",
                        color="var(--color-white)",
                        padding="12px 24px",
                        border_radius="6px",
                        border="none",
                        font_weight="600",
                        cursor="pointer",
                        transition="background-color 0.2s ease",
                        _hover=CSSStyle(background_color="var(--color-secondary-dark)"),
                    ),
                },
                "card": CSSStyle(
                    background_color="var(--color-white)",
                    padding="var(--spacing-lg)",
                    border_radius="8px",
                    box_shadow="0 1px 3px rgba(0, 0, 0, 0.1)",
                ),
            },
        )

    @classmethod
    def classic(cls) -> "Theme":
        """
        Classic theme with traditional, timeless design.

        Returns:
            Classic Theme object
        """
        return cls(
            name="Classic",
            colors={
                "primary": "#0066cc",
                "primary-dark": "#004c99",
                "secondary": "#6c757d",
                "secondary-dark": "#5a6268",
                "neutral": "#6c757d",
                "success": "#28a745",
                "danger": "#dc3545",
                "warning": "#ffc107",
                "info": "#17a2b8",
                "light": "#f8f9fa",
                "dark": "#343a40",
                "white": "#ffffff",
                "black": "#000000",
            },
            typography={
                "body": "Georgia, 'Times New Roman', Times, serif",
                "heading": "Georgia, 'Times New Roman', Times, serif",
                "mono": "Courier New, Courier, monospace",
                "sizes": {
                    "xs": "12px",
                    "sm": "14px",
                    "base": "16px",
                    "lg": "18px",
                    "xl": "21px",
                    "2xl": "24px",
                    "3xl": "32px",
                    "4xl": "40px",
                },
            },
            spacing={
                "xs": "4px",
                "sm": "8px",
                "md": "16px",
                "lg": "24px",
                "xl": "32px",
                "2xl": "48px",
                "3xl": "64px",
            },
            components={
                "button": {
                    "primary": CSSStyle(
                        background_color="var(--color-primary)",
                        color="var(--color-white)",
                        padding="10px 20px",
                        border_radius="4px",
                        border="none",
                        font_weight="400",
                        cursor="pointer",
                        transition="background-color 0.3s ease",
                        _hover=CSSStyle(background_color="var(--color-primary-dark)"),
                    ),
                    "secondary": CSSStyle(
                        background_color="var(--color-white)",
                        color="var(--color-primary)",
                        padding="10px 20px",
                        border_radius="4px",
                        border="2px solid var(--color-primary)",
                        font_weight="400",
                        cursor="pointer",
                        transition="all 0.3s ease",
                        _hover=CSSStyle(
                            background_color="var(--color-primary)",
                            color="var(--color-white)",
                        ),
                    ),
                },
                "card": CSSStyle(
                    background_color="var(--color-white)",
                    padding="var(--spacing-lg)",
                    border_radius="4px",
                    border="1px solid var(--color-light)",
                    box_shadow="0 2px 4px rgba(0, 0, 0, 0.05)",
                ),
            },
        )

    @classmethod
    def minimal(cls) -> "Theme":
        """
        Minimal theme with clean, stripped-down design.

        Returns:
            Minimal Theme object
        """
        return cls(
            name="Minimal",
            colors={
                "primary": "#000000",
                "primary-dark": "#333333",
                "secondary": "#666666",
                "secondary-dark": "#444444",
                "neutral": "#999999",
                "success": "#00cc00",
                "danger": "#cc0000",
                "warning": "#cc9900",
                "info": "#0099cc",
                "light": "#f5f5f5",
                "dark": "#1a1a1a",
                "white": "#ffffff",
                "black": "#000000",
            },
            typography={
                "body": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                "heading": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                "mono": "'SF Mono', Monaco, 'Cascadia Code', monospace",
                "sizes": {
                    "xs": "12px",
                    "sm": "14px",
                    "base": "16px",
                    "lg": "18px",
                    "xl": "20px",
                    "2xl": "24px",
                    "3xl": "32px",
                    "4xl": "40px",
                },
            },
            spacing={
                "xs": "4px",
                "sm": "8px",
                "md": "16px",
                "lg": "24px",
                "xl": "32px",
                "2xl": "48px",
                "3xl": "64px",
            },
            components={
                "button": {
                    "primary": CSSStyle(
                        background_color="var(--color-primary)",
                        color="var(--color-white)",
                        padding="8px 16px",
                        border_radius="0px",
                        border="none",
                        font_weight="500",
                        cursor="pointer",
                        transition="opacity 0.2s ease",
                        _hover=CSSStyle(opacity="0.8"),
                    ),
                    "secondary": CSSStyle(
                        background_color="var(--color-white)",
                        color="var(--color-primary)",
                        padding="8px 16px",
                        border_radius="0px",
                        border="1px solid var(--color-primary)",
                        font_weight="500",
                        cursor="pointer",
                        transition="all 0.2s ease",
                        _hover=CSSStyle(
                            background_color="var(--color-primary)",
                            color="var(--color-white)",
                        ),
                    ),
                },
                "card": CSSStyle(
                    background_color="var(--color-white)",
                    padding="var(--spacing-md)",
                    border_radius="0px",
                    border="1px solid var(--color-light)",
                ),
            },
        )
