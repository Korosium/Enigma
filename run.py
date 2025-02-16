from enigma import app, db
from enigma.models import User, Post

def create_dummy_database():
    with app.app_context():
        # Reset the database
        db.drop_all()
        db.create_all()

        # Create the users
        user_1 = User(username="Koro", email="totally@legit.com", password="1234")
        db.session.add(user_1)
        db.session.commit()

        # Create the posts
        post_1 = Post(title="Blog 1", content="First Post Content!", user_id=user_1.id)
        post_2 = Post(title="Blog 2", content="Second Post Content!", user_id=user_1.id)
        db.session.add(post_1)
        db.session.add(post_2)
        db.session.commit()

if __name__ == "__main__":
    create_dummy_database()
    app.run(debug=True)