import datetime
import unittest
from unittest.mock import MagicMock
from datetime import date

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contact_by_id,
    get_contacts,
    verify_email_phone,
    get_contact_birthday,
    create_contact,
    update_contact,
    remove_contact,
)


class TestNotes(unittest.IsolatedAsyncioTestCase):

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

    async def test_get_contacts(self):
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, first_name='', last_name='', email='', db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_first_name(self):
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, first_name=self.contact_test.first_name,
                                    last_name='', email='', db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_first_name_and_email(self):
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().select_from().filter().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, first_name=self.contact_test.first_name,
                                    last_name='', email=self.contact_test.email, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_last_name(self):
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, first_name='',
                                    last_name=self.contact_test.last_name, email='', db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_last_name_and_email(self):
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().select_from().filter().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, first_name='', last_name=self.contact_test.last_name,
                                    email=self.contact_test.email, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_email(self):
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, first_name='',
                                    last_name='', email=self.contact_test.email, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_id(self):
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().filter().first.return_value = contacts
        result = await get_contact_by_id(contact_id=self.contact_test.id, db=self.session)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactModel(
            first_name=self.contact_test.first_name,
            last_name=self.contact_test.last_name,
            email=self.contact_test.email,
            phone=self.contact_test.email,
            date_of_birth=self.contact_test.date_of_birth,
        )
        result = await create_contact(body=body, db=self.session, user=self.user)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.date_of_birth, body.date_of_birth)
        self.assertTrue(hasattr(result, "id"))



if __name__ == '__main__':
    unittest.main()
