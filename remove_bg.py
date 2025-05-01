import os
from rembg import remove
from PIL import Image

# Pasta com as imagens de entrada
input_folder = 'images'
# Pasta onde as imagens com fundo removido serão salvas
output_folder = 'removed_bg_images'

# Cria a pasta de saída se não existir
os.makedirs(output_folder, exist_ok=True)

# Tipos de arquivos permitidos
image_extensions = ('.png', '.jpg', '.jpeg', '.webp')

for filename in os.listdir(input_folder):
    if filename.lower().endswith(image_extensions):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.png')  # saída sempre em PNG

        with Image.open(input_path) as img:
            img = img.convert("RGBA")
            result = remove(img)
            result.save(output_path)

        print(f'Fundo removido: {filename}')
