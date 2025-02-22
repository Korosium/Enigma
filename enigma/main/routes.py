from flask import Blueprint, request, render_template
from enigma.models import Post
from enigma.users.utils import load_picture

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, load_picture=load_picture)

@main.route("/about")
def about():
    return render_template('about.html', title="About")
