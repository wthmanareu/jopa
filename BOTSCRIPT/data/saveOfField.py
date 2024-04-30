import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class SavedField(SqlAlchemyBase):
    __tablename__ = 'savesOfFields'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    userId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    userField = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    enemyFieldUser = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    userShipCount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    enemyField = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    enemyShipCount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    enemyHodi = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    enemyLst = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    enemyDrctx = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    enemyDrctx2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    drctForShot = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    whoIsTurn = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)