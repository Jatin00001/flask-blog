# main.py

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# # Dummy users for demonstration, replace with your database implementation
# users = {
#     'user1': {
#         'username': 'jatin',
#         'password': bcrypt.generate_password_hash('password1').decode('utf-8')
#     },
#     'user2': {
#         'username': 'jatin2',
#         'password': bcrypt.generate_password_hash('password2').decode('utf-8')
#     }
# }

Skills = [{
    'id': 1,
    'sname': 'Python',
    'sdesc': 9
}, {
    'id': 2,
    'sname': 'C++',
    'sdesc': 9
}, {
    'id': 3,
    'sname': 'Java',
    'sdesc': 9
}]


class User:

  def __init__(self, username, password):
    self.username = username
    self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    # print(self.password)


# Dummy users for demonstration
user1 = User('jatin', 'jatin9920')
user2 = User('jatin2', '123456789')
user3 = User('Admin', 'admin123456')

# Store user objects in a dictionary for easy access
users = {user.username: user for user in [user1, user2, user3]}


@app.route('/')
def index():
  return render_template('landingpage.html', skils=Skills)


# @app.route('/login')
# def login():
#     return render_template('login.html')


# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
  if 'username' in session:
    current_user = session['username']
    return render_template('dashboard.html', username=current_user)
  if request.method == 'POST':
    username = request.form['email']
    password = request.form['password']
    if username in users and bcrypt.check_password_hash(
        users[username].password, password):
      session['username'] = username
      return redirect(url_for('dashboard'))
    else:
      return render_template('login.html',
                             message='Invalid username or password')
  return render_template('login.html')


@app.route('/dashboard')
def dashboard():
  if 'username' in session:
    current_user = session['username']
    return render_template('dashboard.html', username=current_user)
  return render_template('login.html')


# Route for logout
@app.route('/logout')
def logout():
  if 'username' in session:
    session.pop('username', None)
    return render_template('login.html')
  return redirect(url_for('login'))


# @app.route('/register')
# def register():
#     return render_template('register.html')


@app.route('/books')
def books():
  return render_template('/dashboardhtml/dashboardbase.html')


@app.route('/api/skills')
def skills():
  print(type(Skills))
  return jsonify({"skills": Skills})


if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")
