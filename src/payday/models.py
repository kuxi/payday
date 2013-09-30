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


class WorkLog(Base):
    __tablename__ = 'work_hours'

    id = Column(types.Integer, primary_key=True)
    date = Column(types.Date, nullable=False)
    hours = Column(types.Integer, nullable=False)
    description = Column(types.Text, nullable=False)

    @classmethod
    def all(cls):
        session = Session()
        logs = session.query(WorkLog).all()
        session.close()
        return logs

    @classmethod
    def get_for_date(cls, date):
        session = Session()
        logs = session.query(WorkLog).\
            filter(WorkLog.date == date).all()
        session.close()
        return logs

    @classmethod
    def get(cls, id):
        session = Session()
        log = session.query(WorkLog).get(id)
        session.close()
        return log

    def save(self):
        session = Session()
        session.add(self)
        session.commit()
        session.close()

    def delete(self):
        session = Session()
        session.delete(self)
        session.commit()
        session.close()

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
