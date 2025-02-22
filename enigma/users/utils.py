import os
from PIL import Image
from flask import url_for, current_app
from enigma import mail
from enigma.cipher.file import encrypt_file, decrypt_file
from flask_mail import Message
from base64 import b64encode

def save_picture(form_picture):
    # random_hex = secrets.token_hex(8)
    # _, f_ext = os.path.splitext(form_picture.filename)
    # picture_fn = random_hex + f_ext
    # picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_fn)

    # print(form_picture.read())

    # Resize image
    # output_size = (125, 125)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)
    # i.save(picture_path)

    return encrypt_file(os.getenv("PROFILE_PICS_SECRET_KEY"), form_picture).split(os.path.sep).pop()

def load_picture(image_file):
    if image_file != "default.jpg":
        cipher_path = os.path.join(current_app.root_path, "static", "profile_pics", image_file)
        plaintext, filename = decrypt_file(os.getenv("PROFILE_PICS_SECRET_KEY"), cipher_path)
        return f"data:image/{filename.split('.').pop()};base64,{b64encode(plaintext).decode('utf-8')}"
    else:
        return url_for("static", filename=f"profile_pics/{image_file}")

def send_reset_email(user):
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
