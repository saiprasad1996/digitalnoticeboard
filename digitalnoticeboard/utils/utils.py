import hashlib
import base64


def base64ofsha(input):
    s = hashlib.sha256(input.encode('utf-8')).digest()
    return str(base64.b64encode(s), encoding="utf-8")
