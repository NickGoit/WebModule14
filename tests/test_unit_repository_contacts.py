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


if __name__ == '__main__':
    unittest.main()
