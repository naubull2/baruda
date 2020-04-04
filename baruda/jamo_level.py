# coding: utf8
"""
  jamo_level.py
  ~~~~~~~~~~~~~
  Hangul(Korean letter) convert, decompose and recompose function utils

  :copyright: (c) 2020- by naubull2
  :license: BSD, view LICENSE for more details.
"""
import logging
import unicodedata

from jamo import h2j

from .jamodict import (
    CHOSEONG_LIST, JUNGSEONG_LIST,
    JONGSEONG_LIST, INFREQUENT_JONGSEONG,
    CONSONANTS
)


def conv_hcj(ch):
    """Convert Hangul Jamo to Compatibility Hangul Jamo
    """
    unicode_names = unicodedata.name(ch)
    if unicode_names.find('CHOSEONG') >= 0:
        unicode_names = unicode_names.replace('CHOSEONG', 'LETTER')
    elif unicode_names.find('JUNGSEONG') >= 0:
        unicode_names = unicode_names.replace('JUNGSEONG', 'LETTER')
    elif unicode_names.find('JONGSEONG') >= 0:
        unicode_names = unicode_names.replace('JONGSEONG', 'LETTER')
    try:
        return unicodedata.lookup(unicode_names)
    except Exception:
        logging.warning('Warning: Invalid Hangul Jamo "{}"'.format(ch))
    return ch


def conv_hj(ch, code=None):
    """Revert Compatibility Hangul Jamo to Hangul Jamo
    Args:
      ch   : A hcj letter to revert to hj letter
      code : Code name among [CHOSEONG|JUNGSEONG|JONGSEONG]
    """
    try:
        unicode_names = unicodedata.name(ch)
        if 'LETTER' in unicode_names and 'HANGUL' in unicode_names:
            if code:
                unicode_names = unicode_names.replace('LETTER', code)
            elif ch in JUNGSEONG_LIST:
                unicode_names = unicode_names.replace('LETTER', 'JUNGSEONG')

        elif code and 'CHOSEONG' in unicode_names:
            unicode_names = unicode_names.replace('CHOSEONG', code)

        elif code and 'JONGSEONG' in unicode_names:
            unicode_names = unicode_names.replace('JONGSEONG', code)

        ch = unicodedata.lookup(unicode_names)

    except Exception as e:
        raise ValueError('Invalid synthesis : {}'.format(str(e)))
    else:
        return ch


def string2jamo(string, letter=False):
    """Convert Korean string into Hangul Jamo sequence
    Args:
      letter : If true, return in Hangul compatibility Jamo.
    """
    jamos = h2j(string)
    if letter:
        return ''.join([conv_hcj(c) for c in jamos])
    return jamos


def jamo2string(jamo_string):
    """Convert Hangul Jamo sequence into Hangul syllables
    """
    def _compose_syllable(seq):
        """Takes in letter type Jamo string and compose into a complete korean character"""
        try:
            seq = [conv_hcj(c) for c in seq]
            if len(seq) == 3:
                # chosung + jungsung + jongsung
                code = 44032 + CHOSEONG_LIST.index(seq[0]) * 588 + JUNGSEONG_LIST.index(seq[1]) * 28 + JONGSEONG_LIST.index(seq[2])
                return chr(code)
            elif len(seq) == 2:
                # chosung + jungsung
                code = 44032 + CHOSEONG_LIST.index(seq[0]) * 588 + JUNGSEONG_LIST.index(seq[1]) * 28
                return chr(code)

            elif seq:
                return ''.join(seq)
            else:
                return ''
        except Exception:
            return ''.join(seq)

    # Look for choseong initialized subsequence
    output = list()
    tmp = list()
    for c in jamo_string:
        try:
            code_name = unicodedata.name(c)
            if ('CHOSEONG' in code_name or \
                    c == ' ' or  \
                    not code_name.startswith('HANGUL') or \
                    code_name.startswith('HANGUL LETTER')) and tmp:
                output.append(_compose_syllable(tmp))
                tmp = list()
                tmp.append(c)
            else:
                tmp.append(c)
        except Exception:
            tmp.append(c)
    if tmp:
        output.append(_compose_syllable(tmp))
    return ''.join(output)


class _Jamo(object):
    """Internal object for recomposition of Hangul phrases and sentences
    """
    # NOTE: These jungseong can mean special memes online
    # 'ㅠ'|'ㅜ' : Used for representing crying face
    # 'ㅗ' : Used inplace of the "that-F**-word-you-know".
    special_jungseong = {'ㅠ', 'ㅜ', 'ㅗ'}
    def __init__(self, string):
        self.origin = string
        self.jamos = list()
        self.compat_jamos = list()

    def decompose(self):
        self.jamos = string2jamo(self.origin, letter=True)
        self.compat_jamos = string2jamo(self.origin, letter=False)

    def fix_jamo_typo(self):
        """Fix Hangul Jamo frequent typos on heuristics on human mistake patterns
          - Consecutive Jungseong, Choseon letters are highly likely to be typos
        """
        last_c = ''
        last_code = ''
        last_val = ''
        add_twice = False

        output = []
        for c in self.compat_jamos:
            code_name = unicodedata.name(c)
            curr_val = conv_hcj(c)

            if 'JONGSEONG' in last_code and last_val == curr_val and 'LETTER' in code_name:
                add_twice = True
                pass
            elif 'JUNGSEONG' in last_code and last_val == curr_val and 'LETTER' in code_name:
                continue
            elif 'JUNGSEONG' in last_code and curr_val in JUNGSEONG_LIST and \
                 curr_val not in self.special_jungseong:
                continue
            else:
                if last_c:
                    output.append(last_c)
                    if add_twice:
                        output.append(last_c)
                        add_twice = False

            last_c = c
            last_code = code_name
            last_val = curr_val

        if last_c:
            output.append(last_c)
            if add_twice:
                output.append(last_c)

        self.compat_jamos = output

    def synth_syllables(self):
        """Check sliding window of Hangul Jamo sequence, re-composing Hangul Syllables
        """
        output = []
        try:
            # NOTE: How this scan over jamos work
            # - On Choseong, look ahead until non-space is found
            #   - If next is LETTER, check for (cho + jung), then compose a [syllable.len == 2 ]
            #     ㄴpush forward i to the next position after space
            #   - Check for (cho != cho) AND (i-1 == jung), if so, change cho->jong, then compose
            # - Otherwise, cancel look ahead
            i = 0
            while i < len(self.compat_jamos):
                c = self.compat_jamos[i]
                code_name = unicodedata.name(c)
                curr_val = conv_hcj(c)
                if ('LETTER' in code_name or curr_val in CHOSEONG_LIST) and i + 1 < len(self.compat_jamos):
                    # look ahead for non whitespace
                    j = i + 1
                    while j + 1 < len(self.compat_jamos) and self.compat_jamos[j] == ' ':
                        j += 1
                    next_code = unicodedata.name(self.compat_jamos[j])
                    next_val = conv_hcj(self.compat_jamos[j])
                    if 'LETTER' in next_code and any(next_val in L for L in CONSONANTS) and curr_val != next_val:
                        if output and 'JUNGSEONG' in unicodedata.name(output[-1]) and curr_val in JONGSEONG_LIST:
                            output.append(conv_hj(curr_val, 'JONGSEONG'))
                            i += 1
                            continue
                    elif 'LETTER' in next_code and next_val in JUNGSEONG_LIST and curr_val in CHOSEONG_LIST and \
                         not ('JONGSEONG' in code_name and next_val in self.special_jungseong):
                        output.append(conv_hj(curr_val, 'CHOSEONG'))
                        output.append(conv_hj(next_val, 'JUNGSEONG'))
                        i = j + 1
                        continue
                    elif 'CHOSEONG' in next_code:
                        if output and 'JUNGSEONG' in unicodedata.name(output[-1]) and curr_val in JONGSEONG_LIST:
                            output.append(conv_hj(curr_val, 'JONGSEONG'))
                            i += 1
                            continue
                    else:
                        pass
                output.append(c)
                i += 1

            self.compat_jamos = output
        except Exception as e:
            raise ValueError('Invalid synthesis : {}'.format(str(e)))

    def infrequent_jongseong(self):
        """Return true if the data has an infrequent Jongseong
        """
        if self.compat_jamos:
            for c in self.compat_jamos:
                code_name = unicodedata.name(c)
                val = conv_hcj(c)
                if 'JONGSEONG' in code_name and val in INFREQUENT_JONGSEONG:
                    return True
        return False

    def compose(self):
        """Compose Hangul Jamo sequence back to Hangul syllables
        """
        if self.compat_jamos:
            return jamo2string(self.compat_jamos)
        else:
            return self.origin


def jamofix(msg):
    """Fix Hangul Jamo frequent typos and reconstruct into valid syllables
    """
    # Compose broken syllables first
    try:
        t_j = _Jamo(msg)
        t_j.decompose()
        t_j.synth_syllables()
        msg = t_j.compose()
    except Exception:
        pass

    # Fix frequent jamo typos per chunks
    output = list()
    try:
        for eoj in msg.split():
            j = _Jamo(eoj)
            j.decompose()
            j.fix_jamo_typo()
            output.append(j.compose())
    except Exception:
        return msg

    return ' '.join(output)


if __name__ == '__main__':
    line = input('Input: ')
    print(jamofix(line))
