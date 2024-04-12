# main.py

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt
from logindatabase import loadformdbskills, load_form_blogs_db, load_form_db_skills ,load_form_blogs_db_fm_id

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

# Skills = [{
#     'id': 1,
#     'sname': 'Python',
#     'sdesc': 9
# }, {
#     'id': 2,
#     'sname': 'C++',
#     'sdesc': 9
# }, {
#     'id': 3,
#     'sname': 'Java',
#     'sdesc': 9
# }]

# class User:

#   def __init__(self, username, password):
#     self.username = username
#     self.password = bcrypt.generate_password_hash(password).decode('utf-8')
#     # print(self.password)

# # Dummy users for demonstration
# user1 = User('jatin', 'jatin9920')
# user2 = User('jatin2', '123456789')
# user3 = User('Admin', 'admin123456')

# # Store user objects in a dictionary for easy access
# users = {user.username: user for user in [user1, user2, user3]}


@app.route('/')
def index():
  skill = loadformdbskills()
  blogs = load_form_blogs_db()
  return render_template('landingpage.html', skills=skill, blogs=blogs)

@app.route('/blogs/<id>')
def get_blog(id):
  blog = load_form_blogs_db_fm_id(id)
  if blog is not None:
    # keys_list = list(blog.keys())
    return render_template('blogs.html', blog=blog)
  else:
    return jsonify({"error": "Blog not found"}), 404

@app.route('/all_blogs')
def get_all_blogs():
  blogs = load_form_blogs_db()
  return render_template('all_blogs.html', blogs=blogs)

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








# -------AFTER THIS SECTION ALL API WITH RAW DATA ------------------------------------------------------------------------
@app.route('/api/skills')
def skills():
  skills = loadformdbskills()
  print(type(skills))
  return jsonify({"skills": skills})


@app.route('/api/<id>')
def get_skill(id):
  skill = load_form_db_skills(id)
  if skill is not None:
    return jsonify({"skill": skill})
  else:
    return jsonify({"error": "Skill not found"}), 404


@app.route('/api/blogs/<id>')
def get_blog_api(id):
  blog = load_form_blogs_db_fm_id(id)
  if blog is not None:
    return jsonify({"blog": blog})
  else:
    return jsonify({"error": "Blog not found"}), 404
  
  

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")
