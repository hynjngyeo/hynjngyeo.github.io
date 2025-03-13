+++
title = "Knowledge Distillation, 2015"
description = "Model Lightweighting Methods Using Soft Targets"
tags = [
    "distillation",
    "classification"
]
date = "2023-03-14"
categories = [
    "PaperReview",
]
menu = "main"
+++

Knowledge Distillation is a technique where a smaller, lightweight student model learns from a larger teacher model from its soft target. This method helps reduce model size after training for efficient deployment.

> Paper : [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531)


## 1. Knowledge Distillation
<hr>

### 1.1. Concept

지식 증류는 분류를 수행하는 큰(cumbersome) 뉴럴 네트워크가 학습한 soft target을 활용해 규모가 작은(small) 모델에 효과적으로 transfer learning을 하는 방법이다. 이때 hard target이란  또는 1로 표현되는 데이터 샘플의 true label을, soft target이란 softmax 함수의 결과 확률 또는 로짓을 의미한다. Soft target은 그 데이터셋에 대한 많은 정보를 포함하고 있으므로, 모든 클래스에 대한 값이 의미를 가진다. 이런 정보를 효과적으로 더 작은 모델로 이전하는 것이 지식 증류의 목적이다. 

> ### Problem: soft target 확률이 작아 cross-entopy에 반영되지 않는다.
실제로는 soft target에 대한 여러 클래스의 softmax 확률 값이 매우 작기 때문에, cross-entropy 비용 함수에 효과적으로 이 정보를 입력하기 어렵다. 

예를 들어 MNIST 학습처럼 충분히 큰 모델이 높은 정확도를 내는 과제에서 학습된 정보는 대부분 soft target에 저장된다. 예를 들어 "2"를 나타내는 데이터는 "3"으로 분류될 확률이 $10^{-6}$인데 반해 "7"로 분류될 확률은 $10^{-9}$일 수 있다. 이런 데이터에 대한 확률 비율은 클래스 유사도를 나타내는 귀중한 정보이지만 확률 자체의 값이 너무 작아 cross-entropy 비용 함수에서는 거의 반영되지 않는다.

**모델 학습시 참고:** soft target이 충분히 엔트로피가 높으면, hard target에 비해 더 많은 정보를 담고 있으며, 학습시 그래디언트의 variance 또한 작다는 것을 의미한다. 따라서 가벼운 모델은 더 작은 데이터셋에 대해 더 큰 learning rate를 사용해 학습할 수 있다.

> ### Solution: Increase the temperature in Softmax function

지식 증류는 이 문제를 softmax 함수의 온도(temperature)를 높여서 해결한다. 여기서 온도란 softmax 함수의 변수로, 온도를 높일수록 함수는 더 랜덤한 결과를 도출해 클래스 확률 분포를 줄인다. 높은 온도를 통해 더 "부드러운(soft)" 클래스 확률 분포를 얻을 수 있으므로, 결론적으로 soft target들의 확률을 전반적으로 높일 수 있다. 

우선 무거운 모델이 충분히 "soft"한 target set을 도출할 때까지 temperature를 높여, 이 높은 temperature를 가벼운 모델을 학습할 때 적용하여 계산한다. 이때 증류된 모델이 학습하는 1️⃣ transfer set에 라벨이 없는 경우, 큰 모델의 soft target과 높은 온도를 이용하여 학습한다. 2️⃣ transfer set의 라벨을 얻을 수 있는 경우, 앞선 학습과 correct target을 1의 온도로 학습한 cross-entropy 함수의 가중치 평균을 활용하여 학습하는 것이 효과적이다. 

temperature $T$를 포함한 softmax는 로짓 $z_i$를 다른 로짓들 ${z_i}$와 비교하여 확률 $q_i$를 도출하는 함수이다.

$$
q_i = \frac{exp(z_i / T)}{\sum_j exp(z_j/ T)}
$$

$T=1$인 경우는 일반적인 softmax 함수가 되며, $T$를 높이면 더 "soft"한 클래스 확률 분포를 얻을 수 있다.

2️⃣ 의 경우에 대한 최종 손실 함수는 가중지 $\alpha$에 대해 다음과 같이 쓸 수 있다 ($T^2$를 스케일링 해주는 그래디언트 계산 때문인데, 자세히는 아래에서 살펴본다):

$$
L = \alpha T^2 \text{CE} (P_{small}^{T=t}, P_{big}^{T=t}) + (1- \alpha) \text{CE}(P_{small}^{T=1}, \text{true label})
$$



### 1.2. Making Use of Transfer Set
transfer set의 데이터에 대해 무거운 모델의 soft target 분포를 활용하면 distilation을 할 수 있다. 만약 transfer set이 라벨된 경우, soft target과 hard target에 대한 cross-entropy를 각각 계산하여 가중합 할 수 있다. 
1. soft target의 cross-entropy를 오리지널 모델의 temperature를 사용하여 계산한다.
2. hard target의 cross-entorpy를 $T=1$로 계산한다.

이때 soft target으로 생성한 그래디언트의 크기는 $1/T^2$배 스케일되어 있으므로 그래디언트에 최종적으로 $T^2$를 곱해야 $T$를 변화해도 hard와 soft target의 비율을 유지할 수 있다.

#### Psuedo Code

위에서 정의한 softmax 함수와 손실 함수를 바탕으로 간략한 의사 코드를 쓸 수 있다.

```python
# Define distilled model which has softmax layer with temperature as final layer.
class DistilledModel(Module):
    def __init__(self, input_dim, output_dim, temp=1, name=None):
        super().__init__(name=name)
        self.small_model = ... # define some small model.
        self.temp = temp
        
    def softmax_temp(self, x):
        exp_x = np.exp(x / self.temp)
        exp_x = exp_x - np.max(exp_x)
        sum_exp_x = np.sum(exp_x)
        return exp_x / sum_exp_x

    def __call__(self, x):
        logit = self.small_model(x) 
        output = self.softmax_temp(logit)
        return output
        
# Define final weighted cross-entropy function for distilled model.
# By the paper, it is recommended alpha > 0.5.
def final_cross_entropy(y_true, y_pred, y_soft, big_soft, alpha, high_temp):
    entropy_1 = CrossEntropy(y_soft, big_soft)
    entropy_2 = CrossEntropy(y_true, y_pred)
    return alpha * (high_temp ** 2) * entropy_1 + (1. - alpha) * entropy_2

# Train small model with soft target and high temperature from the cumbersome model.
distilled_model_1 = DistilledModel(input_dim, output_dim, temp=high_temp)
distilled_model_1.compile(...)
y_soft = distilled_model_1.fit((transfer_set, soft_target))

# Train true target of transfer set with temperature 1.
distilled_model_2 = DistilledModel(input_dim, output_dim)
distilled_model_2.compile(...)
y_pred = distilled_model_2.fit((transfer_set, true_target))

# Compute final cross-entropy function.
final_cross_entropy = final_cross_entropy(y_true, y_pred, 
                                          y_soft, big_soft,
                                          alpha, high_temp)
```


#### 1.3 지식 증류 특수 사례 : Logit 활용

실제로는 Logit을 활용하여 cross-entropy 함수를 변환하는 것 또한 지식 증류의 한 사례다. 이를 확인하기 위해 로짓의 그래디언트 디센트를 해보자.

- 큰 모델의 로짓 $v_i$, 확률 $p_i$
- 증류된 모델의 로짓 $z_i$, 확률 $q_i$
- 증류된 모델의 cross-entopy $C$

이때 증류된 모델의 cross-entropy 그래디언트는 다음과 같다(여기서는 하나의 로짓에 대한 편미분으로 나타냈다):

$$
\begin{aligned}
\frac{\partial C}{\partial z_i} 
&= \frac{1}{T} ( q_i - p_i) \\
&= \frac{1}{T} (\frac{e^{z_i/T}}{\sum_j e^{z_j/T}} - \frac{e^{v_i/T}}{\sum_j e^{v_j/T}})
\end{aligned}
$$

여기서 1️⃣ 온도가 로짓의 값보다 상대적으로 크면 (즉 $1/T$가 전체값을 충분히 작게 만들면) Smoothing을 적용할 수 있다:

$$
\frac{\partial C}{\partial z_i} 
\approx 
\frac{1}{NT} (\frac{1 + e^{z_i/T}}{N + \sum_j e^{z_j/T}} - \frac{1 + e^{v_i/T}}{N + \sum_j e^{v_j/T}})
$$

또한 2️⃣ 가정을 통해 두 로짓의 평균이 $0$이 되도록 만들 수 있다 (즉 $\sum_j z_j = \sum_j v_j = 0 $). 위의 두가지 조건이 만족되면 그래디언트를 다음과 같이 **두 로짓의 오차에 대한 상수배**값으로 근사할 수 있다:

$$
\frac{\partial C}{\partial z_i} 
\approx 
\frac{1}{NT^2} (z_i - v_i)
$$

위의 편미분을 모든 로짓 $z_i$에 대한 그래디언트를 구하고 $T^2$로 스케일링을 하면, 지식 증류는 두 로짓의 오차 제곱 $\frac{1}{2} (z_i - q_i)^2$를 최소화하는 작업이 된다.


## 2. Experiment
<hr>

### 2.1. Basic test on MNIST 

distillation으로 큰 모델과 비슷한 성능을 낼 수 있는지 실험했다.

| size of NN | generalization | test errors |
| :---: | :---: | :---: |
| big | Dropout | 67 |
| small | None | 146 |
| small | Distillation | 74 |

모델은 모두 2개의 hidden layer를 가지며 큰 모델의 경우 1200개, 작은 모델의 경우 800개의 hidden unit을 가진다. 결과적으로 MNIST의 6만개 데이터셋에 대해 학습한 큰 모델과 그 soft target을 추가적으로 학습한 작은 모델은 성능이 비슷했다. 충분한 bias(3.5)를 고려하면 작은 모델의 학습 데이터에서 하나의 클래스가 누락되더라도 distillation을 통해 누락된 클래스에 대해 98.6%의 예측 정확도를 얻을 수 있었다. 두개의 클래스가 누락된 경우 bias를 더 높여(7~8) 정확도를 높일 수 있었다.


### 2.2 Testing Ensemble Effect: Speech Recognition

앙상블 모델을 distilling하는 것이 같은 크기의 단순 모델에 비해 성능이 뛰어나다는 것을 증명하고자 했다.

논문이 쓰일 당시의 자동 음성 인식은 DNN을 통해 매 시점에 waveform을 독립 Hidden Markov 모델(HMM)의 특정 상태에 대한 확률 분포를 예측했으며, 라벨은 시퀀스 순서로 강제되었다. 즉 일반적으로 DNN을 통해 예측값과 라벨의 frame당 클래스를 cross entropy 최소화 방식으로 학습했으므로 distillation을 수행하기 적합했다. 

시간 t에서 acoustic 데이터 $s_t$를 HMM의 "옳은"(hard target) 상태 확률 $h_t$로 나타내는 확률로 모델의 파라미터 $\theta$를 다음과 같이 결정할 수 있다:

$$
\theta = \text{argmax}_{\theta'}P(h_t|s_t;\theta')
$$

| System | Test Frame Accuracy | WER |
| :---: | :---: | :---: |
| Baseline | 58.9% | 10.9% |
| 10xEnsemble | 61.1% | 10.7% |
| Distilled Single Model | 60.8% | 10.7% |

Baseline은 Android voice search이며 앙상블은 10개의 모델에 대해 진행하였다. 의도한대로 앙상블 모델의 성능이 전이되었음을 Accuracy와 WER의 유사함을 통해 확인할 수 있다.


### 2.3 Testing Regularizer Effect

Soft target을 hard target과 같이 활용하는 것이 regularizer 역할을 할 수 있다는 것을 보인다. 

| System & training set | Train Frame Accuracy | Test Frame Accuracy |
| :---: | :---: | :---: |
| Baseline(100% of training set) | 63.4% | 58.9% |
| Baseline(3% of training set) | 67.3% | 44.5% |
| Soft Targets(3% of training set) | 65.4% | 57.0% |

앞서 본 speech recognition과제의 baseline은 85M개의 파라미터를 가졌다. 학습 데이터의 3% 만으로 새로운 모델을 학습하면 심한 overfitting이 나타났지만, soft target을 활용하여 학습하면 전체 데이터셋의 대부분의 정보를 학습할 뿐만 아니라 early stopping 없이도 수렴하는 결과를 보였다.



