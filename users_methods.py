# connect_args = {'ssl': {'cert': '/path/to/certificate.pem'}}
from sqlalchemy import create_engine, text

import os

my_secret = os.environ['DB_CONNECTION_STRING']
db_connection_string = my_secret
engine = create_engine(db_connection_string)


def get_users():
  try:
    with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM users"))
      # print(result)
      users = []
      for row in result.all():
        users.append(row._asdict())  # Convert row to dictionary
      return users
  except Exception as e:
    print(e)
    return None, 500


def user_by_query():
  try:
    with engine.connect() as conn:
      result = conn.execute(text("SELECT username, email, role FROM users"))
      users = []
      for row in result.all():
        users.append(row._asdict())  # Convert row to dictionary
      return users
  except Exception as e:
    print("Error fetching users:", e)
    return None, 500


def get_users_count():
  try:
    with engine.connect() as conn:
      result = conn.execute(text("SELECT COUNT(*) FROM users"))
      count = result.fetchone()[0]
      return count, 200
  except Exception as e:
    print(e)
    return None, 500


def delete_user(id):
  try:
    with engine.connect() as conn:
      # Delete user from the database
      delete_query = text("DELETE FROM users WHERE id = :id")
      conn.execute(delete_query, {"id": id})
      conn.commit()
      return True, 200
  except Exception as e:
    print("Error deleting user:", e)
    return None, 500
