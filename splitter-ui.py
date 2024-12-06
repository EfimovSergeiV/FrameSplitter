#!/usr/bin/env python3

import cv2
import os

import tkinter as tk
from tkinter import filedialog



class VideoManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Извлечение кадров из видеофайла")
        self.root.geometry("640x420")
        
        # Глобальные переменные (в данном случае это атрибуты класса)
        self.video_path = ""
        self.save_directory = ""
        self.counter = 0
        self.status = "Готов к работе"
        
        # Интерфейс
        self.create_widgets()

    def create_widgets(self):
        # Поле для ввода пути к видеофайлу
        tk.Label(self.root, text="Выберите видеофайл:").pack(pady=5)
        self.video_path_entry = tk.Entry(self.root, width=60)
        self.video_path_entry.pack(pady=5)
        tk.Button(self.root, text="Обзор", command=self.select_video).pack(pady=5)

        # video_frame = tk.Frame(self.root)
        # video_frame.pack(pady=10)

        # # Поле ввода пути к видеофайлу
        # self.video_path_entry = tk.Entry(video_frame, width=60)
        # self.video_path_entry.pack(side=tk.LEFT, padx=5, ipady=4)  # ipady делает Entry выше
        
        # # Кнопка рядом с полем
        # select_video_button = tk.Button(video_frame, text="Обзор", command=self.select_video, height=1)
        # select_video_button.pack(side=tk.LEFT)

        
        # Поле для указания пути директории сохранения
        tk.Label(self.root, text="Укажите директорию для сохранения:").pack(pady=5)
        self.save_path_entry = tk.Entry(self.root, width=60)
        self.save_path_entry.pack(pady=5)
        tk.Button(self.root, text="Обзор", command=self.select_save_directory).pack(pady=5)
        
        # Кнопка для вывода глобальных переменных в консоль
        tk.Button(self.root, text="Запустить", font=("Arial", 18), bg="#86efac", command=self.extract_frames).pack(pady=10)
        # tk.Button(self.root, text="Показать глобальные переменные", command=self.show_globals).pack(pady=10)

        #
        # tk.Label(self.root, text=f"Извлечено кадров: { self.counter } ").pack(pady=5)
        # tk.Label(self.root, text=f"Готовность: { self.counter } ").pack(pady=5)
        # Сохранение ссылки на метку
        self.counter_label = tk.Label(self.root, text=f"Извлечено кадров: {self.counter}", font=("Arial", 18))
        self.counter_label.pack(pady=5)

        self.status_label = tk.Label(self.root, text=f"Готовность: {self.status}", font=("Arial", 16))
        self.status_label.pack(pady=5)




        
        # Кнопка для выхода из программы
        tk.Button(self.root, text="Выход", command=self.root.quit).pack(pady=10)

    def select_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
        if file_path:
            self.video_path = file_path
            self.video_path_entry.delete(0, tk.END)
            self.video_path_entry.insert(0, self.video_path)

    def select_save_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.save_directory = directory
            self.save_path_entry.delete(0, tk.END)
            self.save_path_entry.insert(0, self.save_directory)

    def show_globals(self):
        self.counter += 1

        # self.counter_label.config(text=f"Извлечено кадров: {self.counter}")
        # self.status_label.config(text=f"Готовность: {self.status}")

        # print(f"Video Path: {self.video_path.split('.')[0].split('/')[-1]}")
        # print(f"Save Directory: {self.save_directory}")



    def extract_frames(self):
        # Папка для сохранения кадров
        output_folder = f'{str(self.save_directory)}/{str(self.video_path.split(".")[0].split("/")[-1])}'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Частота среза: каждый n-ый кадр
        frequency = 1  # Извлекать каждый кадр

        # Открытие видеофайла
        cap = cv2.VideoCapture(self.video_path)

        frame_count = 0
        self.counter = 0

        self.status_label.config(text="Готовность: извлекаем кадры...")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Сохранять только каждый n-ый кадр
            if frame_count % frequency == 0:
                frame_filename = os.path.join(output_folder, f'frame_{self.counter:04d}.jpg')
                cv2.imwrite(frame_filename, frame)
                self.counter += 1

                # Обновляем метку
                self.counter_label.config(text=f"Извлечено кадров: {self.counter}")
                self.root.update()  # Принудительное обновление интерфейса

            frame_count += 1

        # Освобождение ресурсов
        cap.release()
        cv2.destroyAllWindows()
        self.status_label.config(text="Готовность: всё извлекли")



# Основной запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoManagerApp(root)
    root.mainloop()