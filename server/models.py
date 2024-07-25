from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name field is required.")
        author = db.session.query(Author.id).filter_by(name = name).first()
        if author is not None:
            raise ValueError("Name must be unique.")
        return name
    
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and not re.match(r'^\d{10}$', phone_number):
            raise ValueError('Phone number must be exactly 10 digits')
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Post title is required')
        if not re.search(r'Won\'t Believe|Secret|Top|Guess', title):
            raise ValueError('Post title must contain one of the following: "Won\'t Believe", "Secret", "Top", "Guess"')
        return title

    @validates('content')
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError('Post content must be at least 250 characters long')
        return content

    @validates('category')
    def validate_category(self, key, category):
        if category and category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Post category must be either "Fiction" or "Non-Fiction"')
        return category

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError('Post summary must be a maximum of 250 characters')
        return summary

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'