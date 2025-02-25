import os
import io
from PIL import Image
from flask import url_for, current_app
from enigma import mail
from enigma.cipher.file import encrypt_file, decrypt_file
from enigma.models import User
from flask_mail import Message
from base64 import b64encode
from werkzeug.datastructures.file_storage import FileStorage

# https://stackoverflow.com/questions/41718892/pillow-resizing-a-gif
def resize_image(form_picture:FileStorage):
    output_size = (128, 128)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    data = io.BytesIO()
    img.save(data, format=img.format)
    return data.getvalue()

def save_picture(form_picture:FileStorage, current_image:str):
    if current_image != os.getenv("DEFAULT_PROFILE_PICTURE"):
        cipher_path = os.path.join(current_app.root_path, "static", "profile_pics", current_image)
        os.remove(cipher_path)
    return encrypt_file(
        key=os.getenv("PROFILE_PICS_SECRET_KEY"),
        data=resize_image(form_picture),
        filename=form_picture.filename,
        path=os.path.join(current_app.root_path, "static", "profile_pics")
    )

def load_picture(image_file:str):
    cipher_path = os.path.join(current_app.root_path, "static", "profile_pics", image_file)
    plaintext, filename = decrypt_file(os.getenv("PROFILE_PICS_SECRET_KEY"), cipher_path)
    return f"data:image/{filename.split('.').pop()};base64,{b64encode(plaintext).decode('utf-8')}"

def send_reset_email(user:User):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender="noreply@enigma.com", recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    # We do not have a service for that at the moment.
    # mail.send(msg)

    # For now we print the token in the console.
    print(url_for('users.reset_token', token=token, _external=True))
