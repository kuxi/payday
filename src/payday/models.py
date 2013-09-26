from datetime import date
import json


from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import types
from sqlalchemy import Column

Base = declarative_base()
engine = create_engine("sqlite://")
Session = sessionmaker(bind=engine)


class WorkHours(Base):
    __tablename__ = 'work_hours'

    date = Column(types.Date, primary_key=True)
    hours = Column(types.Integer, nullable=False)
    description = Column(types.Text, nullable=False)

    @classmethod
    def all(cls):
        session = Session()
        return session.query(WorkHours).all()

    @classmethod
    def get(cls, date):
        session = Session()
        return session.query(WorkHours).filter(WorkHours.date == date).first()

    def save(self):
        session = Session()
        session.add(self)
        session.commit()

Base.metadata.create_all(bind=engine)


class ModelEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Base):
            encoded = {}
            for key in o._sa_instance_state.attrs.keys():
                encoded[key] = getattr(o, key)
            return encoded
        if isinstance(o, date):
            return {
                'year': o.year,
                'month': o.month,
                'day': o.day,
            }

        return super(ModelEncoder, self).default(o)
json._default_encoder = ModelEncoder()
