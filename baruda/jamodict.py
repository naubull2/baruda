# coding: utf-8
"""
  jamodict.py
  ~~~~~~~~~~~
  Hangul consonants and vowels resource.

  :copyright: (c) 2020- by naubull2
  :license: BSD, view LICENSE for more details.
"""

CHOSEONG_LIST = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ',
    'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
    'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ',
    'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

JUNGSEONG_LIST = [
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ',
    'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
    'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ',
    'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
    'ㅣ'
]

JONGSEONG_LIST = [
    ' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ',
    'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ',
    'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ',
    'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
    'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ',
    'ㅌ', 'ㅍ', 'ㅎ'
]

INFREQUENT_JONGSEONG = [
    'ㅋ', 'ㅎ', 'ㅅ', 'ㅊ', 'ㅌ', 'ㅍ',
    'ㄲ', 'ㄳ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄺ',
    'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅄ'
]

CONSONANTS = set(CHOSEONG_LIST + JONGSEONG_LIST)
