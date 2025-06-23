import secrets
import os
from flask import Blueprint, redirect ,render_template ,url_for,request,current_app ,abort,flash
from flask_login import login_required ,current_user
from app.form import UpdateAccountForm , CreatePostForm
from app import db
from app.models import Post

main = Blueprint('main' , __name__)

@main.route('/')
# @login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('home.html', posts=posts)



# This function saves pic in our system 
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    form_picture.save(picture_path)
    return picture_fn


@main.route('/account' , methods = ['POST' , 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data)
            current_user.image = picture_file
 
        current_user.username = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect (url_for('main.account'))
    elif request.method == 'GET':
        form.name.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', form = form)

@main.route('/post' , methods= ['POST' ,'GET'])
@login_required
def post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data , content = form.content.data , author = current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))
        
    return render_template('post.html' , form = form)

@main.route('/post/<int:post_id>')
def  single_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template ('singlePost.html' , post = post)  

@main.route('/update_post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = CreatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('main.single_post', post_id=post.id))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('singlePost.html', post=post, form=form)

@main.route('/delete_post/<int:post_id>' , methods = ['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('main.home')) 




          