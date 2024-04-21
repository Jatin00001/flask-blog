import sqlalchemy
from sqlalchemy import create_engine, text
import os

my_secret = os.environ['DB_CONNECTION_STRING']

db_connection_string = my_secret
# connect_args = {'ssl': {'cert': '/path/to/certificate.pem'}}
engine = create_engine(db_connection_string)


def loadformdbskills():
  try:
    with engine.connect() as conn:
      # print("Connected to the database -- >", conn)
      result = conn.execute(text("SELECT * FROM skills"))
      skills = []
      for row in result.all():
        skills.append(row._asdict())  #convert data into dictionary
      # print(skills)
      return skills
      # print(type(jobs))

  except Exception as e:
    print(e)


# def admin_email():
#   try:
#     with engine.connect() as conn:
#       # Assuming you have a 'users' table with columns 'email' and 'role'
#       admin = "admin"
#       result = conn.execute(
#           text("SELECT email FROM users WHERE role = :admin"),
#           {"admin": admin})
#       admin_email = result.fetchone()[0]
#       return admin_email
#   except Exception as e:
#     print("Error fetching admin email:", e)
#     return None


def load_form_db_skills(id):
  try:
    with engine.connect() as conn:
      # print("Connected to the database -- >", conn)
      result = conn.execute(text("SELECT * FROM skills WHERE id = :val"),
                            {"val": id})
      row = result.first()
      if row:  # len(rows) gives a len of row
        return row._asdict()  # Convert row to dictionary using ._asdict()
      else:
        return None
  except Exception as e:
    print("An error occurred:", e)
    return None
