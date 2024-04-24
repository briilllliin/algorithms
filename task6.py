import random
from PIL import Image, ImageDraw
from bitarray._bitarray import bitarray
from bitarray.util import int2ba

def embed_text(image_path, text, lamb=0.7, sigma=3, K0=42):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()

    bit_chars = []
    for char in text:
        bites = [1 if i else 0 for i in int2ba(char)]
        bit_chars.append(([0] * (8 - len(bites)) + bites))

    random.seed(K0)

    for i in range(len(bit_chars)):
        for j in range(len(bit_chars[i])):
            count = i * len(bit_chars) + j

            x = random.uniform(sigma, width - sigma)
            y = random.uniform(sigma, height - sigma)

            r, g, b = pix[x, y]
            power = 0.3 * r + 0.59 * g + 0.11 * b

            b += int((2 * bit_chars[i][j] - 1) * lamb * power)

            if b < 0:
                b = 0
            if b > 255:
                b = 255
            draw.point((x, y), (r, g, b))

    image.save("temp_with_secret.png", "PNG")
    print('Скрытие информации завершено')

def extract_text(image_path, sigma=3, K0=42):
    image = Image.open(image_path)
    pix = image.load()
    random.seed(K0)

    width = image.size[0]
    height = image.size[1]
    res = bitarray()
    for i in range(sigma, width - sigma):
        for j in range(sigma, height - sigma):
            x = random.uniform(sigma, width - sigma)
            y = random.uniform(sigma, height - sigma)

            temp_b = 0
            b = pix[x, y][2]
            for k in range(1, sigma + 1):
                bt = pix[x, y + k][2]
                bd = pix[x, y - k][2]
                bl = pix[x - k, y][2]
                br = pix[x, y + k][2]
                temp_b += bt + bd + bl + br
            temp_b /= 4 * sigma

            res += [temp_b < b]

    return res.tobytes()

# Пример использования
text = b'Very very secret text'
embed_text("temp.jpg", text)
extracted_text = extract_text("temp_with_secret.png")
print(extracted_text)
