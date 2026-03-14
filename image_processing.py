from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

class ImageProcessing:

    def __init__(self):
        self.img = None
        self.image_width = None
        self.image_height = None
        self.x = None
        self.y = None

    def watermark(self, photo: str, text: str, path:str) -> None:
        self.img = Image.open(f"{photo}").convert(mode="RGBA")
        self.image_width, self.image_height = self.img.size
        self.x = 0.0
        self.y = 0.0

        font = ImageFont.load_default(size=500)
        text_layer = Image.new("RGBA", self.img.size, (255, 255, 255, 0))
        draw_text_layer = ImageDraw.Draw(text_layer)

        pos = draw_text_layer.textbbox((0, 0), text=text, font=font)
        self.x = (self.image_width - (pos[2] - pos[0])) / 2
        self.y = (self.image_height - (pos[3] - pos[1])) / 2

        draw_text_layer.text((self.x, self.y), text, fill=(0, 0, 0, 150), font=font)

        self.img = Image.alpha_composite(self.img, text_layer)
        print(path + photo.split('/')[-1])
        self.img.convert("RGB").save(path + '/' + photo.split('/')[-1])


