import unittest
from unittest.mock import MagicMock

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
            phone='+35428421424'
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


if __name__ == '__main__':
    unittest.main()
