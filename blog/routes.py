from blog import app, db
from slugify import slugify
from blog.models import BlogPost, Comment, Tag
from flask import request, jsonify, Blueprint
import json

REQUEST_API = Blueprint('routes', __name__)


def get_blueprint():
    return REQUEST_API

def dict_helper(objectlist):
    result = [item.obj_to_dict() for item in objectlist]
    return result

#Get Blog Post!
@app.route('/api/posts/<slug>', methods=["GET"])
def get_blog(slug):
    blog = BlogPost.query.get(slug)
    return {"blogPost" : blog.obj_to_dict()}


#List Blog Posts
@app.route('/api/posts', methods=["GET"])
def get_blog_posts():
    posts = BlogPost.query.order_by(BlogPost.updated_at.desc())
    try:
        tag =  request.args.get('tag')
        if tag:
            posts = BlogPost.query.filter(BlogPost.tags.any(name=tag))
    finally:
        postcount = posts.count()
        return {"blogPosts" :dict_helper(posts),
                "postsCount" : postcount}

#Create Blog Post
@app.route('/api/posts', methods=["POST"])
def add_blog_post():
    title=request.json['blogPost']['title']
    description=request.json['blogPost']['description']
    body=request.json['blogPost']['body']
    slug=slugify(title)
    new_blog_post= BlogPost(slug=slug, title=title, description=description, body=body)
    try:
        tags = request.json['blogPost']['tagList']
        for tag in tags:
            blogtag = Tag.query.filter_by(name=tag).first()
            if not blogtag:
                blogtag=Tag(name=tag)
                db.session.add(blogtag)
            new_blog_post.tags.append(blogtag)
            db.session.commit()
    except KeyError:
        pass
    db.session.add(new_blog_post)
    db.session.commit()
    return {"blogPost": new_blog_post.obj_to_dict()}

#Update Blog Post
@app.route('/api/posts/<slug>', methods=["PUT"])
def update_blog(slug):
    blog=BlogPost.query.get(slug)
    title=blog.title
    slug=blog.slug
    description=blog.description
    body=blog.body
    try:
        title=request.json['title']
        blog.title=title
        blog.slug=slugify(title)
    except KeyError:
        pass
    try:
        blog.description=request.json['description']
    except KeyError:
        pass
    try:
        blog.body=request.json['body']
    except KeyError:
        pass
    db.session.commit()
    return {"blogPost": blog.obj_to_dict()}

#Delete Blog Post
@app.route('/api/posts/<slug>', methods=["DELETE"])
def delete_blog(slug):
    blog = BlogPost.query.get(slug)
    db.session.delete(blog)
    db.session.commit()
    return {"blogPost": blog.obj_to_dict()}

#Get Tags
@app.route('/api/tags')
def get_tags():
    tags = Tag.query.all()
    return {"tags" : dict_helper(tags)}

#Add Comments to a blog post
@app.route('/api/posts/<slug>/comments', methods=["POST"])
def add_comment(slug):
    body = request.json['comment']['body']
    comment = Comment(body=body, blog=slug)
    db.session.add(comment)
    db.session.commit()
    comment = Comment.query.filter_by(body=body, blog=slug).first()
    return {"comment" : comment.obj_to_dict()}


#Get Comments from a blog post
@app.route('/api/posts/<slug>/comments', methods=["GET"])
def get_comments(slug):
    comments = Comment.query.filter_by(blog=slug)
    return {"comments" : dict_helper(comments)}
    
#Delete comment
@app.route('/api/posts/<slug>/comments/<id>', methods=["DELETE"])
def delete_comment(slug,id):
    comment = Comment.query.filter_by(id=id, blog=slug).first()
    db.session.delete(comment)
    db.session.commit()
    return {"comment" : comment.obj_to_dict()}

