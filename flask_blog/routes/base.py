from flask import render_template
from flask_login import current_user

from .utils import posts_not_deleted, posts_deleted
from .. import app
from ..forms import PostForm
from ..repository import db
from ..repository.model import User, Post


@app.route('/')
def index():
    return render_template('main.html', user=current_user, current_user=current_user)


# noinspection PyShadowingNames
@app.route('/user/<login>')
def user(login: str):
    user: User = User.query.filter_by(login=login).first_or_404(description=f'No user with login {login}')
    # noinspection PyUnresolvedReferences
    posts: list[Post] = posts_not_deleted().filter(Post.author == user).order_by(Post.created_at.desc()).all()
    return render_template('user.html', title=f"Hello, {user.login}",
                           user=user, current_user=current_user, posts=posts)


# noinspection PyShadowingNames
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    user: User = current_user

    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, text_content=form.text_content.data, author=user)
        db.session.add(post)
        db.session.commit()
    # noinspection PyUnresolvedReferences
    posts: list[Post] = posts_not_deleted().order_by(Post.created_at.desc()).all()
    return render_template('post/post_list.html', title='Live posts', user=user,
                           current_user=current_user, posts=posts, form=form)


# noinspection PyShadowingNames
@app.route('/deleted_posts')
def deleted_posts():
    user: User = current_user
    # noinspection PyUnresolvedReferences
    deleted_posts: list[Post] = posts_deleted().filter(Post.author == user).order_by(Post.created_at.desc()).all()
    return render_template('post/deleted_post_list.html', title='Deleted posts',
                           user=user, current_user=user, deleted_posts=deleted_posts)
