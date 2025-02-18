import aiohttp
from src.config import settings
from zlib import compress
import string
import base64
from aiogram.types import BufferedInputFile
from datetime import datetime

plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
base64_alphabet   = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
b64_to_plantuml = bytes.maketrans(base64_alphabet.encode('utf-8'), plantuml_alphabet.encode('utf-8'))

def deflate_and_encode(plantuml_text):
    zlibbed_str = compress(plantuml_text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string).translate(b64_to_plantuml).decode('utf-8')

class PlantUML:
    def __init__(self, url: str | None = None):
        self.url = url or settings.UML_SERVER_URL
        self.session = aiohttp.ClientSession


    async def process(self, text: string):
        converted = deflate_and_encode(text)
        if self.url.endswith('/'):
            url = self.url + converted
        else:
            url = self.url + '/' + converted

        async with self.session() as s:
            async with s.get(url) as response:
                if response.status == 200:
                    f = await response.read()
                    return BufferedInputFile(f, f"{datetime.timestamp(datetime.now())}.png")
                else:
                    raise Exception(f'Server responded with code: {response.status}')

generator = PlantUML()