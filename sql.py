from sqlalchemy import text, create_engine

engine = create_engine('[conn str]')
with engine.connect() as connection:
    result = connection.execute(text("select * from test"))
    for row in result:
        print(row)