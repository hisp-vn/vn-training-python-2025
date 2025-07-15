import io
import os
from datetime import datetime, timedelta, timezone

import base45
import qrcode
import typer
from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from joserfc import jwt
from joserfc.jwk import OctKey
from pydantic import BaseModel

app = FastAPI(redirect_slashes=True)


HS256_SECRET_KEY: str = os.getenv("HS256_SECRET_KEY", "supersecretkey")
SECRET_KEY = OctKey.import_key(HS256_SECRET_KEY)


class UserIn(BaseModel):
    name: str


def jwt_hs256_sign(user: UserIn):
    header = {"alg": "HS256"}

    token = user.model_dump()
    token["exp"] = int((datetime.now(timezone.utc) + timedelta(minutes=60)).timestamp())

    token = jwt.encode(header, token, SECRET_KEY)
    token = base45.b45encode(token.encode()).decode()

    typer.echo(f"🔐 Signed JWT: {token}")

    return token


def jwt_hs256_verify(token: str):
    try:
        decoded_base45 = base45.b45decode(token)
        decoded_token = jwt.decode(decoded_base45, SECRET_KEY)
        return decoded_token

    except Exception as e:
        raise HTTPException(status_code=409, detail=f"JWT Verification Failed: {str(e)}")

    return None


@app.post("/", response_class=StreamingResponse)
def get_signed_qr(user: UserIn):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=8,
        border=2,
    )

    qr.add_data(jwt_hs256_sign(user))
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    return StreamingResponse(img_io, media_type="image/png")


@app.post("/verify")
def verify_jwt(body: str = Body(..., media_type="text/plain")):
    return {"data": jwt_hs256_verify(body)}
