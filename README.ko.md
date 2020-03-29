# Baruda
[![Build Status](
  https://travis-ci.com/naubull2/Baruda.svg?branch=master 
)](https://travis-ci.com/naubull2/Baruda)
[![README in English](
  https://img.shields.io/badge/readme-english-blue.svg?style=flat
)](README.md)

"바루다" : 바르게 하다. 고치다.
 - [나무위키: 순우리말목록](https://namu.wiki/w/%EC%88%9C%EC%9A%B0%EB%A6%AC%EB%A7%90/%EB%AA%A9%EB%A1%9D)

## 설치

- 소스 설치

  ```
	python setup.py install
  ```

- PYPI 설치

  ```
	pip install baruda
  ```

## 사용법

- **jamofix()** : 자모 수준의 오타 수정, 깨진 한글 결합 처리를 해줍니다.
> ex. "ㅇㅣㄱㅓ 진짴ㅋㅋ ㄷㅚ욬ㅋ" -> "이거 진짜ㅋㅋㅋ 되요ㅋ"

```python
from baruda import jamofix

s = "ㅇㅣㄱㅓ 진짴ㅋㅋ ㄷㅚ욬ㅋ"
print(jamofix(s))
# >>> "이거 진짜ㅋㅋㅋ 되요ㅋ"
```

## 참고

- [JDongian/jamo](https://github.com/JDongian/python-jamo): 자모 분해시 직접 구현하는것보다 빨라서 채용.
