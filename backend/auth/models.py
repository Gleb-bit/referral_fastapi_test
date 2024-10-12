from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config import Base


class User(Base):
    """Таблица пользователя"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    first_name = Column(String, nullable=False)
    last_name = Column(String)

    is_active = Column(Boolean, default=True)
    refer_code = Column(String)

    code = relationship(
        "UserCode",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class UserCode(Base):
    """Таблица с реферальным кодом пользователя"""

    __tablename__ = "user_codes"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String, nullable=False)
    expiration_in_days = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="code")
