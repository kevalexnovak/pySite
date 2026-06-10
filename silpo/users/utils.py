import os # для роботи з файлами і папка в OS
from django.conf import settings #Налаштування конфігурація Django
from PIL import Image # Бібліотека для роботи з фото
import io # Робота з байтами
import uuid # Генерація унікальних імен файлів
from django.core.files.base import ContentFile # Файл, який передав користувач

def compress_image(image_field, size=(800,800), quality=85):
    # Якщо фото у PNG, перетворить у RGB
    image = Image.open(image_field).convert('RGB')
    #Зберігає оригільне співідношення сторін згідно size
    image.thumbnail(size, Image.LANCZOS)
    #Робимо ім'я фото - Рандом
    uid = str(uuid.uuid4())[:10] # 10 символів назви
    image_name = '{}.webp'.format(uid)
    # фото буде в пам'яті
    output = io.BytesIO()
    # перетвоюємо зображення
    image.save(output, format='WEBP', quality=quality)
    output.seek(0) #Зміщаємося на початок у пам'яті

    # отримуємо саме фото
    resized_image = ContentFile(output.getvalue())
    # Повертаємо назву фото і змінений розмір фото
    return resized_image, image_name

def save_custom_image(image, size, folder):
    resized_image, image_name = compress_image(image, size)
    # Створюємо шлях до директорії та шлях до файлу
    dir_path = os.path.join(settings.IMAGES_ROOT, folder)
    full_path = os.path.join(dir_path, image_name)
    # Створюємо папки, якщо їх ще не існує
    os.makedirs(dir_path, exist_ok=True)
    # Зберігаємо файл
    with open(full_path, "wb") as f:
        f.write(resized_image.read())
    return image_name