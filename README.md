# PNG Logo Tool

A small Python command-line utility to recolor, resize, trim, and adjust transparent margins around PNG logos. Useful for boot-screen assets, icons, overlays, and other transparent images.

## Features

- Recolor visible pixels using a six-digit RGB hex color while preserving transparency.
- Resize by width or height while preserving aspect ratio.
- Fit within a target canvas or stretch to exact dimensions.
- Remove fully transparent margins.
- Add or crop space independently on the top, bottom, left, and right.
- Set equal horizontal or vertical padding.
- Keep the input file unchanged by default.

## Requirements

Python 3.10+.

## Install from source

```bash
git clone https://github.com/YOUR-USERNAME/png-logo-tool.git
cd png-logo-tool
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Replace `YOUR-USERNAME` with your GitHub username. The command `png-logo-tool --help` shows all options.

On Arch Linux / Omarchy, for a source-only workflow, install Pillow with `sudo pacman -S python-pillow`, then run commands using `PYTHONPATH=src python -m png_logo_tool.cli ...`.

## Quick examples

```bash
# Recolor red
png-logo-tool logo.png logo-red.png --color "#FF3030"

# Trim fully transparent outer margins
png-logo-tool logo.png logo-trimmed.png --trim

# Add 20 px left, 30 px right, 5 px top, 10 px bottom
png-logo-tool logo.png logo-padded.png --left 20 --right 30 --top 5 --bottom 10

# Add 10 px above and below
png-logo-tool logo.png logo-vertical.png --vertical-padding 10

# Remove 10 px left/right and 5 px top/bottom (may crop artwork)
png-logo-tool logo.png logo-cropped.png --left -10 --right -10 --top -5 --bottom -5

# Width only: height follows automatically
png-logo-tool logo.png logo-1000.png --width 1000

# Fit inside a 1200 x 400 transparent canvas without distortion
png-logo-tool logo.png logo-fit.png --width 1200 --height 400

# Force exact dimensions (may distort artwork)
png-logo-tool logo.png logo-stretched.png --width 1200 --height 400 --fit stretch

# Combine operations
png-logo-tool shiva_transparent.png shiva-red.png --color "#FF3030" --trim --horizontal-padding 20 --vertical-padding 10 --width 1200
```

## How margins work

Positive margin values add transparent pixels. Negative values crop from that edge and can cut into the visible artwork. `--trim` removes fully transparent outer margins before margin changes. `--horizontal-padding N` sets both left and right margins to `N`; `--vertical-padding N` sets top and bottom. These shortcuts override the corresponding individual values.

Operations are applied in this order: load image as RGBA, trim if requested, recolor if requested, apply margins, resize, save PNG.

`--fit contain` is the default when both dimensions are specified: it creates the exact target canvas and fits the image inside without distortion. `--fit stretch` forces the artwork to the exact dimensions and may distort it.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Troubleshooting

- `command not found`: activate `.venv` and run `python -m pip install -e .`.
- `No module named PIL`: install the project dependencies.
- Background remains visible: `--trim` only removes fully transparent pixels; it does not remove a solid black or colored background.
- Logo looks distorted: use the default `contain` instead of `--fit stretch`.
- Lettering gets cropped: avoid negative margins, or use `--trim` followed by positive padding.

## License

MIT. See [LICENSE](LICENSE).
