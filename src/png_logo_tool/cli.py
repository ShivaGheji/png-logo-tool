"""Recolor, resize, trim, and adjust transparent PNG margins."""
import argparse
from pathlib import Path
from PIL import Image


def hex_color(value):
    value = value.strip().removeprefix("#")
    if len(value) != 6:
        raise argparse.ArgumentTypeError("Use a 6-digit hex color, e.g. #FF3030")
    try:
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Invalid hex color") from exc


def trim(image):
    bounds = image.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("Image is fully transparent; nothing to trim.")
    return image.crop(bounds)


def margins(image, left=0, top=0, right=0, bottom=0):
    cl, ct, cr, cb = max(0, -left), max(0, -top), max(0, -right), max(0, -bottom)
    if cl + cr >= image.width or ct + cb >= image.height:
        raise ValueError("Cropping would remove the entire image.")
    if any((cl, ct, cr, cb)):
        image = image.crop((cl, ct, image.width-cr, image.height-cb))
    pl, pt, pr, pb = max(0, left), max(0, top), max(0, right), max(0, bottom)
    if any((pl, pt, pr, pb)):
        canvas = Image.new("RGBA", (image.width+pl+pr, image.height+pt+pb), (0, 0, 0, 0))
        canvas.alpha_composite(image, (pl, pt))
        image = canvas
    return image


def resize(image, width=None, height=None, fit="contain"):
    if width is None and height is None:
        return image
    if width is not None and width <= 0 or height is not None and height <= 0:
        raise ValueError("Width and height must be greater than zero.")
    ow, oh = image.size
    if width is None:
        width = max(1, round(ow * height / oh))
    if height is None:
        height = max(1, round(oh * width / ow))
    if fit == "stretch":
        return image.resize((width, height), Image.Resampling.LANCZOS)
    scale = min(width / ow, height / oh)
    nw, nh = max(1, round(ow * scale)), max(1, round(oh * scale))
    image = image.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    canvas.alpha_composite(image, ((width-nw)//2, (height-nh)//2))
    return canvas


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--color", type=hex_color, help='RGB hex color, e.g. "#FF3030"')
    p.add_argument("--trim", action="store_true", help="Remove fully transparent outer margins")
    p.add_argument("--left", type=int, default=0, help="Margin px: positive adds space, negative crops")
    p.add_argument("--right", type=int, default=0, help="Margin px: positive adds space, negative crops")
    p.add_argument("--top", type=int, default=0, help="Margin px: positive adds space, negative crops")
    p.add_argument("--bottom", type=int, default=0, help="Margin px: positive adds space, negative crops")
    p.add_argument("--horizontal-padding", type=int, help="Set left and right margins equally")
    p.add_argument("--vertical-padding", type=int, help="Set top and bottom margins equally")
    p.add_argument("--width", type=int, help="Output width; height is calculated if omitted")
    p.add_argument("--height", type=int, help="Output height; width is calculated if omitted")
    p.add_argument("--fit", choices=("contain", "stretch"), default="contain",
                   help="contain preserves proportions; stretch may distort the logo")
    a = p.parse_args()
    try:
        if not a.input.is_file():
            raise FileNotFoundError(f"Input not found: {a.input}")
        with Image.open(a.input) as source:
            image = source.convert("RGBA")
        if a.trim:
            image = trim(image)
        if a.color is not None:
            alpha = image.getchannel("A")
            image = Image.new("RGBA", image.size, (*a.color, 255))
            image.putalpha(alpha)
        left, right, top, bottom = a.left, a.right, a.top, a.bottom
        if a.horizontal_padding is not None:
            left = right = a.horizontal_padding
        if a.vertical_padding is not None:
            top = bottom = a.vertical_padding
        image = margins(image, left=left, right=right, top=top, bottom=bottom)
        image = resize(image, width=a.width, height=a.height, fit=a.fit)
        a.output.parent.mkdir(parents=True, exist_ok=True)
        image.save(a.output, "PNG")
        print(f"Saved {a.output} ({image.width}x{image.height}px, RGBA PNG).")
    except (OSError, ValueError) as exc:
        p.error(str(exc))


if __name__ == "__main__":
    main()
