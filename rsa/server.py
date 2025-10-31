from fastapi import FastAPI, Request
from generate_keys import generate_keys
from rsa import decrypt, encrypt
import uvicorn
import requests


def get_public_ip() -> str:
    return requests.get('https://api.ipify.org').text
    # return "31.159.41.34"


app = FastAPI()
keys: dict[str, int] = dict(zip(("n", "e", "d"), generate_keys(bits_len=5)))


@app.get("/public_key")
async def get_public_key() -> dict[str, int]:
    return {
        "n": keys["n"],
        "e": keys["e"],
    }


@app.post("/decrypt_message")
async def decrypt_message(request: Request):
    data = await request.json()
    message = data["message"]
    decrypted_text = decrypt(message, (keys["d"], keys["n"]))
    return {"message": decrypted_text}


@app.post("/encrypt_message")
async def encrypt_message(request: Request):
    data = await request.json()
    public_key = data["public_key"]
    message = f"Hello World! from ip {get_public_ip()}"
    message = bytes(message, "utf-8")
    encrypted_text = encrypt(message, public_key)
    return {"message": encrypted_text}



def main() -> None:
    """Entry point."""
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == '__main__':
    main()
