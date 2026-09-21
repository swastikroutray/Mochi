from .app import DoomPetApp


def main() -> int:
    return DoomPetApp().run()


if __name__ == "__main__":
    raise SystemExit(main())