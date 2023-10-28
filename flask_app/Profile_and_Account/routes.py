# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Rayan Souissi - Youssef Alaoui - Aydan Guliyeva - Ho Yan Or

from datetime import date

# import today as today
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from sqlalchemy.orm import session
from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash
from wtforms.validators import url

from flask_app.models import Profile, User, Posts, Comments, Likes, Comment_Likes

from flask_app import db, photos, csrf
from flask_app.Profile_and_Account.forms import ProfileForm, PasswordForm, EmailForm, EditProfileForm, FirstNameForm, \
    LastNameForm, DateOfBirthForm

Profile_and_Account_bp = Blueprint('Profile_and_Account', __name__, url_prefix='/Profile_and_Account')


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


@Profile_and_Account_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()

    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')

        return redirect(url_for('Profile_and_Account.display_profile', username=profile.username, url=url))
    else:
        return redirect(url_for('Profile_and_Account.create_profile'))


@Profile_and_Account_bp.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()

    if request.method == 'POST' and form.validate_on_submit():

        filename = None
        if 'photo' in request.files:
            if request.files['photo'].filename != '':
                filename = photos.save(request.files['photo'])

        profile = Profile(username=form.username.data, photo=filename, bio=form.bio.data, gender=form.gender.data,
                          age=calculate_age(current_user.dob), user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()

        if profile:
            if profile.photo != None:
                url = photos.url(
                    profile.photo)  # uses the global photos plus the photo file name to determine the full url path
            else:
                url = url_for('static', filename='Default_Account_Image.png')
        else:
            url = url_for('static', filename='Default_Account_Image.png')

        return redirect(url_for('Profile_and_Account.display_profile', username=profile.username, url=url))

    url = url_for('static', filename='Default_Account_Image.png')

    return render_template('Profile_create_profile.html', form=form, url=url)


@Profile_and_Account_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    form = ProfileForm()

    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')
        return render_template('Profile_create_profile.html', form=form, url=url)

    form = ProfileForm(obj=profile)

    if request.method == 'POST' and form.validate_on_submit():
        if 'photo' in request.files:
            if request.files['photo'].filename != '':
                filename = photos.save(request.files['photo'])
                profile.photo = filename  # Updates the photo field
        user = current_user
        profile.bio = form.bio.data  # Updates the bio field
        profile.username = form.username.data  # Updates the user field
        profile.gender = form.gender.data
        profile.age = calculate_age(user.dob)
        db.session.commit()  # Save the changes to the database
        return redirect(url_for('Profile_and_Account.display_profile', username=profile.username, url=url))

    return render_template('Profile_edit_profile.html', form=form, url=url)


@Profile_and_Account_bp.route('/display_profile/<username>/', methods=['POST', 'GET'])
@login_required
def display_profile(username=None):
    current_profile = Profile.query.join(User).filter_by(id=current_user.id).first()

    if current_profile.photo != None:
        current_profile_url = photos.url(current_profile.photo)
    else:
        current_profile_url = url_for('static', filename='Default_Account_Image.png')

    if username != None:
        searched_profile = Profile.query.filter_by(username=username).first()
        searched_profile_posts = Posts.query.filter_by(profile_id=searched_profile.id)
        if searched_profile.photo != None:
            searched_profile_url = photos.url(searched_profile.photo)
        else:
            searched_profile_url = url_for('static', filename='Default_Account_Image.png')

    return render_template('Profile_display_profile.html', url=current_profile_url, profile=searched_profile,
                           searched_profile_url=searched_profile_url, posts=searched_profile_posts)


@Profile_and_Account_bp.route('/display_other_profile/<username>/', methods=['POST', 'GET'])
@login_required
def display_other_profile(username=None):
    current_profile = Profile.query.join(User).filter_by(id=current_user.id).first()

    if current_profile.photo != None:
        current_profile_url = photos.url(current_profile.photo)
    else:
        current_profile_url = url_for('static', filename='Default_Account_Image.png')

    if username != None:
        searched_profile = Profile.query.filter_by(username=username).first()
        searched_profile_posts = Posts.query.filter_by(profile_id=searched_profile.id)
        if searched_profile.photo != None:
            searched_profile_url = photos.url(searched_profile.photo)
        else:
            searched_profile_url = url_for('static', filename='Default_Account_Image.png')

    return render_template('Profile_display_other.html', url=current_profile_url, profile=searched_profile,
                           searched_profile_url=searched_profile_url, posts=searched_profile_posts)


@Profile_and_Account_bp.route('/display_profile', methods=['POST', 'GET'])
@Profile_and_Account_bp.route('/delete_profile', methods=['GET', 'POST'])
@login_required
def delete_profile():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    form = ProfileForm()
    posts = Posts.query.filter_by(profile_id=profile.id).all()
    comments = Comments.query.filter_by(profile_id=profile.id).all()
    likes = Likes.query.filter_by(profile_id=profile.id).all()
    comments_likes = Comment_Likes.query.filter_by(profile_id=profile.id).all()

    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')
        flash('Create a Profile before deleting one !', "warning")
        return render_template('Profile_create_profile.html', form=form, url=url)

    if request.method == 'POST':
        if profile:
            db.session.delete(profile)
            for post in posts:
                db.session.delete(post)
            for comment in comments:
                db.session.delete(comment)
            for like in likes:
                db.session.delete(like)
            for comment_like in comments_likes:
                db.session.delete(comment_like)
            db.session.commit()
            return redirect('/')
        abort(404)
    return render_template('Profile_delete_profile.html', url=url)


@Profile_and_Account_bp.route('/user_account', methods=['GET', 'POST'])
@login_required
def user_account():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')
    form = EditProfileForm()
    return render_template('UserAccount_display_account.html', form=form, url=url, profile=profile)


@Profile_and_Account_bp.route('/edit_account', methods=['GET', 'POST'])
@login_required
def edit_user_account():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')
    form = EditProfileForm()
    return render_template('UserAccount_edit_account.html', form=form, url=url, profile=profile)


@Profile_and_Account_bp.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_user_account():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()

    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')

    if request.method == 'POST':
        if current_user:
            db.session.delete(current_user)
            if profile:
                db.session.delete(profile)
                posts = Posts.query.filter_by(profile_id=profile.id).all()
                comments = Comments.query.filter_by(profile_id=profile.id).all()
                likes = Likes.query.filter_by(profile_id=profile.id).all()
                comments_likes = Comment_Likes.query.filter_by(profile_id=profile.id).all()
                for post in posts:
                    db.session.delete(post)
                for comment in comments:
                    db.session.delete(comment)
                for like in likes:
                    db.session.delete(like)
                for comment_like in comments_likes:
                    db.session.delete(comment_like)
            db.session.commit()
            return redirect(url_for("main.index"))
        abort(404)
    return render_template('UserAccount_delete_account.html', url=url)


@Profile_and_Account_bp.route('/edit_account', methods=['POST', 'GET'])
@Profile_and_Account_bp.route('/edit_account/password_change', methods=['POST', 'GET'])
@login_required
def user_account_password_change():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')
    form = PasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.password = generate_password_hash(form.new_password.data)
            db.session.add(user)
            db.session.commit()
            flash('Password has been updated!', 'success')
            return redirect(url_for("Profile_and_Account.user_account"))
    return render_template('UserAccount_change_password.html', form=form, url=url)


@Profile_and_Account_bp.route('/edit_account', methods=['POST', 'GET'])
@Profile_and_Account_bp.route('/edit_account/email_change', methods=['POST', 'GET'])
@login_required
def user_account_email_change():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')
    form = EmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.email = form.email.data
            db.session.add(user)
            db.session.commit()
            flash('Email has been updated!', 'success')
            return redirect(url_for("Profile_and_Account.user_account"))
    return render_template('UserAccount_change_email.html', form=form, url=url)


@Profile_and_Account_bp.route('/edit_account/firstname_change', methods=['POST', 'GET'])
@login_required
def user_account_firstname_change():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')
    form = FirstNameForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.firstname = form.firstname.data
            db.session.add(user)
            db.session.commit()
            flash('First name has been updated!', 'success')
            return redirect(url_for("Profile_and_Account.user_account"))
    return render_template('UserAccount_change_firstname.html', form=form, url=url)


@Profile_and_Account_bp.route('/edit_account/lastname_change', methods=['POST', 'GET'])
@login_required
def user_account_lastname_change():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')
    form = LastNameForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.lastname = form.lastname.data
            db.session.add(user)
            db.session.commit()
            flash('Last name has been updated!', 'success')
            return redirect(url_for("Profile_and_Account.user_account"))
    return render_template('UserAccount_change_lastname.html', form=form, url=url)


@Profile_and_Account_bp.route('/edit_account/date_of_birth_change', methods=['POST', 'GET'])
@login_required
def user_account_dob_change():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    if profile:
        if profile.photo != None:
            url = photos.url(
                profile.photo)  # uses the global photos plus the photo file name to determine the full url path
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = url_for('static', filename='Default_Account_Image.png')
    form = DateOfBirthForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.dob = form.dob.data
            db.session.add(user)
            db.session.commit()
            flash('Date of birth has been updated!', 'success')
            return redirect(url_for("Profile_and_Account.user_account"))
    return render_template('UserAccount_change_dob.html', form=form, url=url)
