# Modern Control Map for The Witcher 3

> **Modern Control Map is now Modern Control Remapping.** Its next version (1.0.1) and everything after it live in
> [ApocryphaRealm/ModernControlRemappingW3](https://github.com/ApocryphaRealm/ModernControlRemappingW3) and on the same
> Nexus page ([The Witcher 3 mod 13679](https://www.nexusmods.com/witcher3/mods/13679)). Modern Control Remapping
> carries this map and its controls itself and adds the Key Bindings and Controller Scheme features; replace Modern
> Control Map with it, do not run both. This repository stays as the record of 1.0.0.

The owner's controller layout (Xbox), finalized 2026-10-06. It is built on Unbind Vanilla Controls (UVC W3), which adds:
- tap-B dodge in combat and tap-B sprint toggle out of combat;
- X for both swords (tap steel, hold silver);
- the dismount hold that follows its binding;
- the sign buttons for alternative sign casting.

- `map/input.settings`: the profile's input.settings as finalized (MO2 profile `Default`).
- `banners/`: one 1920x1080 diagram per context: Exploration, Combat, Horseback, Swimming & Diving, Sailing, Sign Casting.
  They're drawn in AMF's Skellige theme, with its frame art.
- `tools/make_banners.py`: regenerates the banners (`python -I tools/make_banners.py banners`, needs Chrome).

Game options the map expects: Options > Controls > Left Stick Sprint **off**; Options > Gameplay > alternative sign
casting **on** (for the Sign Casting banner).

Changes to the map are made as exact-line edits of the profile's input.settings with MO2 and the game closed (the
game will not rebind a controller control once it is unbound).
