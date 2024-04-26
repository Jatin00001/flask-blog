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
      result = conn.execute(text("SELECT * FROM blogs WHERE blog_id = :val"),
                            {"val": blog_id})
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


def update_blog(blog_id, title, content, slug):
  try:
    with engine.begin() as conn:  # Start a transaction
      update_query = text(
          "UPDATE blogs SET title = :title, content = :content, slug = :slug WHERE blog_id = :blog_id"
      )
      # # Validate input
      # if not (isinstance(blog_id, int) and isinstance(title, str) and isinstance(content, str) and isinstance(slug, str)):
      #   raise ValueError("Invalid input parameters")

      # Execute the update query
      conn.execute(update_query, {
          "blog_id": blog_id,
          "title": title,
          "content": content,
          "slug": slug
      })

    return True  # Return True if update is successful

  except Exception as e:
    # Handle exceptions
    print(f"Error updating blog: {e}")
    return False


def total_blogs():
  try:
    with engine.connect() as conn:
      result = conn.execute(text("SELECT COUNT(*) FROM blogs"))
      count = result.fetchone()[0]
      return count, 200
  except Exception as e:
    print(e)
    return None, 500


def add_blog(title, slug, content, subhead, author_id):
  try:
    with engine.connect() as conn:
      query = text(
          "INSERT INTO blogs (title, slug, subhead, content, author_id) VALUES (:title, :slug, :subhead, :content, :author_id)"
      )
      conn.execute(
          query, {
              "title": title,
              "slug": slug,
              "subhead": subhead,
              "content": content,
              "author_id": author_id
          })

      conn.commit()
      return True
  except Exception as e:
    print(e)
    return False


def delete_blog(blog_id):
  try:
    with engine.connect() as conn:
      # Delete user from the database
      delete_query = text("DELETE FROM blogs WHERE blog_id = :id")
      conn.execute(delete_query, {"id": blog_id})
      conn.commit()
      return True
  except Exception as e:
    print("Error deleting user:", e)
    return False
