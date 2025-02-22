from enigma import create_app, db, argon2
from enigma.models import User, Post

from enigma.cipher.encrypt import encrypt_to_bytes, encrypt_to_base64
from enigma.cipher.decrypt import decrypt_from_bytes_to_utf8

app = create_app()

def create_dummy_database():
    with app.app_context():
        # Reset the database
        db.drop_all()
        db.create_all()

        # Create the users
        user_1 = User(username="Koro", email="koro@koro.com", password=argon2.generate_password_hash("1234"))
        user_2 = User(username="Orok", email="orok@orok.com", password=argon2.generate_password_hash("5678"))
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()
        print(user_1)
        print(user_2)

        # Create the posts
        for i in range(25):
            post = Post(title=f"Blog {i+1}", content=f"Post #{i+1}'s content!", user_id= user_1.id if i % 2 == 0 else user_2.id)
            db.session.add(post)
        db.session.commit()

        #
        print()
        key = "abc"
        plaintext = "This is a test"
        ciphertext = encrypt_to_bytes(key=key, plaintext=plaintext)
        result = decrypt_from_bytes_to_utf8(key=key, ciphertext=ciphertext)
        print(result)
        print()

if __name__ == "__main__":
    # create_dummy_database()
    app.run(debug=True)