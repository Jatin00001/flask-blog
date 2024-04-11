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


# ------blogs--
def load_form_blogs_db():
  try:
    with engine.connect() as conn:
      # print("Connected to the database -- >", conn)
      result = conn.execute(text("SELECT * FROM blogs"))
      blogs = []
      for row in result.all():
        blogs.append(row._asdict())  #convert data into dictionary
      # print(skills)
      return blogs
      # print(type(jobs))
  except Exception as e:
    print(e)
