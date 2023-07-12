from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('sqlite:///Users/pavlo/Documents/Python/flask-homework/Flask_Homerowk_35/database.db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    purchases = db.relationship('Purchase', backref='user', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
        user_list.append(user_data)
    return jsonify(user_list)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
        return jsonify(user_data)
    else:
        return 'User not found', 404

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author
        }
        book_list.append(book_data)
    return jsonify(book_list)

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author
        }
        return jsonify(book_data)
    else:
        return 'Book not found', 404

@app.route('/purchases', methods=['GET'])
def get_purchases():
    purchases = Purchase.query.all()
    purchase_list = []
    for purchase in purchases:
        purchase_data = {
            'id': purchase.id,
            'user_id': purchase.user_id,
            'book_id': purchase.book_id,
            'quantity': purchase.quantity,
            'user_name': purchase.user.name,
            'book_title': purchase.book.title
        }
        purchase_list.append(purchase_data)
    return jsonify(purchase_list)

@app.route('/purchases/<int:purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    purchase = Purchase.query.get(purchase_id)
    if purchase:
        purchase_data = {
            'id': purchase.id,
            'user_id': purchase.user_id,
            'book_id': purchase.book_id,
            'quantity': purchase.quantity,
            'user_name': purchase.user.name,
            'book_title': purchase.book.title
        }
        return jsonify(purchase_data)
    else:
        return 'Purchase not found', 404

@app.route('/users', methods=['POST'])
def create_user():
    name = request.form.get('name')
    email = request.form.get('email')
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return 'User created', 201

@app.route('/books', methods=['POST'])
def create_book():
    title = request.form.get('title')
    author = request.form.get('author')
    book = Book(title=title, author=author)
    db.session.add(book)
    db.session.commit()
    return 'Book created', 201

@app.route('/purchases', methods=['POST'])
def create_purchase():
    user_id = request.form.get('user_id')
    book_id = request.form.get('book_id')
    quantity = request.form.get('quantity')
    user = User.query.get(user_id)
    book = Book.query.get(book_id)
    if user and book:
        purchase = Purchase(user_id=user.id, book_id=book.id, quantity=quantity)
        db.session.add(purchase)
        db.session.commit()
        return 'Purchase created', 201
    else:
        return 'User or book not found', 404

if __name__ == '__main__':
    app.run(host=os.environ.get('HOST', 'http://127.0.0.1'), port=os.environ.get('PORT', 5000))