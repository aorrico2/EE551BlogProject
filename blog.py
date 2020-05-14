# Anthony Orrico
# EE-551 Blog Project

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

# Need flask sqlalchemy as database
from flask_sqlalchemy import SQLAlchemy

blog = Flask(__name__)

blog.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/aorri/OneDrive/Desktop/FlaskProject/blog.db'
db = SQLAlchemy(blog)

# Need to create table to hold blog posts information
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))    # 40 Characters
    header = db.Column(db.String(60))   # 60 Characters
    poster = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    post = db.Column(db.Text)           # Text for longer strings of text
    #comments = db.relationship('Comments', backref='Post', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(150))
    commenter = db.Column(db.String(20))
    post_id = db.Column(db.Integer)

# Need routes for each of the templates used
# index, about, contact, post

@blog.route('/')
def home():
    # Want to display the most recent posts on the home page
    posts = Posts.query.order_by(Posts.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@blog.route('/about')
def about():
    return render_template('about.html')

@blog.route('/post/<int:post_id>')
def post(post_id):
    post = Posts.query.filter_by(id=post_id).one()
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.id.desc()).all()
    date_posted = post.date_posted.strftime('%B %d, %Y')
    
    return render_template('post.html', post=post,date_posted=date_posted,comments=comments)

@blog.route('/newPosts')
def newPosts():
    return render_template('newPosts.html')

@blog.route('/sendPost', methods=['POST'])
def sendPost():
    title = request.form['title']
    header = request.form['header']
    author = request.form['poster']
    post = request.form['post']

    # Now want to add to the database
    post = Posts(title=title, header=header, poster=author, date_posted=datetime.now(), post=post)

    db.session.add(post)
    db.session.commit()
    
    return redirect(url_for('home'))

@blog.route('/sendComment/<int:post_id>', methods=['POST'])
def sendComment(post_id):
    comment = request.form['comment']
    author = request.form['commenter']

    # Now want to add to the database
    newCom = Comment(comment=comment, commenter=author, post_id=post_id)

    db.session.add(newCom)
    db.session.commit()
    
    return redirect(url_for('post', post_id=post_id))


if __name__ == '__main__':
    blog.run(debug=True)
