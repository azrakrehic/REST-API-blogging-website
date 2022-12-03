from blog import db, ma
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from marshmallow import Schema,fields


def dict_helper(objectlist):
    result = [item.obj_to_dict() for item in objectlist]
    return result

post_tags = db.Table('post_tags',
                    db.Column('blog_post_slug', db.Integer, db.ForeignKey('blog_post.slug')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                    )

class Tag(db.Model):
    id= db.Column(db.Integer(), primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    def obj_to_dict(self): 
        return self.name

class BlogPost(db.Model):
    slug = db.Column(db.String(), unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String(), unique=True, nullable=False)
    body = db.Column(db.String(), unique=True, nullable=False)
    tags = db.relationship('Tag', secondary='post_tags', backref='posts')
    created_at = db.Column(DateTime, default=datetime.now)
    updated_at = db.Column(DateTime, default=datetime.now, onupdate=datetime.now)
    comments = db.relationship('Comment', backref='blogs_comments', lazy=True)
    
    def obj_to_dict(self): 
        return {
            "slug": self.slug,
            "title" : self.title,
            "description": self.description,
            "body": self.body,
            "tagList": dict_helper(self.tags),
            "created_at" : self.created_at,
            "updated_at": self.updated_at,
        }
    

class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(DateTime, default=datetime.now)
    updated_at = db.Column(DateTime, default=datetime.now, onupdate=datetime.now)
    blog = db.Column(db.String(), db.ForeignKey('blog_post.slug'))
    body = db.Column(db.String(), unique=True, nullable=False)

    def obj_to_dict(self): 
        return {
            "id": self.id,
            "created_at" : self.created_at,
            "updated_at": self.updated_at,
            "body": self.body
        }



        
