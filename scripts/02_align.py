# -*- coding: utf-8 -*-
"""Align known Unicode Genesis 1:1 against the legacy byte string to derive mapping hypotheses."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

legacy = '«kht¼{kt Eïhu ykfkþ yLku Ãk]Úðe MkßÞkO'
uni    = 'આરંભમાં ઈશ્વરે આકાશ અને પૃથ્વી સર્જ્યાં'

lw = legacy.split(' ')
uw = uni.split(' ')
for i, (l, u) in enumerate(zip(lw, uw)):
    print(f'--- word {i} ---')
    print('  legacy :', l, '=>', ' '.join(f'{ord(c):02x}' for c in l))
    print('  unicode:', u, '=>', ' '.join(f'U+{ord(c):04X}' for c in u))
    print('  unames :', ' '.join(f'{c}' for c in u))
