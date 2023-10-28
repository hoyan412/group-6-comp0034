# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Rayan Souissi - Bailey Roberts - Youssef Alaoui - Ho Yan Or


import functools

from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from sqlalchemy.orm import session
from werkzeug.security import generate_password_hash
from flask_app.models import Profile, User, Posts, Comments, Likes, Comment_Likes
from flask_app.community.forms import PostForm, CommentForm

from flask_app import db, photos, csrf, login_manager

community_bp = Blueprint('community', __name__, url_prefix='/community')


def profile_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        current_profile = Profile.query.join(User).filter_by(id=current_user.id).first()
        if current_profile is None:
            flash(f"You must create a profile to access the community.\n", "warning")
            return redirect(url_for('Profile_and_Account.create_profile'))

        return view(**kwargs)

    return wrapped_view


@community_bp.route('/')
@login_required
@profile_required
def index():
    profiles = Profile.query
    posts = Posts.query.order_by(Posts.timestamp)
    comments = Comments.query
    likes = Likes.query
    current_profile = Profile.query.join(User).filter_by(id=current_user.id).first()

    if current_profile:
        if current_profile.photo != None:
            url = photos.url(
                current_profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')

    for profile in profiles:
        if profile.photo != None:
            profile.photo = photos.url(profile.photo)
        else:
            profile.photo = url_for('static', filename='Default_Account_Image.png')

    return render_template('Community_page_index.html', title="Community", posts=posts, comments=comments,
                           profiles=profiles, likes=likes, url=url)


@community_bp.route('/create_post', methods=['GET', 'POST'])
@login_required
@profile_required
def create_post():
    profile = Profile.query.filter_by(user_id=current_user.id).first()

    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')

        name = ""
        if not current_user.is_anonymous:
            name = current_user.firstname

        form = PostForm()
        if form.validate_on_submit():
            profile = Profile.query.filter_by(user_id=current_user.id).first()
            post = Posts(body=form.post.data, title=form.post_title.data, profile_id=profile.id)
            db.session.add(post)
            db.session.commit()
            flash('Your post is now live!', "success")
            return redirect(url_for('community.index', url=url))

        return render_template('Community_create_post.html', form=form,
                               name=name, url=url)
    else:
        return redirect(url_for('Profile_and_Account.create_profile'))


@community_bp.route('/<int:post_id>', methods=['GET', 'POST'])
@login_required
@profile_required
def get_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    comments = Comments.query.filter_by(post_id=post_id)
    profiles = Profile.query
    current_profile = Profile.query.filter_by(user_id=current_user.id).first()
    like = Likes.query.filter_by(post_id=post.id, profile_id=current_profile.id).first()
    likes = Likes.query.filter_by(post_id=post.id).count()

    if current_profile:
        if current_profile.photo != None:
            url = photos.url(
                current_profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')

    for profile in profiles:
        if profile.photo != None:
            profile.photo = photos.url(profile.photo)
        else:
            profile.photo = url_for('static', filename='Default_Account_Image.png')

    return render_template('Community_show_specific_post.html', post=post, comments=comments, profiles=profiles,
                           current_profile=current_profile, Comment_Likes=Comment_Likes, url=url, likes=likes,
                           like=like)


@community_bp.route('/<int:post_id>')
@community_bp.route('<int:post_id>/post_comment', methods=['GET', 'POST'])
@login_required
@profile_required
def write_comment(post_id):
    profile = Profile.query.filter_by(user_id=current_user.id).first()

    if profile:
        if profile.photo != None:
            url = photos.url(profile.photo)
        else:
            url = url_for('static', filename='Default_Account_Image.png')

        form = CommentForm()
        post = Posts.query.filter_by(id=post_id).first()
        if form.validate_on_submit():
            profile = Profile.query.filter_by(user_id=current_user.id).first()
            comment = Comments(body=form.comment.data, profile_id=profile.id, post_id=post_id, )
            db.session.add(comment)
            db.session.commit()
            flash('Your comment is now live!', "success")
            return redirect(url_for('community.get_post', post_id=post.id))
        return render_template('Community_write_comment.html', form=form, post=post, url=url)

    else:
        return redirect(url_for('Profile_and_Account.create_profile'))


@community_bp.route('/<int:post_id>')
@community_bp.route('<int:post_id>/edit_post', methods=['GET', 'POST'])
@login_required
@profile_required
def edit_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    form = PostForm(obj=post)
    name = current_user.firstname
    profile = Profile.query.filter_by(user_id=current_user.id).first()

    if profile:
        if profile.photo != None:
            url = photos.url(profile.photo)
        else:
            url = url_for('static', filename='Default_Account_Image.png')

        if form.validate_on_submit() and post.profile_id == profile.id:
            post.body = form.post.data
            post.title = form.post_title.data
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('community.get_post', post_id=post.id))

    return render_template('Community_edit_post.html', form=form, name=name, url=url)


@community_bp.route('/<int:post_id>')
@community_bp.route('<int:post_id>/like_post', methods=['GET', 'POST'])
@login_required
@profile_required
def like_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    profile = Profile.query.filter_by(user_id=current_user.id).first()

    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')

        if request.method == 'POST':
            like = Likes(profile_id=profile.id, post_id=post.id)
            db.session.add(like)
            db.session.commit()
            flash('You have liked this post', "success")
            return redirect(url_for('community.get_post', post_id=post.id, like=like, url=url))
    else:
        url = url_for('static', filename='Default_Account_Image.png')

    return render_template('Community_show_specific_post.html', url=url)


@community_bp.route('/<int:post_id>')
@community_bp.route('<int:post_id>/unlike_post', methods=['GET', 'POST'])
@login_required
@profile_required
def unlike_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    like = Likes.query.filter_by(profile_id=profile.id, post_id=post.id).first()

    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')

    if request.method == 'POST':
        db.session.delete(like)
        db.session.commit()
        flash('You have unliked this post', "danger")
        return redirect(url_for('community.get_post', post_id=post.id, like=like, url=url))

    return render_template('Community_show_specific_post.html', url=url)


@community_bp.route('/<int:post_id>')
@community_bp.route('<int:post_id>/<int:comment_id>/edit_comment', methods=['GET', 'POST'])
@login_required
@profile_required
def edit_comment(post_id, comment_id):
    form = CommentForm()
    post = Posts.query.filter_by(id=post_id).first()
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    comment = Comments.query.filter_by(post_id=post_id, id=comment_id).first()

    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')

    if form.validate_on_submit() and profile.id == comment.profile_id:
        comment.body = form.comment.data
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been updated', "info")
        return redirect(url_for('community.get_post', post_id=post.id, url=url))

    return render_template('Community_write_comment.html', form=form, post=post, url=url)


@community_bp.route('/<int:post_id>')
@community_bp.route('<int:post_id>/delete_post', methods=['GET', 'POST'])
@login_required
@profile_required
def delete_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    profile = Profile.query.filter_by(user_id=current_user.id).first()

    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
        if profile.id == post.profile_id and request.method == 'POST':
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('community.index'))
    else:
        url = url_for('static', filename='Default_Account_Image.png')

    return render_template('Community_delete_post.html', post=post, url=url)


@community_bp.route('/<int:post_id>')
@community_bp.route('<int:post_id>/<int:comment_id>/delete_comment', methods=['GET', 'POST'])
@login_required
@profile_required
def delete_comment(post_id, comment_id):
    post = Posts.query.filter_by(id=post_id).first()
    profile = Profile.query.filter_by(user_id=current_user.id).first()

    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')

    comment = Comments.query.filter_by(post_id=post_id, id=comment_id).first()
    if request.method == 'POST' and profile.id == comment.profile_id:
        db.session.delete(comment)
        db.session.commit()
        flash('Your comment has been deleted', "danger")
        return redirect(url_for('community.get_post', post_id=post.id, url=url))

    return render_template('Community_delete_comment.html', post=post, url=url)


@community_bp.route('/<int:post_id>')
@community_bp.route('<int:post_id>/<int:comment_id>/like_comment', methods=['GET', 'POST'])
@login_required
@profile_required
def like_comment(post_id, comment_id):
    post = Posts.query.filter_by(id=post_id).first()
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    comment = Comments.query.filter_by(post_id=post_id, id=comment_id).first()

    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')

    if request.method == 'POST':
        comment_like = Comment_Likes(profile_id=profile.id, comment_id=comment.id, post_id=post.id)
        db.session.add(comment_like)
        db.session.commit()
        flash('You have liked this comment', "info")
        return redirect(url_for('community.get_post', post_id=post.id, url=url))

    return render_template('community.get_post.html', post=post, url=url)


@community_bp.route('/<int:post_id>')
@community_bp.route('<int:post_id>/<int:comment_id>/unlike_comment', methods=['GET', 'POST'])
@login_required
@profile_required
def unlike_comment(post_id, comment_id):
    post = Posts.query.filter_by(id=post_id).first()
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    comment = Comments.query.filter_by(post_id=post_id, id=comment_id).first()
    comment_like = Comment_Likes.query.filter_by(profile_id=profile.id, comment_id=comment.id, post_id=post.id).first()

    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')

    if request.method == 'POST':
        db.session.delete(comment_like)
        db.session.commit()
        flash('You have unliked this comment', "danger")
        return redirect(url_for('community.get_post', post_id=post.id, url=url))

    return render_template('community.get_post.html', post=post, url=url)


@community_bp.route('/search_results', methods=['POST', 'GET'])
@login_required
@profile_required
def search_bar_results(username=None):
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    if profile:
        if profile.photo != None:
            current_url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            current_url = url_for('static', filename='Default_Account_Image.png')

    if username is None:
        if request.method == 'POST':
            term = request.form['search_term']
            if term == "":
                flash("Search for a user profile", "warning")
                return redirect(url_for("main.index"))
            results = Profile.query.filter(Profile.username.contains(term)).all()
            posts = Posts.query.filter(Posts.title.contains(term)).all()
    else:
        results = Profile.query.filter_by(username=username).all()
        posts = Posts.query.filter_by(title=username).all()

    if not results:
        if not posts:
            flash("No users or posts found.", "danger")
            return redirect(url_for("main.index"))

    urls = []
    for result in results:
        if result.photo != None:
            url = photos.url(
                result.photo)  # uses the global photos plus the photo file name to determine the full url path
            urls.append(url)
        else:
            url = url_for('static', filename='Default_Account_Image.png')
            urls.append(url)

    return render_template('Search_bar_results.html', results=zip(results, urls), url=current_url, posts=posts)
