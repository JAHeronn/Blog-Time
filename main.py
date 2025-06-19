from flask import Flask, render_template, redirect, url_for, request, flash, abort, render_template_string, jsonify
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, date
from forms import AddBlogPost, RegisterForm, LoginForm, CommentForm
from models import db, User, BlogPost, Comment
from seed import seed_demo_data
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
Bootstrap5(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['CKEDITOR_VERSION'] = '4.25.1-lts'
ckeditor = CKEditor(app)
DISABLE_AUTH = os.getenv("DISABLE_AUTH") == "true"

# calculating time since posted for comments
@app.template_filter('time_since')
def time_since(dt):
    now = datetime.now()
    diff = now - dt

    seconds = diff.total_seconds()
    if seconds < 60:
        s = int(seconds)
        return f"{s} second ago" if s == 1 else f"{s} seconds ago"
    elif seconds < 3600:
        m = int(seconds // 60)
        return f"{m} minute ago" if m == 1 else f"{m} minutes ago"
    elif seconds < 86400:
        h = int(seconds // 3600)
        return f"{h} hour ago" if h == 1 else f"{h} hours ago"
    elif seconds < 2592000:
        d = int(seconds // 86400)
        return f"{d} day ago" if d == 1 else f"{d} days ago"
    elif seconds < 31536000:
        mo = int(seconds // 2592000)
        return f"{mo} month ago" if mo == 1 else f"{mo} months ago"
    else:
        y = int(seconds // 31536000)
        return f"{y} year ago" if y == 1 else f"{y} years ago"

@app.context_processor
def inject_year():
    return { 'year': datetime.now().year }


# flask login configuration
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# db initialisation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db.init_app(app)
with app.app_context():
    db.create_all()
    seed_demo_data()

# create gravatar icons
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='identicon',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


# route for user registration
@app.route('/register', methods=["GET", "POST"])
def register():
    if DISABLE_AUTH:
        flash("Registration is disabled in the demo version.", "warning")
        return redirect(url_for("home"))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user:
            flash("That email is already in use, try logging in.")
            return redirect(url_for('login'))
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(email=form.email.data,
                        password=hash_and_salted_password,
                        name=form.name.data)

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template("register.html", form=form)

# route for user login
@app.route('/login', methods=["GET", "POST"])
def login():
    if DISABLE_AUTH:
        flash("Login is disabled in the demo version.", "warning")
        return redirect(url_for("home"))
    form = LoginForm()
    if request.method == "POST":
        email = form.email.data
        password = form.password.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Password was incorrect, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# route for the home page
@app.route('/')
def home():
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)


# route for viewing posts/comments and adding comments
@app.route('/post/<int:post_id>', methods=["GET", "POST"])
def show_post_and_comment(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    form = CommentForm()

    ordered_comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.date_posted.desc()).all()

    if request.method == "POST":
        if form.validate_on_submit():
            if not current_user.is_authenticated:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({
                        'success': False,
                        'error': 'You need to login or register to comment.'
                    })
                flash("You need to login or register to comment.")
                return redirect(url_for("login"))

            new_comment = Comment(
                text=form.comment_text.data,
                comment_author=current_user,
                parent_post=requested_post
            )
            db.session.add(new_comment)
            db.session.commit()

            # AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                comment_html = render_template('partials/_single_comment.html', comment=new_comment)
                return jsonify({
                    'success': True,
                    'comment_html': comment_html
                })
            return redirect(url_for('show_post_and_comment', post_id=post_id))
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'errors': form.errors
                })
    return render_template("post.html", post=requested_post, current_user=current_user, form=form, comments=ordered_comments)


# route for creating a post
@app.route('/new-post', methods=["GET", "POST"])
@login_required
def add_new_post():
    form = AddBlogPost()
    if form.validate_on_submit():
        current_day = date.today()
        formatted_date = current_day.strftime("%B %d, %Y")
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=formatted_date)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("create-post.html", form=form)


# routes for editing posts and comments
@app.route('/edit-post/<int:post_id>', methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    if current_user.id != 1 and current_user.id != requested_post.author_id:
        abort(403)
    form = AddBlogPost(title=requested_post.title,
                       subtitle=requested_post.subtitle,
                       img_url=requested_post.img_url,
                       body=requested_post.body)
    if form.validate_on_submit():
        requested_post.title = form.title.data
        requested_post.subtitle = form.subtitle.data
        requested_post.img_url = form.img_url.data
        requested_post.body = form.body.data
        db.session.commit()
        return redirect(url_for('show_post_and_comment', post_id=requested_post.id))
    return render_template("create-post.html", post=requested_post, form=form, edit_on=True)

@app.route("/edit-comment/<int:comment_id>", methods=["POST"])
@login_required
def edit_comment(comment_id):
    comment = db.get_or_404(Comment, comment_id)
    if current_user.id != comment.comment_author.id and current_user.id != 1:
        abort(403)
    new_text = request.form.get("text")
    if new_text:
        comment.text = new_text
        db.session.commit()
    updated_html = render_template("partials/_single_comment.html", comment=comment)

    return jsonify({"updated_html": updated_html})


# routes for deleting posts and comments
@app.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    if current_user.id != 1 and current_user.id != requested_post.author_id:
        abort(403)
    db.session.delete(requested_post)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/delete-comment/<int:comment_id>", methods=["DELETE"])
@login_required
def delete_comment(comment_id):
    comment = db.get_or_404(Comment, comment_id)
    if current_user.id != comment.comment_author.id and current_user.id != 1:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    return '', 204

# route for feature description page
@app.route("/features")
def feature_page():
    return render_template("features.html")

if __name__ == "__main__":
    app.run(debug=False)