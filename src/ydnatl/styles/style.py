"""CSS Style class for YDNATL."""

from typing import Dict, Any


class CSSStyle:
    """
    Represents CSS styles with support for pseudo-selectors and responsive breakpoints.

    Usage:
        # Basic styles
        style = CSSStyle(
            background_color="#007bff",
            color="white",
            padding="10px 20px"
        )

        # With pseudo-selectors
        style = CSSStyle(
            background_color="#007bff",
            _hover=CSSStyle(background_color="#0056b3"),
            _active=CSSStyle(transform="scale(0.98)")
        )

        # With responsive breakpoints
        style = CSSStyle(
            padding="10px",
            _sm=CSSStyle(padding="15px"),
            _md=CSSStyle(padding="20px")
        )
    """

    def __init__(self, **kwargs):
        """
        Initialize a CSSStyle object.

        Args:
            **kwargs: CSS properties as keyword arguments. Use underscores for hyphens.
                     Pseudo-selectors start with underscore (e.g., _hover, _active)
                     Breakpoints start with underscore (e.g., _sm, _md, _lg)
        """
        self._styles: Dict[str, str] = {}
        self._pseudo: Dict[str, "CSSStyle"] = {}
        self._breakpoints: Dict[str, "CSSStyle"] = {}

        # Known pseudo-selectors
        PSEUDO_SELECTORS = {
            "_hover",
            "_active",
            "_focus",
            "_visited",
            "_link",
            "_first_child",
            "_last_child",
            "_nth_child",
            "_before",
            "_after",
        }

        BREAKPOINTS = {"_xs", "_sm", "_md", "_lg", "_xl", "_2xl"}

        for key, value in kwargs.items():
            if isinstance(value, CSSStyle):
                if key in PSEUDO_SELECTORS:
                    self._pseudo[key[1:].replace("_", "-")] = value
                elif key in BREAKPOINTS:
                    self._breakpoints[key[1:]] = value
            else:
                self._styles[self._to_css_prop(key)] = str(value)

    def _to_css_prop(self, prop: str) -> str:
        """
        Convert Python snake_case to CSS kebab-case.

        Args:
            prop: Property name in snake_case

        Returns:
            Property name in kebab-case
        """
        return prop.replace("_", "-")

    def merge(self, other: "CSSStyle") -> "CSSStyle":
        """
        Merge another CSSStyle object into this one, returning a new CSSStyle.
        The other style's properties will override this one's.

        Args:
            other: Another CSSStyle object to merge

        Returns:
            New CSSStyle object with merged properties
        """
        merged = CSSStyle()
        merged._styles = {**self._styles, **other._styles}
        merged._pseudo = {**self._pseudo, **other._pseudo}
        merged._breakpoints = {**self._breakpoints, **other._breakpoints}
        return merged

    def to_inline(self) -> str:
        """
        Generate inline style string (for style="..." attribute).
        Note: This only includes base styles, not pseudo-selectors or breakpoints.

        Returns:
            CSS string suitable for inline styles
        """
        if not self._styles:
            return ""
        return "; ".join(f"{k}: {v}" for k, v in self._styles.items())

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize to JSON-compatible dictionary.

        Returns:
            Dictionary representation of the style
        """
        result = {"styles": self._styles}

        if self._pseudo:
            result["pseudo"] = {k: v.to_dict() for k, v in self._pseudo.items()}

        if self._breakpoints:
            result["breakpoints"] = {
                k: v.to_dict() for k, v in self._breakpoints.items()
            }

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CSSStyle":
        """
        Deserialize from dictionary.

        Args:
            data: Dictionary representation from to_dict()

        Returns:
            New CSSStyle object
        """
        style = cls()
        style._styles = data.get("styles", {})

        if "pseudo" in data:
            for key, value in data["pseudo"].items():
                style._pseudo[key] = cls.from_dict(value)

        if "breakpoints" in data:
            for key, value in data["breakpoints"].items():
                style._breakpoints[key] = cls.from_dict(value)

        return style

    def has_pseudo_or_breakpoints(self) -> bool:
        """
        Check if this style has pseudo-selectors or breakpoints.
        Useful for deciding whether to extract to external stylesheet.

        Returns:
            True if style has pseudo-selectors or breakpoints
        """
        return bool(self._pseudo or self._breakpoints)

    def is_complex(self, threshold: int = 3) -> bool:
        """
        Check if this style is complex (has many properties).
        Useful for deciding whether to extract to external stylesheet.

        Args:
            threshold: Number of properties to consider complex

        Returns:
            True if style has more properties than threshold
        """
        return len(self._styles) > threshold

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"CSSStyle({self.to_inline()})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another CSSStyle."""
        if not isinstance(other, CSSStyle):
            return False
        return (
            self._styles == other._styles
            and self._pseudo == other._pseudo
            and self._breakpoints == other._breakpoints
        )

    def __hash__(self) -> int:
        """Make CSSStyle hashable for use in dictionaries."""
        styles_tuple = tuple(sorted(self._styles.items()))
        return hash(styles_tuple)
