#!/usr/bin/env python

import argparse
import cv2
import os

""" requirements

pip install opencv-python
pip install argparse

"""


parser = argparse.ArgumentParser(description='Парсинг аргументов.')
parser.add_argument('filename', type=str, help='Название файла')
args = parser.parse_args()


# Путь к видеофайлу
video_path = args.filename


# Папка для сохранения кадров
output_folder = f'{str(video_path).split(".")[0]}'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Частота среза: каждый n-ый кадр
frequency = 1  # Извлекать каждый 10-й кадр

# Открытие видеофайла
cap = cv2.VideoCapture(video_path)

frame_count = 0
saved_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Сохранять только каждый n-ый кадр
    if frame_count % frequency == 0:
        frame_filename = os.path.join(output_folder, f'frame_{saved_count:04d}.jpg')
        cv2.imwrite(frame_filename, frame)
        saved_count += 1

        print(f'Сохранен кадр { saved_count }')

    frame_count += 1

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()

print(f'Разбито на {saved_count} кадров.')