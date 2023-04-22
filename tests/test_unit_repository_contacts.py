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

    async def test_get_notes(self):
        notes = [Note(), Note(), Note()]
        self.session.query().filter().offset().limit().all.return_value = notes
        result = await get_notes(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, notes)