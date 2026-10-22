# -*- coding: utf-8 -*-
"""Build-level regression: verse-key integrity checks on the generated Bible.
Currently guards the Pass-16 Luke 6:36 anchor rekey (source name="v63" -> 36).

Run:  PYTHONIOENCODING=utf-8 python test_verse_keys.py
Exit 0 = pass, 1 = fail."""
import sys, io, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
BIBLE = os.path.join(HERE, '..', 'output', 'bible.json')

EXPECTED_36 = ('તમારા પિતા જેવા દયાળુ છે તેવા તમે પણ દયાળુ થજે. '
               'બીજાના કાજી થશો નહિ (માથ્થી ૭:૧-૫)')


def main():
    b = json.load(open(BIBLE, encoding='utf-8'))
    luke6 = b['NT']['3']['chapters']['6']
    fails = 0

    def check(cond, msg):
        nonlocal fails
        print(('OK ' if cond else '!! ') + msg)
        if not cond:
            fails += 1

    # Pass 16: Luke 6:36 anchor rekey (source had name="v63", id/numeral said 36)
    check('36' in luke6, 'Luke 6:36 key present')
    check('63' not in luke6, 'Luke 6:63 transposed key absent (not duplicated)')
    check(luke6.get('36') == EXPECTED_36, 'Luke 6:36 holds the mercy-sentence value')
    keys = list(luke6.keys())
    if '36' in keys:
        i = keys.index('36')
        check(keys[i-1:i+2] == ['35', '36', '37'], 'Luke 6:36 is in sequence 35,36,37')

    # general: no NT/3 chapter 6 key should be a 2-digit transposition artifact >50
    big = [k for k in luke6 if k.isdigit() and int(k) > 49]
    check(not big, f'no out-of-range Luke 6 keys ({big})')

    print(f"\n{'PASS' if not fails else 'FAIL'}: {len(keys)} Luke 6 verses, {fails} failures")
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
