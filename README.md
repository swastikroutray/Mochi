# DoomPets

A small desktop pet that reacts to your computer habits and nudges you away from doomscrolling.

## v0.4 — HTML/CSS Mochi

Mochi is now rendered with HTML, CSS, SVG, and JavaScript instead of being drawn in Python. This makes the pet easier to redesign and lets contributors build their own pet packs without touching the core engine.

The reference design is a minimal black cartoon cat: pointed ears, large white eyes, a compact body, and a curled tail.

### Features

- Transparent, always-on-top desktop overlay
- HTML/CSS/SVG cat with idle bob and blinking
- Hover triggers a petting/purring animation
- Click and double-click trigger playful reactions
- Drag to move Mochi anywhere on the desktop
- Cursor tracking — Mochi looks left, right, or up depending on pointer position
- Four states: normal, concerned, angry, happy
- Active-window classification (doomscrolling vs. productive)
- Pet packs are plain HTML/CSS/JS, editable in any code editor

## Installation (Windows)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e .
doompet
```

The install is larger than v0.2 because DoomPets now depends on **PySide6-WebEngine** to render the pet.

## Customizing Mochi

Pet files live in:

```
pets/mochi/index.html
pets/mochi/style.css
pets/mochi/script.js
```

- For colors, edit the CSS variables at the top of `style.css`.
- For shape, edit the SVG paths in `index.html`.
- For general design guidelines, see `pets/mochi/design.md`.

## Project layout

```
doompets/
├── engine        # Python desktop app and behavior engine
├── pets/
│   └── mochi/    # HTML/CSS/JS pet pack
└── tests/
```

The goal is a community pet-pack ecosystem — cats, dogs, frogs, pandas, and anything else — without requiring changes to the core engine.

## License

MIT