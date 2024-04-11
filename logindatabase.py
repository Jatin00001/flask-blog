import sqlalchemy
from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://root:fXIllItNLMVVSzRwHPFWGzJfZGNlxykr@monorail.proxy.rlwy.net:51990/railway"
# connect_args = {'ssl': {'cert': '/path/to/certificate.pem'}}
engine = create_engine(db_connection_string)

# def loadformdb():
#   try:
#     with engine.connect() as conn:
#       # print("Connected to the database -- >", conn)
#       result = conn.execute(text("SELECT * FROM userdatalogin"))
#       result_dicts = []
#       for row in result.all():
#         result_dicts.append(row._asdict())   #convert data into dictionary
#       print(type(result_dicts))
#   except Exception as e:
#     print(e) 
