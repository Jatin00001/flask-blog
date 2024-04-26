# connect_args = {'ssl': {'cert': '/path/to/certificate.pem'}}
from sqlalchemy import create_engine, text
import bcrypt
import os

my_secret = os.environ['DB_CONNECTION_STRING']
db_connection_string = my_secret
engine = create_engine(db_connection_string)


class User:

  def __init__(self, username, password, email):
    self.username = username
    self.password_hash = self._hash_password(password)
    self.email = email

  def _hash_password(self, password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash

  def verify_password(self, password):
    # Verify if the provided password matches the stored hash
    return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)


# ----------------------------------------------------------/


def register_new_user(username, password, email):
  # Create a new User instance
  new_user = User(username, password, email)
  try:
    with engine.connect() as conn:
      # Check if email already exists
      email_check_query = text(
          "SELECT COUNT(*) FROM users WHERE email = :email")
      email_count = conn.execute(email_check_query, {
          "email": email
      }).fetchone()[0]

      if email_count > 0:
        print("Error: Email already registered. Try logging in.")
        return False

      # Hash the password
      hashed_password = new_user.password_hash

      # Insert user into the database
      insert_query = text(
          "INSERT INTO users (username, password, email) VALUES (:username, :password, :email)"
      )
      user_data = {
          "username": new_user.username,
          "password": hashed_password,
          "email": new_user.email
      }
      conn.execute(insert_query, user_data)
      conn.commit()

      print(
          "User registered successfully and data inserted into MySQL Workbench!"
      )
      return True
  except Exception as e:
    print("Error registering user:", e)


# -----------------------------------
def login_check(email, password):
  try:
    with engine.connect() as conn:
      # Fetch user data from the database
      select_query = text(
          "SELECT email, password,username FROM users WHERE email = :email")
      result = conn.execute(select_query, {"email": email}).fetchone()

      if result:
        stored_email, stored_password_hash, stored_username = result
        # Verify the password
        if bcrypt.checkpw(password.encode('utf-8'),
                          stored_password_hash.encode('utf-8')):
          print("Login successful!")
          return True
        else:
          print("Invalid password. Please try again.")
          return False
      else:
        return False
        # print("User not found register please.")
  except Exception as e:
    print("Error logging in:", e)


def admin_email():
  try:
    with engine.connect() as conn:
      # Assuming you have a 'users' table with columns 'email' and 'role'
      admin = "admin"
      result = conn.execute(
          text("SELECT email FROM users WHERE role = :admin"),
          {"admin": admin})
      admin_email = result.fetchone()[0]
      return admin_email
  except Exception as e:
    print("Error fetching admin email:", e)
    return None


def get_auth_id(email):
  try:
    with engine.connect() as conn:
      # Assuming you have a 'users' table with columns 'email' and 'role'
      result = conn.execute(
          text("SELECT user_id FROM users WHERE email = :email"),
          {"email": email})
      auth_id = result.fetchone()[0]
      return auth_id
  except Exception as e:
    print("Error fetching email:", e)
    return None
