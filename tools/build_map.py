# Modern Control Map - builds dist\Modern Control Map Installer\map.json: every controller binding the map changes, as
# the difference between the game's own controller lines (map\vanilla.input.settings - the owner's file before any map
# work, whose pad lines are the game's defaults) and the finalized map (map\input.settings). Keyboard lines are never
# read or written. Run: python -I tools/build_map.py [--check]
#   --variant alt1 --out <map.json>  an optional file's map: the finalized map with the VARIANTS moves applied
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
VANILLA = os.path.join(ROOT, 'map', 'vanilla.input.settings')
MAP = os.path.join(ROOT, 'map', 'input.settings')
OUT = os.path.join(ROOT, 'dist', 'Modern Control Map Installer', 'map.json')
# Optional files (the owner, 2026-10-07: "make an alternate version with a alt 1 suffix with the change" - a player asked for
# Witcher Senses on LB instead of a stick click, for the stick button's sake). Each move: (context, action, from, to).
VARIANTS = {
    'alt1': {
        'name': 'Modern Control Map - Alt 1',
        'moves': [('Exploration', 'Focus', 'IK_Pad_LeftThumb', 'IK_Pad_LeftShoulder')],
    },
}
LINE = re.compile(r'^(IK_[A-Za-z0-9_]+)=\(Action=([A-Za-z0-9_]+)([,)].*)$')


def is_pad(key):
    return key.startswith('IK_Pad_') or key.startswith('IK_PS4_')


def load(path):
    ctx, out = None, {}
    for raw in open(path, encoding='utf-8-sig'):
        s = raw.strip()
        if s.startswith('['):
            ctx = s[1:-1]
            continue
        m = LINE.match(s)
        if m and ctx:
            key, action, rest = m.groups()
            e = out.setdefault((ctx, action), {'pad': [], 'none': {}})
            if is_pad(key):
                e['pad'].append(key + '=(Action=' + action + rest)
            elif key == 'IK_None':
                line = 'IK_None=(Action=' + action + rest
                e['none'][line] = e['none'].get(line, 0) + 1
    return out


def apply_variant(new, variant):
    for ctx, action, src, dst in VARIANTS[variant]['moves']:
        e = new.get((ctx, action))
        lines = e['pad'] if e else []
        moved = [l for l in lines if l.startswith(src + '=')]
        if not moved:
            sys.exit('variant %s: [%s] %s has no %s line to move' % (variant, ctx, action, src))
        e['pad'] = [dst + l[len(src):] if l.startswith(src + '=') else l for l in lines]
        # the destination must be free in that context (no other action of it on the same button)
        for (c, a), other in new.items():
            if c == ctx and a != action and any(l.startswith(dst + '=') for l in other['pad']):
                sys.exit('variant %s: %s is already %s in [%s]' % (variant, dst, a, ctx))


def build(variant=None):
    van, new = load(VANILLA), load(MAP)
    if variant:
        apply_variant(new, variant)
    rules = []
    for k in sorted(set(van) | set(new)):
        a, b = van.get(k, {'pad': [], 'none': {}}), new.get(k, {'pad': [], 'none': {}})
        if sorted(a['pad']) != sorted(b['pad']):
            # the empty pad slots the map leaves (an IK_None line where the game had a pad button), with the action's
            # own State/IdleTime kept: the line and how many the context ends up with
            none = [{'line': line, 'count': n} for line, n in sorted(b['none'].items()) if n > a['none'].get(line, 0)]
            rules.append({'context': k[0], 'action': k[1], 'pad': b['pad'], 'none': none})
    return {
        'name': VARIANTS[variant]['name'] if variant else 'Modern Control Map',
        'rules': rules,
        'settings': [
            {'section': 'Controls', 'key': 'LeftStickSprint', 'value': 'false'},
            {'section': 'Gameplay', 'key': 'EnableAlternateSignCasting', 'value': '1'},
        ],
    }


def arg(name):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


def main():
    variant, out = arg('--variant'), arg('--out') or OUT
    if variant and variant not in VARIANTS:
        sys.exit('unknown variant %s (%s)' % (variant, ', '.join(VARIANTS)))
    if variant and out == OUT:
        sys.exit('a variant writes its own map.json: give --out (the dist map.json is the main file\'s)')
    data = json.dumps(build(variant), indent=1, ensure_ascii=False) + '\n'
    if '--check' in sys.argv:
        ok = os.path.exists(OUT) and open(OUT, encoding='utf-8').read() == data
        print('ok    map.json matches the map' if ok else 'FAIL  map.json differs - run tools/build_map.py')
        sys.exit(0 if ok else 1)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8', newline='\n').write(data)
    print('wrote', out, len(json.loads(data)['rules']), 'rules')


if __name__ == '__main__':
    main()
