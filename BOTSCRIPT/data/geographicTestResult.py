import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class GeographicTest(SqlAlchemyBase):
    __tablename__ = 'geographicTestResult'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    userId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    userResult = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)