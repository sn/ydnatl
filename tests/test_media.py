import unittest

from ydnatl.core.element import HTMLElement
from ydnatl.tags.media import (
    Image,
    Video,
    Audio,
    Source,
    Track,
    Picture,
    Figure,
    Figcaption,
    Canvas,
    Embed,
    Object,
    Param,
    Map,
    Area,
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

    def test_track(self):
        """Test the creation of a track element."""
        track = Track(
            kind="subtitles", src="subtitles_en.vtt", srclang="en", label="English"
        )
        self.assertEqual(track.tag, "track")
        self.assertTrue(track.self_closing)
        self.assertIn('kind="subtitles"', str(track))
        self.assertIn('src="subtitles_en.vtt"', str(track))

    def test_video_with_track(self):
        """Test video element with track for subtitles."""
        video = Video(
            Source(src="video.mp4", type="video/mp4"),
            Track(kind="subtitles", src="subtitles_en.vtt", srclang="en"),
            controls="controls",
        )
        self.assertIn("<track", str(video))
        self.assertIn("subtitles", str(video))

    def test_embed(self):
        """Test the creation of an embed element."""
        embed = Embed(src="file.swf", type="application/x-shockwave-flash")
        self.assertEqual(embed.tag, "embed")
        self.assertTrue(embed.self_closing)
        self.assertIn('src="file.swf"', str(embed))

    def test_object(self):
        """Test the creation of an object element."""
        obj = Object(data="movie.swf", type="application/x-shockwave-flash")
        self.assertEqual(obj.tag, "object")
        self.assertIn('data="movie.swf"', str(obj))

    def test_param(self):
        """Test the creation of a param element."""
        param = Param(name="autoplay", value="true")
        self.assertEqual(param.tag, "param")
        self.assertTrue(param.self_closing)
        self.assertIn('name="autoplay"', str(param))
        self.assertIn('value="true"', str(param))

    def test_object_with_param(self):
        """Test object element with param children."""
        obj = Object(
            Param(name="autoplay", value="true"),
            Param(name="loop", value="false"),
            data="movie.swf",
        )
        self.assertIn("<param", str(obj))
        self.assertIn("autoplay", str(obj))

    def test_map(self):
        """Test the creation of a map element."""
        image_map = Map(name="workmap")
        self.assertEqual(image_map.tag, "map")
        self.assertIn('name="workmap"', str(image_map))

    def test_area(self):
        """Test the creation of an area element."""
        area = Area(shape="rect", coords="34,44,270,350", href="link.html", alt="Link")
        self.assertEqual(area.tag, "area")
        self.assertTrue(area.self_closing)
        self.assertIn('shape="rect"', str(area))
        self.assertIn('coords="34,44,270,350"', str(area))

    def test_map_with_areas(self):
        """Test map element with multiple area children."""
        image_map = Map(
            Area(shape="rect", coords="34,44,270,350", href="link1.html"),
            Area(shape="circle", coords="130,136,60", href="link2.html"),
            name="workmap",
        )
        self.assertIn("<area", str(image_map))
        self.assertIn("rect", str(image_map))
        self.assertIn("circle", str(image_map))

    def test_inheritance(self):
        """Test that all media-related classes inherit from HTMLElement."""
        for cls in [
            Image,
            Video,
            Audio,
            Source,
            Track,
            Picture,
            Figure,
            Figcaption,
            Canvas,
            Embed,
            Object,
            Param,
            Map,
            Area,
        ]:
            self.assertTrue(issubclass(cls, HTMLElement))


if __name__ == "__main__":
    unittest.main()
