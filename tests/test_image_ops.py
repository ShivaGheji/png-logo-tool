import unittest
from PIL import Image
from png_logo_tool.cli import margins, resize, trim


class ImageTests(unittest.TestCase):
    def setUp(self):
        self.image = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
        for x in range(3, 7):
            for y in range(2, 8):
                self.image.putpixel((x, y), (20, 30, 40, 255))

    def test_trim(self):
        self.assertEqual(trim(self.image).size, (4, 6))

    def test_individual_padding(self):
        self.assertEqual(margins(self.image, left=2, top=1, right=3, bottom=4).size, (15, 15))

    def test_negative_margin(self):
        self.assertEqual(margins(self.image, left=-1, right=-2).size, (7, 10))

    def test_contain_canvas_size(self):
        self.assertEqual(resize(self.image, width=20, height=20).size, (20, 20))

    def test_stretch_size(self):
        self.assertEqual(resize(self.image, width=20, height=5, fit="stretch").size, (20, 5))


if __name__ == "__main__":
    unittest.main()
