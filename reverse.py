import av


def reverse_video(input_file, output_file):
    try:
        # Открываем входное видео
        container = av.open(input_file)
        # Создаем контейнер для выходного видео
        output_container = av.open(output_file, mode='w')

        # Получаем поток видео
        input_stream = container.streams.video[0]

        # Создаем поток для выходного файла с теми же параметрами
        output_stream = output_container.add_stream(
            codec_name=input_stream.codec_context.codec.name,
            time_base=input_stream.time_base
        )
        output_stream.width = input_stream.codec_context.width
        output_stream.height = input_stream.codec_context.height
        output_stream.pix_fmt = input_stream.codec_context.pix_fmt

        # Читаем все кадры и сохраняем их в список
        frames = [frame for frame in container.decode(video=0)]

        # Обратный порядок кадров
        for frame in reversed(frames):
            # Перекодируем и записываем кадры в выходной файл
            for packet in output_stream.encode(frame):
                output_container.mux(packet)

        # Закрываем потоки
        for packet in output_stream.encode():
            output_container.mux(packet)

        container.close()
        output_container.close()
        print("Видео успешно обработано и сохранено в", output_file)
    except Exception as e:
        print("Ошибка при обработке видео:", e)


# Входной и выходной файлы
input_file = "lr1_1.AVI"
output_file = "reversed_lr1_1.AVI"

reverse_video(input_file, output_file)
