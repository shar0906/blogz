#!/usr/bin/env python3

import logging
from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

userdata = {}

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.String(500))
    published = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, entry, user):
        self.title = title
        self.entry = entry
        self.published = True
        self.user = user

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(35))
    blogs = db.relationship('Blog', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route("/")
def index():
    return redirect('/blog')

@app.route('/entries', methods=['GET'])
def entries():
    id = int(request.args.get('id'))
    post = Blog.query.get(id)
    return render_template('entries.html', post=post)

@app.route('/blog', methods=['POST', 'GET'])
def home():
    published_blogs = Blog.query.filter_by(published=True).all()
    return render_template('blogs.html',title="Blogs!", published_blogs=published_blogs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global userdata
    message = "Your username and/or password was incorrect. Please try again."
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == request.form['password']:
                userdata[username] = {True}
                breakpoint()
                return redirect('/newpost')
        return redirect(url_for('login', message=message)) 

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    message = "Please enter some text."
    if request.method == 'GET':
        return render_template('newpost.html')

    if request.method == 'POST':
        if not request.form['blogtitle'] or not request.form['blogbody']:
            return redirect(url_for('newpost', message=message))
        else:
            blog_title = request.form['blogtitle']
            blog_entry = request.form['blogbody']
            new_blog = Blog(blog_title, blog_entry)
            db.session.add(new_blog)
            db.session.commit()
            last = Blog.query.all()[-1]
        return redirect(f'/entries?id={last.id}')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        
        counter = 0
        messages = {}

        if validate(request.form['username']) == False:
            counter += 1
            messages['message1'] = "Your username is invalid!"

        if validate(request.form['password']) == False:
            counter += 1
            messages['message2'] = "Your password is invalid!"
        
        verify = request.form['verify']
        if verify != request.form['password']:
            counter += 1
            messages['message3'] = "Your passwords must match!"

        if counter == 0:
            # = request.form['username, password']
            user = User()
            return redirect('newpost.html')
        else:
            return redirect(url_for('index', **messages, **request.form))

def validate(value):
    if value:
        if ' ' in value:
            return False
        if 3 > len(value) or len(value) > 20: 
            return False
    else:
        return False

if __name__ == '__main__':
    db.create_all()
    app.run(port=9999)
