from flask import Flask
from flask_sqlalchemy import SQLAlchemy

"""
    SQLAlchemy is a Python library that allows us to interact with a database
    using Python code. It is an Object Relational Mapper (ORM), which means that
    it maps Python objects to database tables and vice versa. It also provides
    a SQL Expression Language, which allows us to write SQL queries using Python
    code. SQLAlchemy is compatible with many different database management systems,
    including SQLite, MySQL, and PostgreSQL.
"""

db = SQLAlchemy() # create database instance
DB_NAME = "database.db"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #Todo
