from __future__ import annotations
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship

from referral_module.models.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    referr_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Codes(Base):
    __tablename__ = "codes"

    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True)
    expired_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    def to_json(self):
        data = {'id': self.id,
                'code': self.code,
                'expired_date': str(self.expired_date),
                'user_id': self.user_id}
        return data
