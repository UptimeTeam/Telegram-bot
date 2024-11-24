from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from app.dao.base import BaseDAO
from app.api.models import User, Application, Admin
from app.database import async_session_maker

class UserDAO(BaseDAO):
    model = User

class ApplicationDAO(BaseDAO):
    model = Application

class AdminDAO(BaseDAO):
    model = Admin
    