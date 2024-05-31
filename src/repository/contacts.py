from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import func
from src.schemas.contact import ContactInput
from src.entity.models import Contact
from datetime import date, datetime, timedelta

async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

async def get_contacts_by_id(contact_id: str, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()

async def get_contacts_by_first_name(first_name: str, db: AsyncSession):
    stmt = select(Contact).filter_by(first_name=first_name)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

async def get_contacts_by_last_name(last_name: str, db: AsyncSession):
    stmt = select(Contact).filter_by(last_name=last_name)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

async def get_contacts_by_email(email: str, db: AsyncSession):
    stmt = select(Contact).filter_by(email=email)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()

async def create_contacts(body: ContactInput, db: AsyncSession):
    contact_data = body.model_dump(exclude_unset=True)
    
    # Преобразование даты в строку, если поле birthday существует
    if 'birthday' in contact_data and isinstance(contact_data['birthday'], date):
        contact_data['birthday'] = contact_data['birthday'].strftime('%Y-%m-%d')
    
    contact = Contact(**contact_data)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

async def update_contacts(contact_id: int, body: ContactInput, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if not contact:
        return None
    contact.first_name = body.first_name
    contact.last_name = body.last_name
    contact.email = body.email
    contact.phone_number = body.phone_number
    contact.birthday = body.birthday
    contact.other = body.other
    await db.commit()
    await db.refresh(contact)
    return contact

async def delete_contacts(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if not contact:
        return None
    await db.delete(contact)
    await db.commit()
    return contact


async def get_contacts_with_upcoming_birthdays(db: AsyncSession):
    current_date = datetime.now().date()
    one_week_later = current_date + timedelta(days=7)
    
    # Получаем всех контактов
    stmt = select(Contact).filter(Contact.birthday != None)
    result = await db.execute(stmt)
    contacts = result.scalars().all()

    upcoming_birthdays = []
    for contact in contacts:
        if isinstance(contact.birthday, str):
            birthday = datetime.strptime(contact.birthday, '%Y-%m-%d').date()
        else:
            birthday = contact.birthday
        birthday_this_year = birthday.replace(year=current_date.year)
        days_until_birthday = (birthday_this_year - current_date).days
        if 0 <= days_until_birthday <= 7:
            upcoming_birthdays.append(contact)

    return upcoming_birthdays
