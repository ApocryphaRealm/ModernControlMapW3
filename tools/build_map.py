# Modern Control Map - builds dist\Modern Control Map Installer\map.json: every controller binding the map changes, as
# the difference between the game's own controller lines (map\vanilla.input.settings - the owner's file before any map
# work, whose pad lines are the game's defaults) and the finalized map (map\input.settings). Keyboard lines are never
# read or written. Run: python -I tools/build_map.py [--check]
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
VANILLA = os.path.join(ROOT, 'map', 'vanilla.input.settings')
MAP = os.path.join(ROOT, 'map', 'input.settings')
OUT = os.path.join(ROOT, 'dist', 'Modern Control Map Installer', 'map.json')
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
            e = out.setdefault((ctx, action), {'pad': [], 'none': 0})
            if is_pad(key):
                e['pad'].append(key + '=(Action=' + action + rest)
            elif key == 'IK_None':
                e['none'] += 1
    return out


def build():
    van, new = load(VANILLA), load(MAP)
    rules = []
    for k in sorted(set(van) | set(new)):
        a, b = van.get(k, {'pad': [], 'none': 0}), new.get(k, {'pad': [], 'none': 0})
        if sorted(a['pad']) != sorted(b['pad']):
            rules.append({'context': k[0], 'action': k[1], 'pad': b['pad'],
                          'unbound': not b['pad']})
    return {
        'name': 'Modern Control Map',
        'rules': rules,
        'settings': [
            {'section': 'Controls', 'key': 'LeftStickSprint', 'value': 'false'},
            {'section': 'Gameplay', 'key': 'EnableAlternateSignCasting', 'value': '1'},
        ],
    }


def main():
    data = json.dumps(build(), indent=1, ensure_ascii=False) + '\n'
    if '--check' in sys.argv:
        ok = os.path.exists(OUT) and open(OUT, encoding='utf-8').read() == data
        print('ok    map.json matches the map' if ok else 'FAIL  map.json differs - run tools/build_map.py')
        sys.exit(0 if ok else 1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8', newline='\n').write(data)
    print('wrote', OUT, len(json.loads(data)['rules']), 'rules')


if __name__ == '__main__':
    main()
