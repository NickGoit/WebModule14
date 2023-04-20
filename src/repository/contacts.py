from typing import List
from datetime import date, timedelta
from sqlalchemy import or_, and_

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contact_by_id(contact_id: int, db: Session):
    """
The get_contact_by_id function returns a contact from the database by its id.

:param contact_id: int: Specify the id of the contact that we want to retrieve
:param db: Session: Pass in the database session to be used for querying
:return: A contact object
:doc-author: Trelent
"""
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def get_contacts(skip: int,
                       limit: int,
                       first_name: str,
                       last_name: str,
                       email: str,
                       db: Session):

    """
The get_contacts function returns a list of contacts from the database.

:param skip: int: Skip a number of records in the database
:param limit: int: Limit the number of results returned
:param first_name: str: Filter the contacts by first name
:param last_name: str: Filter the contacts by last name
:param email: str: Filter the contacts by email
:param db: Session: Pass the database session to the function
:return: A list of contacts
:doc-author: Trelent
"""
    if first_name:
            if last_name or email:
                return db.query(Contact).select_from(Contact)\
                                  .filter(Contact.first_name == first_name,
                                          or_(Contact.last_name == last_name, Contact.email == email)).all()
            else:
                return db.query(Contact).filter(Contact.first_name == first_name).all()

    if last_name:
        if email:
            return db.query(Contact).select_from(Contact) \
                .filter(Contact.last_name == last_name, Contact.email == email).all()
        else:
            return db.query(Contact).filter(Contact.last_name == last_name).all()

    if email:
        return db.query(Contact).filter(Contact.email == email).all()

    return db.query(Contact).offset(skip).limit(limit).all()


async def verify_email_phone(email: str, phone: str, db: Session):
    """
The verify_email_phone function is used to verify that the email and phone number provided by the user are not already in use.
    If either of them are, then an error message will be returned to the user.

:param email: str: Pass the email address to the function
:param phone: str: Pass in the phone number to be verified
:param db: Session: Pass the database session to the function
:return: A tuple of email and phone data
:doc-author: Trelent
"""
    email_data = db.query(Contact.email).filter(Contact.email == email).first()
    if email_data:
        return email_data

    phone_data = db.query(Contact.phone).filter(Contact.phone == phone).first()
    if phone_data:
        return phone_data

    return None


async def get_contact_birthday(skip: int,
                               limit: int, db: Session):
    """
The get_contact_birthday function returns a list of contacts with birthdays in the next 7 days.
    The function takes two arguments: skip and limit, which are used to paginate the results.
    It also takes a db Session object as an argument.

:param skip: int: Skip the first n number of contacts
:param limit: int: Limit the number of contacts returned by the function
:param db: Session: Pass the database session to the function
:return: A list of contacts with birthday in the next 7 days
:doc-author: Trelent
"""
    contacts_with_next_birth = []
    today = date.today()
    all_contacts = db.query(Contact).offset(skip).limit(limit).all()
    for contact in all_contacts:
        if contact.date_of_birth.month == today.month:
            if 0 <= (contact.date_of_birth.day - today.day) <= 7:
                contacts_with_next_birth.append(contact)
        else:
            continue
    return contacts_with_next_birth


async def create_contact(body: ContactModel, db: Session, user: User):
    """
The create_contact function creates a new contact in the database.

:param body: ContactModel: Get the data from the request body
:param db: Session: Access the database
:param user: User: Get the user id of the current logged in user
:return: The contact created
:doc-author: Trelent
"""
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session, user: User):
    """
The update_contact function updates a contact in the database.
    Args:
        contact_id (int): The id of the contact to update.
        body (ContactModel): The updated information for the specified user's contact.

:param contact_id: int: Identify the contact that is being updated
:param body: ContactModel: Pass the json data from the request body to the function
:param db: Session: Pass the database session to the function
:param user: User: Get the user id from the token
:return: The updated contact object
:doc-author: Trelent
"""
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.date_of_birth = body.date_of_birth
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session, user: User):
    """
The remove_contact function removes a contact from the database.
    Args:
        contact_id (int): The id of the contact to be removed.
        db (Session): A connection to the database.
        user (User): The user who is removing this contact.

:param contact_id: int: Specify the id of the contact to be deleted
:param db: Session: Access the database
:param user: User: Get the user id from the token
:return: A contact object
:doc-author: Trelent
"""
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
