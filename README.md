# Baruda
[![Python package](
  https://github.com/naubull2/baruda/workflows/Python%20package/badge.svg?branch=master
)](https://github.com/naubull2/baruda/actions?query=workflow%3A%22Python+package%22)
[![README in Korean](
  https://img.shields.io/badge/readme-korean-blue.svg?style=flat
)](README.ko.md)

"Baruda"("바루다") is a pure Korean word that means "fix or correct things"
 - [Namu Wiki: List of pure Korean words](https://namu.wiki/w/%EC%88%9C%EC%9A%B0%EB%A6%AC%EB%A7%90/%EB%AA%A9%EB%A1%9D)

## Setup

- Source install

  ```
	python setup.py install
  ```

- PYPI install

  ```
	pip install baruda
  ```

## Usage

- **jamofix()** : Fix Hangul Jamo-level typos and synthesize broken Hangul syllables.
> ex. "ㅇㅣㄱㅓ 진짴ㅋㅋ ㄷㅚ욬ㅋ" -> "이거 진짜ㅋㅋㅋ 되요ㅋ"

```python
from baruda import jamofix

s = "ㅇㅣㄱㅓ 진짴ㅋㅋ ㄷㅚ욬ㅋ"
print(jamofix(s))
# >>> "이거 진짜ㅋㅋㅋ 되요ㅋ"
```

## Reference

- [JDongian/jamo](https://github.com/JDongian/python-jamo): Used for faster jamo decomposition.
