# main.py

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt
from logindatabase import loadformdbskills, load_form_db_skills
from login import login_check, register_new_user
from blogsdb import fetchblogs, fetchallblogs, update_blog
import os

my_secret_admin = os.environ['admin_email']

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key'  # Change this to a random secret key


@app.route('/')
def index():
  skill = loadformdbskills()
  blogs = fetchallblogs()
  return render_template('landingpage.html', skills=skill, blogs=blogs)


@app.route('/blogs/<id>')
def get_blog(id):
  blog = fetchblogs(id)
  if blog is not None:
    # keys_list = list(blog.keys())
    return render_template('blogs.html', blog=blog)
  else:
    return jsonify({"error": "Blog not found"}), 404


@app.route('/all_blogs')
def get_all_blogs():
  blogs = fetchallblogs()
  return render_template('all_blogs.html', blogs=blogs)


@app.route('/dashboard')
def dashboard():
  if 'email' in session:
    current_user = session['email']
    return render_template('dashboard.html', email=current_user)
  return render_template('login.html')


@app.route('/dashboard/admin/users')
def admin_users():
  if 'email' in session and session['email'] == my_secret_admin:
    users = loadformdbskills()
    return render_template('/users/admin_users.html', users=users, admin=True)
  return redirect(url_for('login'))


@app.route('/dashboard/admin/allpost')
def get_all_post():
  if 'email' in session:
    # user = session['email']
    blogs = fetchallblogs()
    return render_template('all_post.html', blogs=blogs, admin=True)
  return redirect(url_for('login'))


@app.route('/dashboard/admin/allpost/user/edit/<id>' , methods=['GET', 'POST'])
def edit_user(id):
  if 'email' in session and session['email'] == my_secret_admin:

    if request.method == 'POST':
      
      title = request.form.get('title')
      content = request.form.get('content')
      slug = request.form.get('slug')

      if update_blog(id, title, content, slug):
        print("Updated blog successfully")
        return redirect(url_for('get_blog', id=id))
      else:
        return jsonify({"error": "Failed to update blog"}), 500

    else:
      blog = fetchblogs(id)
      if blog is not None:
        print("IN fetch by id block")
        return render_template(
            '/users/edit_user.html',
            blog=blog,
            admin=True,
            email=my_secret_admin,
        form_action=url_for('edit_user', id=id))

  return redirect(url_for('login'))


# @app.route("/dashboard/admin/allpost/user/edit/<id>", methods=['GET', 'POST'])
# def update_blog_route(id):
#   if 'email' in session and session['email'] == my_secret_admin:
#     if request.method == 'POST':
#       blog_id = id
#       title = request.form.get('title')
#       content = request.form.get('content')
#       slug = request.form.get('slug')

#       if update_blog(blog_id, title, content, slug):
#         return redirect(url_for('get_blog', id=id))
#       else:
#         return jsonify({"error": "Failed to update blog"}), 500

#   return redirect(url_for('login'))


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


# -------AFTER THIS SECTION ALL API WITH RAW DATA ------------------------------------------------------------------------
@app.route('/api/skills')
def skills():
  skills = loadformdbskills()
  print(type(skills))
  return jsonify({"skills": skills})


@app.route('/api/get_skill/<id>')
def get_skill(id):
  skill = load_form_db_skills(id)
  if skill is not None:
    return jsonify({"skill": skill})
  else:
    return jsonify({"error": "Skill not found"}), 404


@app.route('/api/blogs/<id>')
def get_blog_api(id):
  blog = fetchblogs(id)
  if blog is not None:
    return jsonify({"blog": blog})
  else:
    return jsonify({"error": "Blog not found"}), 404


if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")
