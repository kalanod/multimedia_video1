import av
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Функция для расчета автокорреляции
def calculate_autocorrelation(frame_a, frame_b):
    H, W = frame_a.shape
    mean_a = np.mean(frame_a)
    mean_b = np.mean(frame_b)
    std_a = np.std(frame_a)
    std_b = np.std(frame_b)

    numerator = np.sum((frame_a - mean_a) * (frame_b - mean_b))
    denominator = H * W * std_a * std_b

    return numerator / denominator if denominator != 0 else 0


# Чтение видео и расчет автокорреляции
def analyze_video(video_path):
    # Открытие видео
    container = av.open(video_path)

    # Извлечение кадров
    frames = []
    for frame in container.decode(video=0):
        frames.append(frame.to_ndarray(format='gray'))  # Конвертируем в grayscale

    # Расчет автокорреляции
    num_frames = len(frames)
    autocorrelations = np.zeros((num_frames, num_frames))

    for i in range(num_frames):
        for j in range(num_frames):
            autocorrelations[i, j] = calculate_autocorrelation(frames[i], frames[j])

    return autocorrelations


# Построение 3D-графика автокорреляции и вида сверху
def plot_autocorrelation(autocorrelations):
    num_frames = autocorrelations.shape[0]
    X, Y = np.meshgrid(range(num_frames), range(num_frames))

    # Создание общей фигуры
    fig = plt.figure(figsize=(14, 8))

    # 3D-график
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(X, Y, autocorrelations, cmap='viridis')
    ax1.set_xlabel('Frame i')
    ax1.set_ylabel('Frame j')
    ax1.set_zlabel('Autocorrelation')
    ax1.set_title('3D Autocorrelation Plot')

    # Вид сверху (2D-проекция)
    ax2 = fig.add_subplot(122)
    cax = ax2.imshow(autocorrelations, cmap='viridis', origin='upper')
    ax2.set_xlabel('Frame j')
    ax2.set_ylabel('Frame i')
    ax2.set_title('Top View (2D Projection)')
    fig.colorbar(cax, ax=ax2, orientation='vertical', label='Autocorrelation')

    # Отображение графиков
    plt.tight_layout()
    plt.show()


# Путь к видео (замените на ваш файл)
video_path = 'lr1_3.AVI'

# Анализ видео и построение графиков
autocorrelations = analyze_video(video_path)
plot_autocorrelation(autocorrelations)
