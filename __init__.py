from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'secret_key'

users = {
    1: {'id': 1, 'name': 'John'},
    2: {'id': 2, 'name': 'Jane'}
}

books = {
    1: {'id': 1, 'title': 'Book 1'},
    2: {'id': 2, 'title': 'Book 2'}
}

@app.route('/users')
def show_users():
    if 'username' not in session:
        return redirect('/login')
    return render_template('users.html', users=users.values())

@app.route('/users/<int:user_id>')
def show_user(user_id):
    if 'username' not in session:
        return redirect('/login')
    user = users.get(user_id)
    if not user:
        return 'User not found'
    return render_template('user.html', user=user)

@app.route('/books')
def show_books():
    if 'username' not in session:
        return redirect('/login')
    return render_template('books.html', books=books.values())

@app.route('/books/<int:book_id>')
def show_book(book_id):
    if 'username' not in session:
        return redirect('/login')
    book = books.get(book_id)
    if not book:
        return 'Book not found'
    return render_template('book.html', book=book)

@app.route('/params')
def show_params():
    if 'username' not in session:
        return redirect('/login')
    return render_template('params.html', params=request.args)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/')
def home():
    if 'username' in session:
        return f'Hello, {session["username"]}'
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run()