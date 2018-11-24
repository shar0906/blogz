import logging
from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.String(500))
    published = db.Column(db.Boolean)

    def __init__(self, title, entry):
        self.title = title
        self.entry = entry
        self.published = True


@app.route("/")
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def home():
    published_blogs = Blog.query.filter_by(published=True).all()
    return render_template('blogs.html',title="Blogs!", published_blogs=published_blogs)

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


@app.route('/entries', methods=['GET'])

def entries():
    id = int(request.args.get('id'))
    post = Blog.query.get(id)
    return render_template('entries.html', post=post)

if __name__ == '__main__':
    app.run(port=9999)