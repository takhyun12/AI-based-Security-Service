# -*- coding: utf-8 -*-
import os
import hashlib
import shutil
from PIL import Image

'''
[1] 이미지를 텐서플로우에서 사용 가능하도록 준비함
'''
def Image_Calibration(path):  # 파일의 해쉬값을 가져오는 기능
    if os.path.exists(path):
        for file_name in os.listdir(path):  # 파일명 추출
            print(file_name)
            file_path = os.path.join(path, file_name).replace('\\', '/')  # 파일경로 추출
            file_hash = os.path.join(path, Get_md5(file_path) + '.jpg').replace('\\', '/')  # 파일의 해쉬값을 추출함
            shutil.move(file_path, file_hash)  # 이미지의 파일명을 해쉬로 변경함
            Image_Format_Change(file_hash)  # 파일을 jpg 포맷으로 보정함
'''
[2] 파일명을 해시로 변경하는 기능
    - 중복제거 및 한글 인코딩 문제 해결을 위해 파일명을 해시로 한다.
'''
def Get_md5(file_path):  # 파일의 해쉬값을 가져오는 기능
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:  # 파일을 읽어옴
        for chunk in iter(lambda: f.read(4096), b""):  # 람다 표현식을 통해 해쉬값 추출코드 간소화
            hash_md5.update(chunk)  # 받아온 해쉬값으로 갱신함
    return hash_md5.hexdigest()  # 해쉬값을 문자열로 리턴
'''
[3] 이미지를 재저장하는 기능
    - INCEPTION V3의 CNN 모델을 통해 머신러닝을 하기 위해서는 반드시 JPEG 포맷이어야 한다.
'''
def Image_Format_Change(file_hash):
    try:
        image = Image.open(file_hash).convert('RGB')
        image.save(file_hash, "JPEG", quality=100)
    except:
        os.remove(file_hash)

'''
[메인] 이미지를 텐서플로우에서 사용 가능하도록 하는것이 해당 파일의 목적 
'''
if __name__ == '__main__':
    Image_Calibration("downloads/dog/");

