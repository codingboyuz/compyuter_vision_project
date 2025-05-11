import base64  # Rasmni base64 formatga o‘tkazish uchun
from io import BytesIO  # Rasmni xotirada vaqtincha saqlash uchun

import cv2
from PIL import Image  # Rasmni PNG formatga o‘tkazish uchun (Pillow kutubxonasi)



class FrameConvert:
    def __init__(self, format):
        self.format = format


    def convert(self,frame):
        # BGR -> RGB convert
        rgb_image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        # PIL Image ga o'tkazish
        pil_image = Image.fromarray(rgb_image)
        # Bufferga yozib saqlash
        buffer  = BytesIO()

        pil_image.save(buffer,format=self.format)
        img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return img_b64
