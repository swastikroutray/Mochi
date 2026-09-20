# Designing Mochi

Mochi is intentionally made with **HTML + CSS + SVG + JavaScript** so you can edit the cat visually in VS Code.

## Change the look

Open `style.css` and start with these variables:

```css
:root {
  --fur: #171717;
  --fur-soft: #252525;
  --eye: #fafafa;
  --pupil: #171717;
}
```

The main body shape is in `index.html` as SVG paths. The reference design is a simple black cat silhouette with pointed ears, large white eyes and a curled tail.

## Preview without Python

Open `index.html` in a browser. You can inspect and edit the SVG/CSS while developing. The desktop drag bridge is only active when DoomPets launches the page inside PySide6 WebEngine.

## Add new expressions

The engine currently sends:

- `normal`
- `concerned`
- `angry`
- `happy`

Add CSS rules with `.state-yourstate` and then add the same state to the Python state logic/config.
