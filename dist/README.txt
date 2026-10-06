Modern Control Map (The Witcher 3: Wild Hunt)
Version 0.0.0

A complete controller layout for The Witcher 3, built for the way modern action games are played: attacks on the
triggers and bumpers, signs on the face buttons, and every context - on foot, in combat, on horseback, in the water and
at sea - laid out to match. Xbox button names; the same positions on any controller the game supports.

THE LAYOUT
  Exploration   LT cast sign · L-Stick hold Witcher Senses, press twice call Roach · D-pad Up quick item
                RT strong attack · RB fast attack · Y jump / climb · X swords · B sprint · A interact
  Combat        LT cast sign · LB parry · L-Stick quick item · RT strong attack · RB fast attack
                X swords · B tap dodge, hold run · A roll
  Horseback     LT cast sign · D-pad Up Witcher Senses · RT attack · RB crossbow · Y jump
                X swords · B canter / gallop · A hold to dismount
  Swimming      D-pad Up Witcher Senses · L-Stick crossbow · B dive / swim fast · Y surface / climb out
  Sailing       A speed up · X slow down · B disembark · RB crossbow · D-pad Up Witcher Senses
  Everywhere    D-pad Left / Right potions (hold to swap) · D-pad Down quick access menu
                View game menu (hold: glossary) · Menu quick menu (hold: map) · R-Stick camera lock / track quest
  Sign casting  hold LT, then RT Igni · B Quen · Y Axii · X Yrden · RB Aard
The banners show every button in every context.

WHAT THE MOD ADDS TO THE BINDINGS
  - Sprint: out of combat a tap of B switches running on or off; a hold runs while held.
  - Swords: X draws or sheathes the steel sword on a tap and the silver sword on a hold - the game's own draw, so with
    the other sword out it switches.
  - Dismount: the hold-to-dismount circle follows A (the game always showed it on B, where Gallop is).
  - Signs: with LT held, each sign has its own button; on their own those buttons do their normal job. LT on its own
    still casts the selected sign.

INSTALL
1. Install the archive as a mod (Mod Organizer 2, Vortex), or copy the Mods folder into the game folder.
2. Close the game and run "Modern Control Map Installer\Install Modern Control Map.bat". It sets the controller
   bindings in Documents\The Witcher 3\input.settings, turns Left Stick Sprint off and alternative sign casting on, and
   leaves every keyboard binding as it is. It backs up each file it changes first.
   Mod Organizer 2 with profile-specific game settings: drag the profile folder onto the .bat instead.
Patch 5.0 (Remastered) only. No other mod required.

THE MAP IS FIXED
Set it with the installer, not with Options > Controller Scheme: the game cannot give a controller control a button
again once it has none, so change buttons in input.settings with the game closed.

COMPATIBILITY
The script wraps the game's handlers for Sprint, the two swords, the sign buttons, the dismount indicator and Jump with
annotations, so it merges with other script mods without Script Merger. Each part acts only on a controller and only
with the binding it serves in place.

UNINSTALL
Run "Uninstall Modern Control Map.bat" (it restores the files as they were before the first install - keyboard changes
made since then go with them), then remove the mod.
