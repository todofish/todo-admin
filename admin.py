import os
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    os.getenv("DATABASE_URL", "postgresql://postgres:secret@db/postgres").strip(), 
    convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Entry(Base):
    __tablename__ = "entries"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    order = Column(Integer)
    completed = Column(Boolean)

    def __init__(self, title=None, order=None):
        self.title = title
        self.order = order
        self.completed = False

    def __repr__(self):
        return "<Entry: {}>".format(self.title)


app = Flask("Todos")
app.secret_key = "0987654321qwertyuiop"

admin = Admin(app, name='Todos', template_mode='bootstrap3')
admin.add_view(ModelView(Entry, db_session))

app.run(debug=True, threaded=True, host="0.0.0.0")