from datetime import date, timedelta

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import Contact
from app.schemas import ContactCreate, ContactUpdate


def create_contact(db: Session, contact_data: ContactCreate) -> Contact:
    contact = Contact(**contact_data.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_contacts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
) -> list[Contact]:
    query = db.query(Contact)

    filters = []
    if first_name:
        filters.append(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        filters.append(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        filters.append(Contact.email.ilike(f"%{email}%"))

    if filters:
        query = query.filter(or_(*filters))

    return query.offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int) -> Contact | None:
    return db.query(Contact).filter(Contact.id == contact_id).first()


def update_contact(
    db: Session, contact_id: int, contact_data: ContactUpdate
) -> Contact | None:
    contact = get_contact(db, contact_id)
    if contact is None:
        return None

    for field, value in contact_data.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)

    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(db: Session, contact_id: int) -> Contact | None:
    contact = get_contact(db, contact_id)
    if contact is None:
        return None

    db.delete(contact)
    db.commit()
    return contact


def get_upcoming_birthdays(db: Session) -> list[Contact]:
    today = date.today()
    upcoming = []

    for contact in db.query(Contact).all():
        try:
            birthday_this_year = contact.birthday.replace(year=today.year)
        except ValueError:
            birthday_this_year = contact.birthday.replace(year=today.year, day=28)

        if birthday_this_year < today:
            try:
                birthday_this_year = contact.birthday.replace(year=today.year + 1)
            except ValueError:
                birthday_this_year = contact.birthday.replace(year=today.year + 1, day=28)

        if today <= birthday_this_year <= today + timedelta(days=7):
            upcoming.append(contact)

    return upcoming
