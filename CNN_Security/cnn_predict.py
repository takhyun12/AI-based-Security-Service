import numpy as np
from keras.preprocessing import image
from keras.applications import inception_v3

# 사전 학습된 이미지 인식 모델(Google Inception_V3) 로드
model = inception_v3.InceptionV3()

# 이미지를 불러와서, numpy array 형식으로 변환하여 저장
img = image.load_img("image/denoising_image.png", target_size=(299, 299))
input_image = image.img_to_array(img)

# 모델의 예상대로 모든 픽셀 강도가 [-1, 1]이 되도록 영상 스케일링
input_image /= 255.
input_image -= 0.5
input_image *= 2.

# 배치 크기에 대한 4차원 추가 (Keras가 예상한 대로)
input_image = np.expand_dims(input_image, axis=0)

# 인공신경망을 통한 결과 추론
predictions = model.predict(input_image)

# 예측결과를 텍스트로 변환하여 출력
predicted_classes = inception_v3.decode_predictions(predictions, top=1)
imagenet_id, name, confidence = predicted_classes[0][0]
print("[>] 추론 결과는 {} 로 {:.4}% 의 정확도로 판단됩니다!".format(name, confidence * 100))