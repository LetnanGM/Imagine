import os
import uuid
import mimetypes

from io import BytesIO
from datetime import datetime, timezone
from typing import Callable, Dict, Tuple, Any

import requests

from PIL import Image as PILImage


class SetImagine:
    outfile = "output"


class ImageHandler:
    """
    Universal Smart Image Handler Registry
    """

    _handlers: Dict[type, Callable] = {}

    @classmethod
    def register(cls, target_type: type):

        def decorator(func: Callable):
            cls._handlers[target_type] = func
            return func

        return decorator

    @classmethod
    def process(cls, obj: Any, save_path: str) -> Tuple[bool, str]:

        for target_type, handler in cls._handlers.items():

            if isinstance(obj, target_type):
                return handler(obj, save_path)

        return False, f"No handler for type: {type(obj)}"


class Image:
    """
    Universal Image Save Manager
    """

    def __init__(self):

        self._current_process: str = None
        self._current_fullpath: str = None

        os.makedirs(SetImagine.outfile, exist_ok=True)

    @property
    def current_fullpath(self) -> str:
        return self._current_fullpath

    @property
    def current_process(self) -> str:
        return self._current_process

    def _current_date(self) -> str:

        return datetime.now(
            timezone.utc
        ).strftime("%Y%m%d_%H%M%S")

    def _generate_filename(self, ext="png") -> str:

        return (
            f"temp_TR{self._current_date()}"
            f"_ST{uuid.uuid4().hex}.{ext}"
        )

    def save(
        self,
        data: dict
    ) -> Tuple[bool, str]:

        """
        Expected format:

        {
            "part": Any
        }
        """

        if not data:
            raise ValueError("'data' cannot be empty")

        part = data.get("part")

        filename = self._generate_filename()
        self._current_fullpath = os.path.join(
            SetImagine.outfile,
            filename
        )

        result = ImageHandler.process(
            part,
            self._current_fullpath
        )

        return result

    def __repr__(self):

        return (
            f"<Image "
            f"fullpath={self.current_fullpath}>"
        )


# =========================================================
# HANDLER: PIL IMAGE
# =========================================================

@ImageHandler.register(PILImage.Image)
def handle_pil_image(
    image: PILImage.Image,
    save_path: str
):

    image.save(save_path)

    return True, save_path


# =========================================================
# HANDLER: BYTES
# =========================================================

@ImageHandler.register(bytes)
def handle_bytes(
    data: bytes,
    save_path: str
):

    image = PILImage.open(
        BytesIO(data)
    )

    image.save(save_path)

    return True, save_path


# =========================================================
# HANDLER: BYTEARRAY
# =========================================================

@ImageHandler.register(bytearray)
def handle_bytearray(
    data: bytearray,
    save_path: str
):

    image = PILImage.open(
        BytesIO(data)
    )

    image.save(save_path)

    return True, save_path


# =========================================================
# HANDLER: BytesIO
# =========================================================

@ImageHandler.register(BytesIO)
def handle_bytesio(
    data: BytesIO,
    save_path: str
):

    image = PILImage.open(data)

    image.save(save_path)

    return True, save_path


# =========================================================
# HANDLER: REQUESTS RESPONSE
# =========================================================

@ImageHandler.register(requests.Response)
def handle_requests_response(
    response: requests.Response,
    save_path: str
):

    image = PILImage.open(
        BytesIO(response.content)
    )

    image.save(save_path)

    return True, save_path


# =========================================================
# HANDLER: URL STRING
# =========================================================

@ImageHandler.register(str)
def handle_url_or_path(
    value: str,
    save_path: str
):

    # URL
    if value.startswith("http://") or value.startswith("https://"):

        response = requests.get(value)

        image = PILImage.open(
            BytesIO(response.content)
        )

        image.save(save_path)

        return True, save_path

    # LOCAL FILE
    elif os.path.exists(value):

        image = PILImage.open(value)

        image.save(save_path)

        return True, save_path

    return False, "Invalid string source"