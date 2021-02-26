# AI 기반의 보안 서비스
#### 딥러닝 기반의 보안 서비스에 대한 연구 레포지토리

## 1) 인공신경망 기반의 암/복호화 알고리즘 연구 (Google AI 논문 구현)
#### References : LEARNING TO PROTECT COMMUNICATIONS WITH ADVERSARIAL NEURAL CRYPTOGRAPHY (Google Brain)

![1](https://user-images.githubusercontent.com/41291493/109268442-70316680-784e-11eb-8bdd-8a9a31418c5b.png)
![2](https://user-images.githubusercontent.com/41291493/109268446-7293c080-784e-11eb-964f-bbefe725f8c9.png)
![3](https://user-images.githubusercontent.com/41291493/109268449-73c4ed80-784e-11eb-8451-5b1aeb600ff0.png)
![4](https://user-images.githubusercontent.com/41291493/109268451-745d8400-784e-11eb-9bf2-628344b64b13.png)
![5](https://user-images.githubusercontent.com/41291493/109268455-74f61a80-784e-11eb-8c2e-a125a39a8162.png)
![6](https://user-images.githubusercontent.com/41291493/109268456-758eb100-784e-11eb-8315-78111bc191ed.png)

Author: Tackhyun Jung

Status: 완료

### 핵심목표
1) `Alice` 평문(p)을 대상으로 자체 생성한 암호화 키(k)를 통해 암호문(c)를 만들어 전송한다
2) `Bob` 암호문(c)을 암호화 키(k)를 통해 평문(p)를 유추한다
3) `Eve` 암호문(c)을 암호화 키(k) 없이 Brute force와 Random guessing을 통해 평문(p)를 유추한다

---

### 사용된 기술
* Brute force and Random guessing
* Deep Neural Networks
* AdamOptimizer
* Relu

---

### Requirement
* Python 3.6
* tensorflow
* ArgumentParser
* CryptoNet
* numpy

import matplotlib
---

### Usage

```
$ Python Main.py
```

---

## 2) `CNN` 대상 `Adversarial Attack`에 대한 방어 PoC

(추후 작성 예정)

