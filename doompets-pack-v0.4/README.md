# DoomPets 🐾

A tiny open-source desktop pet that reacts to your computer habits and tries to stop doomscrolling.

## v0.4 — Interactive HTML/CSS Mochi

Mochi is now rendered as **HTML + CSS + SVG + JavaScript** instead of being drawn with Python. This makes the pet much easier to redesign and lets contributors create their own pet packs.

The reference style is a minimal black cartoon cat: pointed ears, large white eyes, compact body, and a curled tail.

### Features

- Transparent always-on-top desktop overlay
- HTML/CSS/SVG cat with idle bob + blinking
- Hover = petting/purring animation
- Click = playful interaction
- Double click = special reaction
- Drag = pick up and move Mochi anywhere on the desktop
- Cursor direction = Mochi looks left/right/up
- States: normal, concerned, angry, happy
- Active-window based doom/productive classification
- Pet design files are easy to edit in VS Code

## Run locally on Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e .
doompet
```

The first install is larger than v0.2 because DoomPets now uses **PySide6-WebEngine** to render the HTML/CSS pet.

## Customize Mochi

Open:

```text
pets/mochi/index.html
pets/mochi/style.css
pets/mochi/script.js
```

For a quick color change, edit the CSS variables at the top of `style.css`.

For the shape, edit the SVG paths in `index.html`.

See `pets/mochi/design.md` for the design guide.

## Project direction

```text
doompets/
├── engine             # Python desktop + behavior engine
├── pets/
│   └── mochi/         # HTML/CSS/JS pet pack
└── tests/
```

The long-term goal is a community pet-pack ecosystem where people can publish cats, dogs, frogs, pandas, and other companions without changing the core engine.

## Roadmap

- [ ] Real scrolling detection instead of only active-window detection
- [ ] Pet-pack manifest/spec
- [ ] Sprite sheets / richer SVG animations
- [ ] Settings dashboard
- [ ] Persistent pet position
- [ ] Cross-platform support

## License

MIT
