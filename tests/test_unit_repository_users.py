import datetime
import unittest
from unittest.mock import MagicMock
from datetime import date

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact_test = Contact(
            id=1,
            first_name='Buster',
            last_name='Johns',
            email='buster@meta.ua',
            phone='+35428421424',
            date_of_birth=datetime.date(year=1985, month=10, day=8),
        )

    async def test_get_user_by_email(self):
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().offset().limit().all.return_value = contacts
        result = await get_user_by_email(email=self.contact_test, db=self.session)
        self.assertEqual(result, contacts)

        # get_user_by_email(email: str, db: Session) -> User | None:
        # db.query(User).filter(User.email == email).first()