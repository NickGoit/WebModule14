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
        self.user = User(
            id=1,
            username='User1',
            email='user1@gmail.com',
            password ='qwerty')
        self.contact_test = Contact(
            id=1,
            first_name='Buster',
            last_name='Johns',
            email='buster@meta.ua',
            phone='+35428421424',
            date_of_birth=datetime.date(year=1985, month=10, day=8),
        )

    async def test_get_user_by_email(self):
        contact = self.contact_test
        self.session.query().filter().first.return_value = contact
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertEqual(result, contact)

    async def test_create_user(self):
        body = UserModel(
                        username=self.user.username,
                        email=self.user.email,
                        password=self.user.password,
            )
        result = await create_user(body=body, db=self.session)

        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))



if __name__ == '__main__':
    unittest.main()
