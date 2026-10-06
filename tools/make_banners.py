# Modern Control Map for The Witcher 3 - controller banners, one per context.
# Every binding below was read from the owner's input.settings (C:\MO2\The Witcher 3\profiles\Default) on 2026-10-06
# after the sign-button edit; the descriptions are the game's own behaviour for those actions (scripts read from
# content0\scripts\game\player\playerInput.ws and the horse state). Run: python -I make_banners.py <out dir>
# Writes <context>.html and renders <context>.png (1920x1080) with headless Chrome.
import html
import os
import subprocess
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'banners')
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# button -> (x, y) on the controller drawing
POS = {
    'LT': (762, 268), 'LB': (735, 310), 'RT': (1158, 268), 'RB': (1185, 310),
    'LS': (757, 500), 'BACK': (902, 500), 'START': (1018, 500),
    'DUP': (842, 590), 'DLEFT': (807, 625), 'DRIGHT': (877, 625), 'DDOWN': (842, 660),
    'RS': (1078, 625), 'Y': (1163, 455), 'X': (1121, 497), 'B': (1205, 497), 'A': (1163, 539),
}
# how far from a button's centre its callout line stops (its edge), so the line never covers the glyph
RAD = {'LT': 10, 'RT': 10, 'LB': 8, 'RB': 8, 'LS': 32, 'RS': 32, 'BACK': 16, 'START': 16, 'DUP': 16, 'DLEFT': 16,
       'DRIGHT': 16, 'DDOWN': 16, 'Y': 23, 'X': 23, 'B': 23, 'A': 23}
LEFT = ['LT', 'LB', 'LS', 'BACK', 'DUP', 'DLEFT', 'DRIGHT', 'DDOWN']
RIGHT = ['RT', 'RB', 'Y', 'X', 'B', 'A', 'START', 'RS']
NAMES = {'LT': 'LT', 'LB': 'LB', 'RT': 'RT', 'RB': 'RB', 'LS': 'L-Stick press', 'RS': 'R-Stick press',
         'BACK': 'View', 'START': 'Menu', 'DUP': 'D-pad Up', 'DLEFT': 'D-pad Left', 'DRIGHT': 'D-pad Right',
         'DDOWN': 'D-pad Down', 'Y': 'Y', 'X': 'X', 'B': 'B', 'A': 'A'}

MENU = ('Game Menu', 'tap: game menu · hold: glossary')
START = ('Quick Menu / Map', 'tap: quick menu · hold: world map')
POTIONS_L = ('Potion 1', 'tap: drink · hold: swap the potion in this slot')
POTIONS_R = ('Potion 2', 'tap: drink · hold: swap the potion in this slot')
RADIAL = ('Quick Access Menu', 'signs, bombs, crossbow')
UNUSED = ('—', 'unused')

CONTEXTS = [
    ('exploration', 'Exploration', 'On foot, out of combat', {
        'LT': ('Cast Sign', 'tap: cast the selected sign · hold: channel it'),
        'LB': UNUSED,
        'LS': ('Witcher Senses / Call Roach', 'hold: Witcher Senses · press twice: call your horse'),
        'BACK': MENU,
        'DUP': ('Quick Item', 'tap: crossbow / bomb · hold: aim'),
        'DLEFT': POTIONS_L, 'DRIGHT': POTIONS_R, 'DDOWN': RADIAL,
        'RT': ('Strong Attack', 'draws your sword · hold: Rend'),
        'RB': ('Fast Attack', 'draws your sword · hold: Whirl'),
        'Y': ('Jump / Climb', 'tap: jump · at a ledge: climb'),
        'X': ('Swords', 'tap: steel sword in or out · hold: silver sword in or out'),
        'B': ('Sprint', 'hold: run while held · tap: run on / off'),
        'A': ('Interact', 'talk, loot, open, pick herbs, mount'),
        'START': START,
        'RS': ('Track Quest', 'objectives · with L-Stick: photo mode'),
    }),
    ('combat', 'Combat', 'Weapon drawn, enemies near', {
        'LT': ('Cast Sign', 'tap: cast the selected sign · hold: channel it'),
        'LB': ('Parry / Block', 'hold: guard · tap in time: counter'),
        'LS': ('Quick Item', 'tap: crossbow / bomb · hold: aim'),
        'BACK': MENU,
        'DUP': UNUSED,
        'DLEFT': POTIONS_L, 'DRIGHT': POTIONS_R, 'DDOWN': RADIAL,
        'RT': ('Strong Attack', 'hold: Rend'),
        'RB': ('Fast Attack', 'hold: Whirl'),
        'Y': UNUSED,
        'X': ('Swords', 'tap: steel sword · hold: silver sword'),
        'B': ('Dodge / Sprint', 'tap: dodge · hold: run'),
        'A': ('Roll', 'tap: roll'),
        'START': START,
        'RS': ('Camera Lock', 'lock onto a target'),
    }),
    ('horseback', 'Horseback', 'Riding Roach', {
        'LT': ('Cast Sign', 'cast the selected sign from the saddle'),
        'LB': UNUSED,
        'LS': ('Interact', 'loot, pick herbs, fast travel from the saddle'),
        'BACK': MENU,
        'DUP': ('Witcher Senses', 'hold'),
        'DLEFT': POTIONS_L, 'DRIGHT': POTIONS_R, 'DDOWN': RADIAL,
        'RT': ('Attack', 'mounted sword strike'),
        'RB': ('Crossbow', 'tap: shoot · hold: aim'),
        'Y': ('Jump', 'jump an obstacle'),
        'X': ('Swords', 'tap: steel sword · hold: silver sword'),
        'B': ('Gallop', 'tap: canter · hold: gallop · cancels aiming'),
        'A': ('Dismount', 'hold'),
        'START': START,
        'RS': ('Camera Lock / Track Quest', 'lock onto a target · objectives'),
    }),
    ('swimming', 'Swimming & Diving', 'In the water', {
        'LT': UNUSED,
        'LB': UNUSED,
        'LS': ('Quick Item', 'tap: crossbow · hold: aim'),
        'BACK': MENU,
        'DUP': ('Witcher Senses', 'hold'),
        'DLEFT': POTIONS_L, 'DRIGHT': POTIONS_R, 'DDOWN': RADIAL,
        'RT': UNUSED,
        'RB': UNUSED,
        'Y': ('Surface / Climb Out', 'swim up · climb onto a ledge'),
        'X': UNUSED,
        'B': ('Dive / Swim Fast', 'tap: dive · hold: swim fast'),
        'A': ('Interact', 'loot, board a boat'),
        'START': START,
        'RS': ('Camera Lock / Track Quest', 'lock onto a target · objectives'),
    }),
    ('sailing', 'Sailing', 'At the helm of a boat', {
        'LT': UNUSED,
        'LB': UNUSED,
        'LS': UNUSED,
        'BACK': MENU,
        'DUP': ('Witcher Senses', 'hold'),
        'DLEFT': POTIONS_L, 'DRIGHT': POTIONS_R, 'DDOWN': RADIAL,
        'RT': UNUSED,
        'RB': ('Crossbow', 'tap: shoot · hold: aim'),
        'Y': UNUSED,
        'X': ('Slow Down / Reverse', 'hold'),
        'B': ('Disembark', 'leave the boat · cancels aiming'),
        'A': ('Speed Up', 'raise the sail'),
        'START': START,
        'RS': ('Camera Lock / Track Quest', 'lock onto a target · objectives'),
    }),
    ('signs', 'Sign Casting', 'Hold LT, then press', {
        'LT': ('Hold: Sign Casting', 'keep LT held, then press a sign button'),
        'LB': UNUSED, 'LS': UNUSED, 'BACK': UNUSED, 'DUP': UNUSED, 'DLEFT': UNUSED, 'DRIGHT': UNUSED, 'DDOWN': UNUSED,
        'RT': ('Igni', 'fire'),
        'RB': ('Aard', 'telekinetic blast'),
        'Y': ('Axii', 'charm and stun'),
        'X': ('Yrden', 'magic trap'),
        'B': ('Quen', 'shield · hold B: channel'),
        'A': UNUSED,
        'START': UNUSED, 'RS': UNUSED,
    }),
]

# AMF's Skellige theme (ApocryphaMenuFrameworkW3 dist\bin\x64_dx12\AMF\themes\skellige.ini) - the owner, 2026-10-06:
# "I want the diagrams to be in the color scheme of AMF Skellige theme. Black and red and white. And match the frame
# art." Colours are the theme's own; every box is drawn with the theme's frame.png as a nine-slice (corner 26), as AMF
# draws its windows.
SK = {'bg': '#020203', 'frame': '#A6A8A7', 'text': '#E8E8E8', 'dim': '#8C8C8C', 'accent': '#8E2A2E'}
FRAME_PNG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'ApocryphaMenuFrameworkW3', 'dist',
                         'bin', 'x64_dx12', 'AMF', 'themes', 'skellige', 'frame.png')


def frame_uri():
    import base64
    return 'data:image/png;base64,' + base64.b64encode(open(FRAME_PNG, 'rb').read()).decode('ascii')


def css():
    f = frame_uri()
    return f"""
*{{box-sizing:border-box}}
html,body{{margin:0;width:1920px;height:1080px;background:{SK['bg']};overflow:hidden}}
body{{font-family:'Segoe UI',Arial,sans-serif;color:{SK['text']};position:relative;
 background:radial-gradient(ellipse at 50% 58%,#160b0c 0%,#070506 45%,{SK['bg']} 80%)}}
svg{{position:absolute;left:0;top:0}}
.outer{{position:absolute;left:14px;top:14px;width:1892px;height:1052px;border-style:solid;border-width:0;
 border-image-source:url({f});border-image-slice:26;border-image-width:34px;border-image-repeat:stretch}}
.box{{position:absolute;width:520px;height:92px;padding:13px 22px 0 22px;border-style:solid;border-width:0;
 background:rgba(8,6,7,.92);border-image-source:url({f});border-image-slice:26;border-image-width:22px;
 border-image-repeat:stretch}}
.box.off{{opacity:.38}}
.row{{display:flex;align-items:center;gap:12px;white-space:nowrap}}
.pill{{background:{SK['accent']};color:{SK['text']};font-size:15px;font-weight:700;padding:3px 11px;border-radius:3px;
 letter-spacing:.5px}}
.off .pill{{background:#2a2a2a;color:{SK['dim']}}}
.name{{font-size:25px;font-weight:600;color:{SK['text']}}}
.desc{{font-size:17.5px;color:{SK['dim']};margin-top:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.t1{{font-family:Georgia,'Times New Roman',serif;font-size:28px;letter-spacing:7px;fill:{SK['accent']};
 text-transform:uppercase}}
.t2{{font-family:Georgia,'Times New Roman',serif;font-size:58px;fill:{SK['text']}}}
.t3{{font-size:22px;fill:{SK['dim']};letter-spacing:1px}}
.foot{{font-size:16px;fill:{SK['dim']}}}
"""


# callouts go to the button through these points (after the elbow next to the box), so no two lines cross and no
# line runs over another button
ROUTES = {'BACK': [(800, 550)], 'DUP': [(790, 565)], 'DRIGHT': [(877, 722)], 'X': [(1121, 622)]}
LEFT = ['LT', 'LB', 'LS', 'BACK', 'DUP', 'DLEFT', 'DDOWN', 'DRIGHT']
RIGHT = ['RT', 'RB', 'Y', 'B', 'A', 'X', 'START', 'RS']


def label(x, y, btn, entry):
    name, desc = entry
    off = name == '—'
    return (f'<div class="box{" off" if off else ""}" style="left:{x}px;top:{y - 46}px">'
            f'<div class="row"><span class="pill">{html.escape(NAMES[btn])}</span>'
            f'<span class="name">{html.escape(name)}</span></div>'
            f'<div class="desc">{html.escape(desc)}</div></div>'), off


def controller():
    s, f, a = '#3c3c3e', SK['frame'], SK['accent']
    face = ''.join(
        f'<circle cx="{cx}" cy="{cy}" r="21" fill="#141416" stroke="{f}" stroke-width="1.6"/>'
        f'<text x="{cx}" y="{cy + 7}" text-anchor="middle" font-size="20" font-weight="700" fill="{SK["text"]}">{t}</text>'
        for t, cx, cy in (('Y', 1163, 455), ('X', 1121, 497), ('B', 1205, 497), ('A', 1163, 539)))
    return f"""
<g>
 <rect x="722" y="250" width="84" height="44" rx="14" fill="#0d0d0f" stroke="{f}" stroke-width="1.4"/>
 <rect x="1114" y="250" width="84" height="44" rx="14" fill="#0d0d0f" stroke="{f}" stroke-width="1.4"/>
 <path d="M688 322 Q700 292 760 290 L840 292 Q856 296 860 306 L700 330 Z" fill="#111113" stroke="{f}" stroke-width="1.4"/>
 <path d="M1232 322 Q1220 292 1160 290 L1080 292 Q1064 296 1060 306 L1220 330 Z" fill="#111113" stroke="{f}" stroke-width="1.4"/>
 <path d="M690 330 Q706 304 770 302 L1150 302 Q1214 304 1230 330 L1268 430 Q1330 620 1310 720 Q1296 800 1236 812
   Q1180 820 1146 760 L1100 690 Q1076 664 1040 664 L880 664 Q844 664 820 690 L774 760 Q740 820 684 812
   Q624 800 610 720 Q590 620 652 430 Z" fill="#0b0b0d" stroke="{f}" stroke-width="2"/>
 <path d="M708 346 Q760 324 800 324 L1120 324 Q1160 324 1212 346" fill="none" stroke="{s}" stroke-width="1.5"/>
 <circle cx="757" cy="500" r="44" fill="#050506" stroke="{s}" stroke-width="2"/>
 <circle cx="757" cy="500" r="30" fill="#141416" stroke="{f}" stroke-width="1.6"/>
 <circle cx="1078" cy="625" r="44" fill="#050506" stroke="{s}" stroke-width="2"/>
 <circle cx="1078" cy="625" r="30" fill="#141416" stroke="{f}" stroke-width="1.6"/>
 <circle cx="842" cy="625" r="58" fill="#070708" stroke="{s}" stroke-width="1.5"/>
 <path d="M826 578 h32 v31 h31 v32 h-31 v31 h-32 v-31 h-31 v-32 h31 Z" fill="#141416" stroke="{f}" stroke-width="1.6"/>
 <circle cx="1163" cy="497" r="76" fill="#070708" stroke="{s}" stroke-width="1.5"/>
 {face}
 <rect x="888" y="490" width="28" height="20" rx="5" fill="#141416" stroke="{f}" stroke-width="1.6"/>
 <rect x="1004" y="490" width="28" height="20" rx="5" fill="#141416" stroke="{f}" stroke-width="1.6"/>
 <circle cx="960" cy="430" r="26" fill="#070708" stroke="{a}" stroke-width="2"/>
 <path d="M946 440 L960 416 L974 440" fill="none" stroke="{a}" stroke-width="3"/>
</g>"""


def banner(key, title, subtitle, data):
    W, H = 1920, 1080
    head = [f'<text x="960" y="66" text-anchor="middle" class="t1">Modern Control Map · The Witcher 3</text>',
            f'<text x="960" y="130" text-anchor="middle" class="t2">{html.escape(title)}</text>',
            f'<text x="960" y="168" text-anchor="middle" class="t3">{html.escape(subtitle)}</text>',
            '<line x1="700" y1="190" x2="1220" y2="190" stroke="#3c3c3e" stroke-width="1"/>',
            f'<rect x="954" y="184" width="12" height="12" transform="rotate(45 960 190)" fill="{SK["accent"]}"/>']
    rows_y = [262 + i * 106 for i in range(8)]
    lw = 520
    lines, boxes = [], []
    for side, keys in (('L', LEFT), ('R', RIGHT)):
        for i, btn in enumerate(keys):
            y = rows_y[i]
            x = 48 if side == 'L' else W - 48 - lw
            box, off = label(x, y, btn, data[btn])
            boxes.append(box)
            cx, cy = POS[btn]
            ex = x + lw if side == 'L' else x
            mid = ex + (40 if side == 'L' else -40)
            pts = [(ex, y), (mid, y)] + ROUTES.get(btn, [])
            lx, ly = pts[-1]
            dx, dy = lx - cx, ly - cy
            d = (dx * dx + dy * dy) ** 0.5 or 1
            bx, by = cx + dx / d * RAD[btn], cy + dy / d * RAD[btn]
            pts.append((bx, by))
            col = '#2c2c2e' if off else SK['frame']
            lines.append(f'<polyline points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in pts)}" fill="none" '
                         f'stroke="{col}" stroke-width="{1.3 if off else 1.8}" opacity="{0.6 if off else 0.95}"/>')
            lines.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{3 if off else 4.5}" '
                         f'fill="{"#2c2c2e" if off else SK["accent"]}" stroke="{"none" if off else SK["text"]}" '
                         f'stroke-width="1"/>')
    foot = ('<text x="960" y="1050" text-anchor="middle" class="foot">Xbox layout · Sprint by pressing Left Stick: off · '
            'Quick Sign Casting: Quick Casting · Automatically Apply Blade Oils: on</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           + '\n'.join(head) + controller() + '\n'.join(lines) + foot + '</svg>')
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>'
            f'<style>{css()}</style></head><body>{svg}<div class="outer"></div>{"".join(boxes)}</body></html>')


def main():
    os.makedirs(OUT, exist_ok=True)
    for i, (key, title, subtitle, data) in enumerate(CONTEXTS, 1):
        assert set(data) == set(POS), key
        name = f'{i}-{key}'
        hp = os.path.abspath(os.path.join(OUT, name + '.html'))
        open(hp, 'w', encoding='utf-8').write(banner(key, title, subtitle, data))
        png = os.path.abspath(os.path.join(OUT, name + '.png'))
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--window-size=1920,1080', '--screenshot=' + png, 'file:///' + hp.replace('\\', '/')],
                       check=True, capture_output=True, timeout=120)
        print(png)


if __name__ == '__main__':
    main()
