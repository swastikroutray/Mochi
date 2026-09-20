from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_mochi_pack_files_exist():
    pack = ROOT / "pets" / "mochi"
    assert (pack / "index.html").exists()
    assert (pack / "style.css").exists()
    assert (pack / "script.js").exists()
    assert (pack / "design.md").exists()


def test_reference_cat_uses_svg():
    html = (ROOT / "pets" / "mochi" / "index.html").read_text(encoding="utf-8")
    assert "<svg" in html
    assert "class=\"tail\"" in html
    assert "eye-white" in html
