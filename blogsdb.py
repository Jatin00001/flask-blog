from flask import jsonify
import sqlalchemy
from sqlalchemy import create_engine, text
import os

my_secret = os.environ['DB_CONNECTION_STRING']

db_connection_string = my_secret
engine = create_engine(db_connection_string)


def fetchblogs(blog_id):
  try:
    with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM blogs WHERE blog_id = :val"), {"val": blog_id})
      row = result.first()
      if row:  # len(rows) gives a len of row
        return row._asdict()  # Convert row to dictionary using ._asdict()
      else:
        return None
  except Exception as e:
    print("An error occurred:", e)
    return None



def fetchallblogs():
  try:
    with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM blogs"))
      blogs = []
      for row in result.all():
        blogs.append(row._asdict())  #convert data into dictionary
      return blogs
  except Exception as e:
    print("An error occurred:", e)
    return None


def update_blog(blog_id, title, content):
  try:
      with engine.begin() as conn:  # Start a transaction
          update_query = text(
              "UPDATE blogs SET title = :title, content = :content WHERE blog_id = :blog_id"
          )
          # Validate input
          if not isinstance(blog_id, int) or not isinstance(title, str) or not isinstance(content, str):
              raise ValueError("Invalid input parameters")

          # Execute the update query
          conn.execute(update_query, {"title": title, "content": content, "blog_id": blog_id})

      return True  # Return True if update is successful

  except Exception as e:
      # Handle exceptions
      print(f"Error updating blog: {e}")
      return False
