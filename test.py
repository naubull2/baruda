# coding: utf-8
from baruda import jamofix


def test_about():
    __import__('baruda.__about__')


def test_jamofix():
    assert(jamofix('ㅇㅣㄱㅔ ㅁㅝ얔ㅋㅋ') == '이게 뭐야ㅋㅋㅋ')
