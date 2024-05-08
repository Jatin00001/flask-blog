import sqlalchemy
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables from .env file

if os.path.exists('.env'):
  load_dotenv()
  my_secret = os.getenv("DB_CONNECTION_STRING")
  print("Found  file")
else:
  print("No .env file found")
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
