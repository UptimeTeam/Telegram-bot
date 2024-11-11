from sqlalchemy import String, BigInteger, Integer, Date, Time, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger,
                                             primary_key=True)  # Уникальный идентификатор пользователя в Telegram
    first_name: Mapped[str] = mapped_column(String, nullable=False)  # Имя пользователя
    username: Mapped[str] = mapped_column(String, nullable=True)  # Telegram username

    # Связь с заявками (один пользователь может иметь несколько заявок)
    applications: Mapped[list["Application"]] = relationship(back_populates="user")


class Admin(Base):
    __tablename__ = 'admins'

    admin_id: Mapped[int] = mapped_column(Integer, primary_key=True,
                                           autoincrement=True)  # Уникальный идентификатор админа
    admin_name: Mapped[str] = mapped_column(String, nullable=False)  # Имя админа

    # Связь с заявками (один админ может иметь несколько заявок)
    applications: Mapped[list["Application"]] = relationship(back_populates="flvby")


class Application(Base):
    __tablename__ = 'applications'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор заявки
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.telegram_id'))  # Внешний ключ на пользователя
    admin_id: Mapped[int] = mapped_column(Integer, ForeignKey('admins.admin_id'))  # Внешний ключ на админа
    appointment_date: Mapped[Date] = mapped_column(Date, nullable=False)  # Дата заявки
    appointment_time: Mapped[Time] = mapped_column(Time, nullable=False)  # Время заявки

    # Связи с админом, пользователем, заявкой
    user: Mapped["User"] = relationship(back_populates="applications")
    master: Mapped["Admin"] = relationship(back_populates="applications")
    service: Mapped["Application"] = relationship(back_populates="applications")