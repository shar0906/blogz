from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:shableharris@localhost:5000/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.String(500))
    published = db.Column(db.Boolean)

    def __init__(self, title):
        self.title = title
        self.entry = entry
        self.published = True


@app.route('/blog', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['blog']
        new_blog = Blog(blog_title)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(published=False).all()
    published_blog = Blog.query.filter_by(published=True).all()
    return render_template('blogs.html',title="Blogs!", 
        blogs=blogs, published_blog=published_blog)


@app.route('/delete-blog', methods=['POST'])
def delete_blog():

    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    blog.published = True
    db.session.add(blog)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()