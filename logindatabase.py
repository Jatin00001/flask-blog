import sqlalchemy
from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://root:fXIllItNLMVVSzRwHPFWGzJfZGNlxykr@monorail.proxy.rlwy.net:51990/railway"
# connect_args = {'ssl': {'cert': '/path/to/certificate.pem'}}
engine = create_engine(db_connection_string)

try:
  with engine.connect() as conn:
    # print("Connected to the database -- >", conn)
    result = conn.execute(text("SELECT username, password FROM userdatalogin"))
    for row in result:
      print(f"username: {row.username}  passoword: {row.password}")



# -------------------------------------------------------------------------------------------------------------------------------why we convert into dict -------------------------------------/
    # for row in result:
    #   print(row)
    # conn.execute(
    #     text(
    #       "INSERT INTO userdatalogin (username, password) VALUES ('lucky', '123456')"
    #     ))
    # conn.commit()
    # for row in result:
    #   print(row)
    # print(result.all()) #  type --->class list
    # print(type(result)) # type ---> class 'sqlalchemy.engine.cursor.CursorResult'

    #now we check whats on first index in row and check its class its 
    # First_postion = result.all[0]
    # print("First pos data class : " , type(First_postion)) #<class 'sqlalchemy.engine.cursor.CursorResult'>'method' object is not subscriptable
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
except Exception as e:
  print(e)
