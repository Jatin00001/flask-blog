# main.py

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt
from logindatabase import loadformdbskills, load_form_blogs_db, load_form_db_skills, load_form_blogs_db_fm_id
from login import login_check, register_new_user

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key'  # Change this to a random secret key


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
  if 'email' in session:
    current_user = session['email']
    return render_template('dashboard.html', email=current_user)
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    if login_check(email, password):
      session['email'] = email
      return redirect(url_for('dashboard'))
    else:
      return render_template('login.html', message='Invalid email or password')
  return render_template('login.html')


@app.route('/dashboard')
def dashboard():
  if 'email' in session:
    current_user = session['email']
    return render_template('dashboard.html', email=current_user)
  return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
  if 'email' in session:
    current_user = session['email']
    return render_template('dashboard.html', email=current_user)

  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    if register_new_user(username, password, email):
      return redirect(url_for('login'))
    else:
      return render_template(
          'register.html',
          message=
          'Registration failed. Please try again or,already have an acount')

  return render_template('register.html')


# Route for logout
@app.route('/logout')
def logout():
  if 'email' in session:
    session.pop('email', None)
    return render_template('login.html')
  return redirect(url_for('login'))


@app.route('/admin/users')
def admin_users():
  admin_email = "admin@gmail.com"
  if 'email' in session and session['email'] == admin_email:
    users = loadformdbskills()
    return render_template('/users/admin_users.html', users=users, admin=True)
  return redirect(url_for('login'))


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
