# ModernControlMapW3 - changelog

Rule 61: this mod's own history, kept beside the code it describes.

<!-- VERSIONING-RULES -->
> **Versioning rules (CLAUDE.md rules 6 and 48):** `X.Y.Z`; a change increments the THIRD
> number; at `.9` the MINOR rolls. The next number is LAST WORKING + 1; failed/scratch/
> untested numbers are reused. Numbers come from version-gate.ps1.

## 1.0.0 - 2026-10-06 - untested

First build (the owner, 2026-10-06: *"finalize the control map we just made ... call it like modern control map for
The Witcher 3"*; *"the current control map shouldn't require UVC it should just come as a control map that's not
rebindable"*; download: a controller-only installer).

### Added
- **The map**: the owner's controller layout, built session by session in Unbind Vanilla Controls' test runs. 250
  controller bindings across every context, kept as the difference from the game's own pad lines (`tools\build_map.py`
  -> `map.json`).
- **Installer**: sets those bindings in input.settings with the game closed and leaves the keyboard alone. Each changed
  file is backed up first, and the uninstaller restores the first backups. It also turns Left Stick Sprint off and
  alternative sign casting on. Each empty pad slot is written as an IK_None line with the action's own State/IdleTime, as the map has it. Tested
  on a copy of the game's default file: every binding line of the map is in the result, nothing else changed except
  the game's own gesture and Steam-controller lines being kept, and a second run changes nothing. Main Agent's run on
  the defaults found the first build missing 56 such IK_None lines; fixed.
- **Script**, moved here from Unbind Vanilla Controls:
  - out-of-combat tap-to-toggle sprint;
  - both swords on one button (tap steel, hold silver);
  - the dismount hold circle follows its binding;
  - sign buttons while Cast Sign is held, with Jump held back.
- **Banners**: one per context, in AMF's Skellige theme.
