from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import math
import os

with open('config.json','r') as c:
    params = json.load(c)["params"]
localServer = True

app = Flask(__name__)
app.secret_key = 'super-key'
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['mail_username'],
    MAIL_PASSWORD = params['mail_password']
)
mail = Mail(app)

localServer = True

if localServer == True:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class Contacts(db.Model):
    # sno,name,email,phone_num,msg,date
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12))

class Posts(db.Model):
    # sno,title,subtitle,content,date,slug,img_file
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    subtitle = db.Column(db.String(100),nullable=True)
    content = db.Column(db.String(10000),nullable=False)
    date = db.Column(db.String(12))
    slug = db.Column(db.String(50))
    img_file = db.Column(db.String(12),nullable=True)

@app.route('/')
def home():
    #pagination logic
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts)/int(params['no_of_posts']))

    #[0:params['no_of_posts']]

    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['no_of_posts']) : (page-1)*int(params['no_of_posts']) + int(params['no_of_posts'])]
    if(page == 1):
        prev = "#"
        next = "/?page="+str(page+1)
    elif(page == last):
        next = "#"
        prev = "/?page=" + str(page - 1)
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)


    return render_template('index.html',params=params,posts = posts,prev=prev,next=next)

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

@app.route('/delete/<string:sno>',methods=['GET','POST'])
def delete(sno):
    if ('user' in session and session['user'] == params['admin_username']):
        post = Posts.query.filter_by(sno = sno).first()
        db.session.delete(post)
        db.session.commit()
        return redirect('/dashboard')


@app.route('/edit/<string:sno>',methods = ['GET','POST'])
def editPost(sno):
    if ('user' in session and session['user'] == params['admin_username']):
        if request.method == 'POST':
            title = request.form.get('title')
            tline = request.form.get('tline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')

            if sno == '0':
                post = Posts(title = title,subtitle = tline,content = content,slug = slug,date = datetime.now(),img_file = img_file)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno = sno).first()
                post.title = title
                post.slug = slug
                post.content = content
                post.tagline = tline
                post.img_file = img_file
                post.date = datetime.now()
                db.session.commit()
                return redirect('/edit/'+sno)
        post = Posts.query.filter_by(sno = sno).first()
        return render_template('edit.html',params=params,post = post,sno=sno)


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():

    if ('user' in session and session['user'] == params['admin_username']):
        posts = Posts.query.all()
        return render_template('dashboard.html',params=params,posts = posts)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if (username == params['admin_username'] and password == params['admin_password']):
            #set the session variable
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html',params=params,posts = posts)

    return render_template('AdminSignin.html',params=params)

@app.route('/post/<string:post_slug>', methods = ['GET'])
def post(post_slug):
    post = Posts.query.filter_by(slug = post_slug).first()
    return render_template('post.html', params=params, post=post)

@app.route('/about')
def about():
    return render_template('about.html',params=params)

@app.route('/uploader',methods=['GET','POST'])
def uploader():
    if ('user' in session and session['user'] == params['admin_username']):
        if(request.method == 'POST'):
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "Uploaded Successfully"


@app.route('/contact', methods=['GET','POST'])
def contact():
    if(request.method == 'POST'):
        # add entry to the database
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contacts(name = name, email = email, date=datetime.now(), phone_num = phone, msg = message)
        db.session.add(entry)
        db.session.commit()

        #sending email
        mail.send_message('New message in your Blog from '+ name,
                          sender=email,
                          recipients = [params['mail_username']],
                          body = message + "\n" + phone
                         )

    return render_template('contact.html',params=params)

app.run(debug=True)

