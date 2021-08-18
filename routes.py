import os
import secrets
from PIL import Image
from flask import render_template,url_for,flash,redirect,request ,abort
from App import app ,db,bcrypt ,mail 
from App.forms import RegisterationForm, LoginForm ,UpdateAccountForm ,PostForm ,OrderForm ,RequestResetForm, ResetPasswordForm ,GalleryForm ,FeedbackForm
from App.models import Feedback, User , Post ,Order ,Gallery
from flask_login import login_user ,current_user , login_required , logout_user
from flask_mail import Message

@app.route('/')
@app.route('/home')
def home():
    page= request.args.get('page',1,type=int)
    q= request.args.get('q')
    if q:
         users=User.query.filter(User.username.contains(q)).paginate(page=page ,per_page=6)
         posts=Post.query.filter(Post.title.contains(q) | Post.caption.contains(q)).paginate(page=page ,per_page=12)
         return render_template('search.html',posts=posts,users=users,q=q)
    else:
        posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page ,per_page=18)
    return render_template('home.html',posts=posts)

@app.route('/c/<string:category>')
def categorie(category):
    c = category[1:]
    page= request.args.get('page',1,type=int)
    posts=Post.query.filter(Post.caption.contains(c)).paginate(page=page ,per_page=18)
    return render_template('home.html',posts=posts)
@app.route('/toprate')
def toprate():
    page= request.args.get('page',1,type=int)
    posts=Post.query.order_by(Post.scoresum.desc()).paginate(page=page,per_page=18)
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/dash')
@login_required
def dash():
    if current_user.id < 2:
         return render_template('orderadmin.html',title='dashboard')
    abort(403)

    

@app.route('/register',methods =['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data, email= form.email.data ,phone=form.phone.data ,password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in ','success')
        return redirect(url_for('login'))
    return render_template('register.html',title = 'Register',form=form)

@app.route('/login',methods =['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html',title = 'Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
def save_picture(form_picture,code):
    f_name , f_ext = os.path.splitext(form_picture.filename)
    picture_fn= code + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
    output_size = (480,480)
    i =Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
def save_design(form_picture,code):
    f_name , f_ext = os.path.splitext(form_picture.filename)
    picture_fn= code + f_ext
    picture_path = os.path.join(app.root_path,'static/design_pics',picture_fn)
    output_size = (1280,960)
    i =Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn 

def save_file(d_file,code):
    f_name , f_ext = os.path.splitext(d_file.filename)
    d_fn = code + f_ext
    d_path  = os.path.join(app.root_path,'static/design_files',d_fn)
    d_file.save(d_path)
    return d_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='printshipllc@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)


@app.route("/account",methods =['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file= save_picture(form.picture.data,current_user.id)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Account updated successfuly' , 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.bio.data = current_user.bio

    image_file= url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',image_file= image_file , form=form)



@app.route("/post/new",methods =['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    random_hex= secrets.token_hex(8)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file= save_design(form.picture.data,random_hex)
            designfile= save_file(form.dfile.data,random_hex)
            post=Post(title=form.title.data,caption=form.caption.data, image_file=picture_file ,author=current_user,dfile=designfile)
        db.session.add(post)
        db.session.commit()
        flash('Post Added Successfuly' , 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',form=form,legend='Create Post')
@app.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    orders=Order.query.filter_by(product=post).paginate()
    gallery = Gallery.query.filter_by(product=post).paginate()
    feedback = Feedback.query.filter_by(rate=post).paginate()
    return render_template('post.html',title=post.title,post=post,orders=orders,gallery=gallery,feedback=feedback)

@app.route("/post/<int:post_id>/share")
def share_post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('share.html',title=post.title,post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    f_name , f_ext = os.path.splitext(post.picture_file.filename)
    if form.validate_on_submit():
        picture_file= save_design(form.picture.data,f_name)
        designfile= save_file(form.dfile.data,f_name)
        post.image_file=picture_file
        post.dfile= designfile
        post.title = form.title.data
        post.caption = form.caption.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.caption.data = post.caption
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post',post=post)

@app.route("/post/<int:post_id>/AddImage", methods=['GET', 'POST'])
@login_required
def Add_image(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = GalleryForm()
    random_hex= secrets.token_hex(8)
    if form.validate_on_submit():
        for file in form.ig.data:
            picture_file= save_design(file,random_hex)
            gallery =Gallery(ig=picture_file ,product =post)
            db.session.add(gallery)
        db.session.commit()
        flash('Pic added Successfuly' , 'success')
        return redirect(url_for('home'))
    return render_template('addimage.html', title='Adding to gallery',form=form,post=post)



@app.route("/post/<int:post_id>/delete",methods =['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user :
        abort(403)
    post.title = "*Deleted*"
    db.session.commit()
    flash('Post Deleted Successfuly' , 'success')
    return redirect(url_for('home'))

@app.route('/user/<string:username>')
def user_posts(username):
    page= request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page ,per_page=6)
    return render_template('user_posts.html',posts=posts,user=user) 

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)



@app.route("/post/<int:post_id>/order",methods =['GET','POST'])
def order_post(post_id):
    post=Post.query.get_or_404(post_id)
    form = OrderForm()
    author= post.author
    if form.validate_on_submit():
        cash=0
        if form.material.data =='Mug 50 LE':
            cash= 50*form.qty.data
        if form.material.data =='T-shirt 200LE':
             cash= 200*form.qty.data
        if form.material.data =='hoodi 300LE':
             cash= 300*form.qty.data
        order=Order(material=form.material.data,name=form.name.data,address=form.location.data,size = form.size.data,phone=form.phone.data,phone2=form.phone2.data,color=form.color.data,qty=form.qty.data ,owner=author,product =post , cash=cash)
        db.session.add(order)
        db.session.commit()
        flash('Order placed Successfuly & total amount is : '+cash+' L.E' , 'success')
        return redirect(url_for('home'))
    return render_template('create_order.html', title='New Order',form=form,post=post)

@app.route("/post/<int:post_id>/feedback",methods =['GET','POST'])
@login_required
def feedback_post(post_id):
    post=Post.query.get_or_404(post_id)
    form = FeedbackForm()
    cond1 = 0
    cond1 = Feedback.query.filter_by(rate= post,critic= current_user).first()
    if cond1:
        flash('Already Rated' , 'warning')
        return redirect(url_for('post', post_id = post.id))
    else:
        if form.validate_on_submit():
            feedback=Feedback(score=form.score.data,cont=form.cont.data ,rate=post,critic=current_user)
            post.scorecount +=1
            post.scoresum = post.scoresum+form.score.data
            db.session.add(feedback)
            db.session.commit()
            flash('Feedback submitted  Successfuly' , 'success')
            return redirect(url_for('post', post_id = post.id))
    return render_template('Feedback.html', title='Feedback',form=form,post=post)


@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('403.html'), 403


@app.errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500

