from flask import Flask, render_template, request, redirect
from .forms import RegistrationForm, PostCreateForm, CommentForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from datetime import datetime
from flask_caching import Cache

app = Flask(__name__)
app.config["SECRET_KEY"] = "123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

cache = Cache(config={"CACHE_TYPE": "SimpleCache",
                      "CACHE_DEFAULT_TIMEOUT": 300})

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))


class Commenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    post = db.Column(db.Integer, db.ForeignKey("post.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False, default="")
    email = db.Column(db.String(50), nullable=False, unique=True)


@login.user_loader
def user_loader(id):
    return User.query.get(id)


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    posts = Post.query.all()
    current_user.is_authenticated()
    return render_template('home.html', post=posts, user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(name=username).first()
        if user is None or user.password != password:
            return redirect("/login")
        login_user(user, remember=form.remember_me.data)
        #cache.set("user", user)
        #cache.get("user")
        return redirect("/")
    return render_template("login.html", form=form)


@app.route("/1", methods=["GET", "POST"])
def form():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        email = form.email.data
        user = User(name=name, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("form.html", form=form)


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    form = PostCreateForm()
    if form.validate_on_submit():
        text = form.text.data
        post = Post(text=text, user=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    return render_template('post_create.html', form=form)


@app.route("/post/<int:id>", methods=["GET", "POST"])
def page_2(id):
    p = Post.query.get(id)
    comments = Commenta.query.filter_by(post=id)
    form = PostCreateForm()
    if form.validate_on_submit():
        text = form.text.data
        new_comment = Commenta(text=text, user=current_user.id, post=1)
        db.session.add(new_comment)
        db.session.commit()
        return redirect("/post")
    return render_template("post.html", form=form, post=p, comments=comments)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")