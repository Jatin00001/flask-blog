# main.py

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt
from logindatabase import loadformdbskills, load_form_db_skills
from login import login_check, register_new_user, admin_email, get_auth_id
from blogsdb import fetchblogs, fetchallblogs, update_blog, total_blogs, add_blog, delete_blog
from users_methods import get_users_count, user_by_query, delete_user

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'sdsdsdasdsdsdscsasxsxsaxwhbdbwejbdijwendiwuhiiiuduiweduiweduihweduihweudhweuidhweuidhwe'  # Change this to a random secret key


@app.route('/')
def index():
  skill = loadformdbskills()
  blogs = fetchallblogs()
  if 'email' in session:
    current_user = session['email']
    return render_template('landingpage.html',
                           skills=skill,
                           blogs=blogs,
                           login=current_user)
  return render_template('landingpage.html',
                         skills=skill,
                         blogs=blogs,
                         login=None)


@app.route('/blogs/<id>')
def get_blog(id):
  if 'email' in session:
    blog = fetchblogs(id)
    login = session['email']
    return render_template('blogs.html', blog=blog, login=login)
  blog = fetchblogs(id)
  if blog is not None:
    # keys_list = list(blog.keys())
    return render_template(
        'blogs.html',
        blog=blog,
        login=None,
    )
  else:
    return jsonify({"error": "Blog not found"}), 404


@app.route('/all_blogs')
def get_all_blogs():
  if 'email' in session:
    blogs = fetchallblogs()
    login = session['email']
    return render_template('all_blogs.html', blogs=blogs, login=login)
  blogs = fetchallblogs()
  return render_template('all_blogs.html', blogs=blogs, login=None)


@app.route('/dashboard')
def dashboard():
  if 'email' in session and session['email'] == admin_email():
    current_user = session['email']
    return render_template('dashboard.html',
                           admin=admin_email(),
                           email=current_user)

  elif 'email' in session:
    current_user = session['email']
    return render_template('/normal_users/user_dashboard.html',
                           email=current_user)
  return render_template('login.html')


@app.route('/dashboard/admin/users')
def admin_users():
  if 'email' in session and session['email'] == admin_email():
    users = get_users_count()
    users_data = user_by_query()
    total_blog = total_blogs()
    return render_template('/users/admin_users.html',
                           users=users,
                           users_data=users_data,
                           total_blogs=total_blog,
                           admin=True)
  return redirect(url_for('login'))


@app.route('/dashboard/admin/users/delete/<int:id>', methods=['GET', 'POST'])
def delete_user_admin(id):
  # Check if user is logged in as admin
  if 'email' in session and session['email'] == admin_email():
    # if request.method == 'POST':
    # Perform deletion action
    # delete_user_admin_data = delete_user(id)
    if delete_user(id):
      # User deleted successfully, redirect to admin users page
      return redirect(url_for('admin_users'))
    else:
      # User not found, return error response
      return jsonify({"error": "User not found"}), 404
  # else:
  #   # GET request, show confirmation page
  #   # return render_template('delete_confirmation.html', user_id=id)
  #   return jsonify({"error": "User not found"}), 404
  else:
    # User is not logged in as admin, redirect to login page
    return redirect(url_for('login'))


@app.route('/dashboard/admin/allpost')
def get_all_post():
  if 'email' in session and session['email'] == admin_email():
    # user = session['email']
    admin = admin_email()
    email = session['email']
    blogs = fetchallblogs()
    return render_template('all_post.html',
                           blogs=blogs,
                           admin=admin,
                           email=email)
  return redirect(url_for('login'))


@app.route('/dashboard/admin/allpost/add_post', methods=['GET', 'POST'])
def add_post():
  if 'email' in session and session['email'] == admin_email():
    if request.method == 'POST':
      title = request.form['title']
      slug = request.form['slug']
      subhead = request.form['content']
      content = request.form['content']
      currentuser = session['email']
      get_auth = get_auth_id(currentuser)
      if add_blog(title, slug, content, subhead, get_auth):
        print(f"Blog added successfully: {title}")
        return redirect(url_for('get_all_post'))
      # if add_blog(title, content, slug):
      #   print("Blog added successfully")
      #   return redirect(url_for('get_all_post'))
      return redirect(url_for('get_all_post'))

    return render_template('/users/add_post.html')

  return redirect(url_for('login'))


@app.route('/dashboard/admin/allpost/user/edit/<id>', methods=['GET', 'POST'])
def edit_user(id):
  if 'email' in session and session['email'] == admin_email():

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
        # print("IN fetch by id block")
        return render_template('/users/edit_user.html',
                               blog=blog,
                               admin=True,
                               email=admin_email(),
                               form_action=url_for('edit_user', id=id))

  return jsonify({"Error": "Page not found"})


@app.route('/dashboard/admin/allpost/delete/<int:id>', methods=['GET', 'POST'])
def delete_blog_route(id):
  if 'email' in session and session['email'] == admin_email():
    if request.method == 'POST':
      # Perform deletion action
      if delete_blog(id):
        # Blog deleted successfully, redirect to admin all posts page
        return redirect(url_for('get_all_post'))
      else:
        # Blog not found, return error response
        return jsonify({"error": "Blog not found"}), 404
    else:
      # Display confirmation page for deleting blog with ID
      return f"Are you sure you want to delete blog with ID {id}? <form action='/dashboard/admin/allpost/delete/{id}' method='post'><input type='submit' value='Delete'></form>"
  else:
    # Unauthorized access, redirect to login page
    return redirect(url_for('login'))


# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
  if 'email' in session and session['email'] == admin_email():
    return redirect(url_for('dashboard'))

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
