

import os
from PIL import Image
import re
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='ch')


def crop_bottom_third(image):
    width, height = image.size
    left = 0
    top = height * 2 // 3  # 识别底部1/3的区域
    right = width
    bottom = height
    return image.crop((left, top, right, bottom))


def extract_chinese_text(image_path):

    result = ocr.ocr(image_path, cls=True)

    text = ''
    for line in result:
        if not line:
            return ""
        for word_info in line:
            text += word_info[1][0]

    chinese_text = re.sub(r'[^\u4e00-\u9fff]', '', text)
    return chinese_text


def rename_jpg_files(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith('.jpg'):
            jpg_path = os.path.join(directory, filename)

            if not os.path.exists(jpg_path):
                break

            with Image.open(jpg_path) as img:
                cropped_img = crop_bottom_third(img)

                temp_path = os.path.join(directory, 'temp.jpg')
                cropped_img.save(temp_path)

                text = extract_chinese_text(temp_path)

                os.remove(temp_path)

                if text:
                    new_jpg_path = os.path.join(directory, text + '.jpg')
                    os.rename(jpg_path, new_jpg_path)
                    print(f'Renamed {filename} to {os.path.basename(new_jpg_path)}')
                else:
                    print(f'No text found in {filename}. Skipping rename.')


if __name__ == '__main__':
    rename_jpg_files('/Users/Pictures/')



