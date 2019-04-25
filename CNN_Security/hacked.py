import numpy as np
from keras.preprocessing import image
from keras.applications import inception_v3
from keras import backend as K
from PIL import Image

# 사전 학습된 이미지 인식 모델 로드
model = inception_v3.InceptionV3()

# 신경망의 첫 번째 및 마지막 층에 대한 참조를 잡습니다.
model_input_layer = model.layers[0].input
model_output_layer = model.layers[-1].output

# 공격대상의 ImageNet feature를 선택합니다.
object_type_to_fake = 859

# 해킹할 이미지 로드
img = image.load_img("image/whippet.jpg", target_size=(299, 299))
original_image = image.img_to_array(img)

# 모델의 예상대로 모든 픽셀 강도가 [-1, 1]이 되도록 영상 스케일링
original_image /= 255.
original_image -= 0.5
original_image *= 2.

# 배치 크기에 대한 4차원 추가
original_image = np.expand_dims(original_image, axis=0)

# 이미지에 허용되는 최대 변경 내용을 미리 계산합니다
# 너무 과하게 변경되지 않도록 제한을 둠
# 숫자가 클수록 이미지는 더 빠르게 생성되지만 완전히 다른 이미지로 왜곡될 위험이 있습니다.
ma1x_change_above = original_image + 0.01
max_change_below = original_image - 0.0

# 복사할 입력 이미지의 복사본을 생성합니다.
hacked_image = np.copy(original_image)

# 각 반복에서 해킹된 이미지를 업데이트하는 방법
learning_rate = 0.1

# 비용 함수를 정의합니다.
# '비용'은 사전 교육을 받은 모델에 따라 목표 등급이 될 가능성이 높습니다.
cost_function = model_output_layer[0, object_type_to_fake]

# Keras를 통해 예측된 결과를 기반으로 변경할 데이터를 계산함
# 이 경우 "model_input_layer"를 참조하면 우리가 해킹하고 있는 이미지를 되찾을 수 있다.
gradient_function = K.gradients(cost_function, model_input_layer)[0]

# Keras를 통해 예측된 결과를 기반으로 변경할 데이터를 계산함
grab_cost_and_gradients_from_model = K.function([model_input_layer, K.learning_phase()], [cost_function, gradient_function])

cost = 0.0

# 루프에서, 해킹된 이미지를 조금씩 조정하여 모델을 더욱 더 속입니다.
# 80% 이상의 신뢰가 올 때까지
while cost < 0.80:
    # 이미지가 목표 클래스와 얼마나 가까운지 확인하고 경사도 파악
    # 그 방향으로 한 단계 더 밀어낼 수 있습니다
    # 참고: 여기에서 Keras 학습 모드에 대해 '0'을 입력하는 것이 매우 중요합니다!
    # 케라스 층은 예측 모드와 열차 모드에서 다르게 작용합니다!
    cost, gradients = grab_cost_and_gradients_from_model([hacked_image, 0])

    hacked_image += gradients * learning_rate

    # 잘못된 이미지가 되기 위해 이미지가 너무 많이 변경되지 않도록 합니다. (소폭만 변경)
    hacked_image = np.clip(hacked_image, max_change_below, max_change_above)
    hacked_image = np.clip(hacked_image, -1.0, 1.0)

    print("이미지 변조 진행상황: {:.8}%".format(cost * 100))

# 영상의 픽셀 크기를 [-1, 1]에서 [0, 255] 범위로 다시 조정
img = hacked_image[0]
img /= 2.
img += 0.5
img *= 255.

# 변조한 이미지를 파일로 저장
im = Image.fromarray(img.astype(np.uint8))
im.save("hacked-image.png")