import unittest

from ydnatl.core.element import HTMLElement
from ydnatl.tags.text import (
    H1,
    H2,
    H3,
    H4,
    H5,
    H6,
    Paragraph,
    Blockquote,
    Pre,
    Quote,
    Cite,
    Em,
    Italic,
    Span,
    Strong,
    Bold,
    Abbr,
    Link,
    Small,
    Superscript,
    Subscript,
    Time,
    Code,
    Del,
    Ins,
    Strikethrough,
    Underline,
    Kbd,
    Samp,
    Var,
    Mark,
    Dfn,
    Br,
    Wbr,
)


class TestTextTags(unittest.TestCase):

    def test_h1_with_attributes(self):
        """Test the creation of an H1 element with attributes."""
        h1 = H1("Heading 1", id="heading-1", class_name="heading-1")
        self.assertEqual(h1.tag, "h1")
        self.assertEqual(str(h1), '<h1 id="heading-1" class="heading-1">Heading 1</h1>')

    def test_h1(self):
        """Test the creation of an H1 element."""
        h1 = H1("Heading 1")
        self.assertEqual(h1.tag, "h1")
        self.assertEqual(str(h1), "<h1>Heading 1</h1>")

    def test_h2(self):
        """Test the creation of an H2 element."""
        h2 = H2("Heading 2")
        self.assertEqual(h2.tag, "h2")
        self.assertEqual(str(h2), "<h2>Heading 2</h2>")

    def test_h3(self):
        """Test the creation of an H3 element."""
        h3 = H3("Heading 3")
        self.assertEqual(h3.tag, "h3")
        self.assertEqual(str(h3), "<h3>Heading 3</h3>")

    def test_h4(self):
        """Test the creation of an H4 element."""
        h4 = H4("Heading 4")
        self.assertEqual(h4.tag, "h4")
        self.assertEqual(str(h4), "<h4>Heading 4</h4>")

    def test_h5(self):
        """Test the creation of an H5 element."""
        h5 = H5("Heading 5")
        self.assertEqual(h5.tag, "h5")
        self.assertEqual(str(h5), "<h5>Heading 5</h5>")

    def test_h6(self):
        """Test the creation of an H6 element."""
        h6 = H6("Heading 6")
        self.assertEqual(h6.tag, "h6")
        self.assertEqual(str(h6), "<h6>Heading 6</h6>")

    def test_paragraph(self):
        """Test the creation of a paragraph element."""
        p = Paragraph("This is a paragraph.")
        self.assertEqual(p.tag, "p")
        self.assertEqual(str(p), "<p>This is a paragraph.</p>")

    def test_blockquote(self):
        """Test the creation of a blockquote element."""
        blockquote = Blockquote("This is a quote.")
        self.assertEqual(blockquote.tag, "blockquote")
        self.assertEqual(str(blockquote), "<blockquote>This is a quote.</blockquote>")

    def test_pre(self):
        """Test the creation of a pre element."""
        pre = Pre("  This is pre-formatted text  ")
        self.assertEqual(pre.tag, "pre")
        self.assertEqual(str(pre), "<pre>  This is pre-formatted text  </pre>")

    def test_quote(self):
        """Test the creation of a quote element."""
        quote = Quote("This is a short quote.")
        self.assertEqual(quote.tag, "q")
        self.assertEqual(str(quote), "<q>This is a short quote.</q>")

    def test_cite(self):
        """Test the creation of a cite element."""
        cite = Cite("Source of the quote")
        self.assertEqual(cite.tag, "cite")
        self.assertEqual(str(cite), "<cite>Source of the quote</cite>")

    def test_em(self):
        """Test the creation of an em element."""
        em = Em("Emphasized text")
        self.assertEqual(em.tag, "em")
        self.assertEqual(str(em), "<em>Emphasized text</em>")

    def test_italic(self):
        """Test the creation of an italic element."""
        italic = Italic("Italic text")
        self.assertEqual(italic.tag, "i")
        self.assertEqual(str(italic), "<i>Italic text</i>")

    def test_span(self):
        """Test the creation of a span element."""
        span = Span("Some text")
        self.assertEqual(span.tag, "span")
        self.assertEqual(str(span), "<span>Some text</span>")

    def test_strong(self):
        """Test the creation of a strong element."""
        strong = Strong("Important text")
        self.assertEqual(strong.tag, "strong")
        self.assertEqual(str(strong), "<strong>Important text</strong>")

    def test_abbr(self):
        """Test the creation of an abbr element."""
        abbr = Abbr("HTML", title="HyperText Markup Language")
        self.assertEqual(abbr.tag, "abbr")
        self.assertEqual(
            str(abbr), '<abbr title="HyperText Markup Language">HTML</abbr>'
        )

    def test_link(self):
        """Test the creation of a link element."""
        link = Link("Visit Google", href="https://www.google.com")
        self.assertEqual(link.tag, "a")
        self.assertEqual(str(link), '<a href="https://www.google.com">Visit Google</a>')

    def test_small(self):
        """Test the creation of a small element."""
        small = Small("Small text")
        self.assertEqual(small.tag, "small")
        self.assertEqual(str(small), "<small>Small text</small>")

    def test_superscript(self):
        """Test the creation of a superscript element."""
        sup = Superscript("2")
        self.assertEqual(sup.tag, "sup")
        self.assertEqual(str(sup), "<sup>2</sup>")

    def test_subscript(self):
        """Test the creation of a subscript element."""
        sub = Subscript("2")
        self.assertEqual(sub.tag, "sub")
        self.assertEqual(str(sub), "<sub>2</sub>")

    def test_time(self):
        """Test the creation of a time element."""
        time = Time("2023-10-01", datetime="2023-10-01T12:00:00Z")
        self.assertEqual(time.tag, "time")
        self.assertEqual(
            str(time), '<time datetime="2023-10-01T12:00:00Z">2023-10-01</time>'
        )

    def test_code(self):
        """Test the creation of a code element."""
        code = Code("print('Hello, World!')")
        self.assertEqual(code.tag, "code")
        # Single quotes are escaped for security (&#x27;)
        self.assertEqual(str(code), "<code>print(&#x27;Hello, World!&#x27;)</code>")

    def test_attributes(self):
        """Test the addition of attributes to text elements."""
        p = Paragraph(
            "This is a paragraph.", id="my-paragraph", class_name="text-style"
        )
        self.assertEqual(
            str(p), '<p id="my-paragraph" class="text-style">This is a paragraph.</p>'
        )

    def test_bold(self):
        """Test the creation of a bold element."""
        bold = Bold("Bold text")
        self.assertEqual(bold.tag, "b")
        self.assertEqual(str(bold), "<b>Bold text</b>")

    def test_del(self):
        """Test the creation of a del element."""
        deleted = Del("Deleted text")
        self.assertEqual(deleted.tag, "del")
        self.assertEqual(str(deleted), "<del>Deleted text</del>")

    def test_ins(self):
        """Test the creation of an ins element."""
        inserted = Ins("Inserted text")
        self.assertEqual(inserted.tag, "ins")
        self.assertEqual(str(inserted), "<ins>Inserted text</ins>")

    def test_strikethrough(self):
        """Test the creation of a strikethrough element."""
        strike = Strikethrough("Strikethrough text")
        self.assertEqual(strike.tag, "s")
        self.assertEqual(str(strike), "<s>Strikethrough text</s>")

    def test_underline(self):
        """Test the creation of an underline element."""
        underline = Underline("Underlined text")
        self.assertEqual(underline.tag, "u")
        self.assertEqual(str(underline), "<u>Underlined text</u>")

    def test_kbd(self):
        """Test the creation of a kbd element."""
        kbd = Kbd("Ctrl+C")
        self.assertEqual(kbd.tag, "kbd")
        self.assertEqual(str(kbd), "<kbd>Ctrl+C</kbd>")

    def test_samp(self):
        """Test the creation of a samp element."""
        samp = Samp("Sample output")
        self.assertEqual(samp.tag, "samp")
        self.assertEqual(str(samp), "<samp>Sample output</samp>")

    def test_var(self):
        """Test the creation of a var element."""
        var = Var("x")
        self.assertEqual(var.tag, "var")
        self.assertEqual(str(var), "<var>x</var>")

    def test_mark(self):
        """Test the creation of a mark element."""
        mark = Mark("Highlighted text")
        self.assertEqual(mark.tag, "mark")
        self.assertEqual(str(mark), "<mark>Highlighted text</mark>")

    def test_dfn(self):
        """Test the creation of a dfn element."""
        dfn = Dfn("Definition term")
        self.assertEqual(dfn.tag, "dfn")
        self.assertEqual(str(dfn), "<dfn>Definition term</dfn>")

    def test_br(self):
        """Test the creation of a br element."""
        br = Br()
        self.assertEqual(br.tag, "br")
        self.assertTrue(br.self_closing)
        self.assertEqual(str(br), "<br />")

    def test_wbr(self):
        """Test the creation of a wbr element."""
        wbr = Wbr()
        self.assertEqual(wbr.tag, "wbr")
        self.assertTrue(wbr.self_closing)
        self.assertEqual(str(wbr), "<wbr />")

    def test_inheritance(self):
        """Test that all text-related classes inherit from HTMLElement."""
        for cls in [
            H1,
            H2,
            H3,
            H4,
            H5,
            H6,
            Paragraph,
            Blockquote,
            Pre,
            Quote,
            Cite,
            Em,
            Italic,
            Span,
            Strong,
            Bold,
            Abbr,
            Link,
            Small,
            Superscript,
            Subscript,
            Time,
            Code,
            Del,
            Ins,
            Strikethrough,
            Underline,
            Kbd,
            Samp,
            Var,
            Mark,
            Dfn,
            Br,
            Wbr,
        ]:
            self.assertTrue(issubclass(cls, HTMLElement))


if __name__ == "__main__":
    unittest.main()
