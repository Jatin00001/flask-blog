import sqlalchemy
from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+pymysql://root:fXIllItNLMVVSzRwHPFWGzJfZGNlxykr@monorail.proxy.rlwy.net:51990/railway"
)

try:
  with engine.connect() as conn:
    print("Connected to the database -- >", conn)
    result = conn.execute(text("SELECT * FROM userdatalogin"))
    # for row in result:
    #   print(row)
    # conn.execute(
    #     text(
    #       "INSERT INTO userdatalogin (username, password) VALUES ('lucky', '123456')"
    #     ))
    # conn.commit()
    for row in result:
      print(row)

except Exception as e:
  print(e)