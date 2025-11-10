import unittest

from ydnatl.core.element import HTMLElement
from ydnatl.tags.media import (
    Image,
    Video,
    Audio,
    Source,
    Picture,
    Figure,
    Figcaption,
    Canvas,
)


class TestMediaTags(unittest.TestCase):

    def test_image(self):
        """Test the creation of an image element."""
        img = Image(src="image.jpg", alt="An image")
        self.assertEqual(img.tag, "img")
        self.assertTrue(img.self_closing)
        self.assertEqual(str(img), '<img src="image.jpg" alt="An image" />')

    def test_video(self):
        """Test the creation of a video element."""
        video = Video(src="video.mp4", controls="controls")
        self.assertEqual(video.tag, "video")
        self.assertEqual(
            str(video), '<video src="video.mp4" controls="controls"></video>'
        )

    def test_audio(self):
        """Test the creation of an audio element."""
        audio = Audio(src="audio.mp3", controls="controls")
        self.assertEqual(audio.tag, "audio")
        self.assertEqual(
            str(audio), '<audio src="audio.mp3" controls="controls"></audio>'
        )

    def test_source(self):
        """Test the creation of a source element."""
        source = Source(src="video.webm", type="video/webm")
        self.assertEqual(source.tag, "source")
        self.assertEqual(str(source), '<source src="video.webm" type="video/webm" />')

    def test_picture(self):
        """Test the creation of a picture element."""
        picture = Picture(
            Source(srcset="image.webp", type="image/webp"),
            Source(srcset="image.jpg", type="image/jpeg"),
            Image(src="fallback.jpg", alt="Fallback image"),
        )
        self.assertEqual(picture.tag, "picture")
        expected = (
            "<picture>"
            '<source srcset="image.webp" type="image/webp" />'
            '<source srcset="image.jpg" type="image/jpeg" />'
            '<img src="fallback.jpg" alt="Fallback image" />'
            "</picture>"
        )
        self.assertEqual(str(picture), expected)

    def test_figure(self):
        """Test the creation of a figure element."""
        figure = Figure(
            Image(src="image.jpg", alt="An image"),
            Figcaption("A caption for the image"),
        )
        self.assertEqual(figure.tag, "figure")
        expected = (
            "<figure>"
            '<img src="image.jpg" alt="An image" />'
            "<figcaption>A caption for the image</figcaption>"
            "</figure>"
        )
        self.assertEqual(str(figure), expected)

    def test_figcaption(self):
        """Test the creation of a figcaption element."""
        figcaption = Figcaption("A caption")
        self.assertEqual(figcaption.tag, "figcaption")
        self.assertEqual(str(figcaption), "<figcaption>A caption</figcaption>")

    def test_canvas(self):
        """Test the creation of a canvas element."""
        canvas = Canvas(width="300", height="150")
        self.assertEqual(canvas.tag, "canvas")
        self.assertEqual(str(canvas), '<canvas width="300" height="150"></canvas>')

    def test_attributes(self):
        """Test the addition of attributes to media elements."""
        video = Video(id="my-video", class_name="video-player", src="video.mp4")
        self.assertEqual(
            str(video),
            '<video id="my-video" class="video-player" src="video.mp4"></video>',
        )

    def test_inheritance(self):
        """Test that all media-related classes inherit from HTMLElement."""
        for cls in [Image, Video, Audio, Source, Picture, Figure, Figcaption, Canvas]:
            self.assertTrue(issubclass(cls, HTMLElement))


if __name__ == "__main__":
    unittest.main()
