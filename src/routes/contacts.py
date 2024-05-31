from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository import contacts as repositories_contact
from src.database.db import get_db
from src.schemas.contact import ContactInput, ContactOutput

router = APIRouter(prefix='/contacts', tags=['contact'])

@router.get(path='/', response_model=list[ContactOutput])
async def get_contacts(limit: int = Query(default=10, ge=10, le=500), offset: int = Query(default=0), db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contact.get_contacts(limit, offset, db)
    return contacts

@router.get(path='/id/{contact_id}', response_model=ContactOutput)
async def get_contacts_by_id(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await repositories_contact.get_contacts_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found!')
    return contact

@router.get(path='/first_name/{first_name}', response_model=list[ContactOutput])
async def get_contacts_by_first_name(first_name: str, db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contact.get_contacts_by_first_name(first_name, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found!')
    return contacts

@router.get(path='/last_name/{last_name}', response_model=list[ContactOutput])
async def get_contacts_by_last_name(last_name: str, db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contact.get_contacts_by_last_name(last_name, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found!')
    return contacts

@router.get(path='/email/{email}', response_model=ContactOutput)
async def get_contacts_by_email(email: str, db: AsyncSession = Depends(get_db)):
    contact = await repositories_contact.get_contacts_by_email(email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found!')
    return contact

@router.post(path='/', response_model=ContactOutput, status_code=status.HTTP_201_CREATED)
async def create_contacts(body: ContactInput, db: AsyncSession = Depends(get_db)):
    contact = await repositories_contact.create_contacts(body, db)
    return contact

@router.put(path='/id/{contact_id}', response_model=ContactOutput)
async def update_contacts(contact_id: int, body: ContactInput, db: AsyncSession = Depends(get_db)):
    contact = await repositories_contact.update_contacts(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found!')
    return contact

@router.delete(path='/id/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contacts(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await repositories_contact.delete_contacts(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found!')
    return {"detail": "Contact deleted successfully"}

@router.get(path='/birthday/next_week', response_model=list[ContactOutput])
async def get_contacts_with_upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contact.get_contacts_with_upcoming_birthdays(db)
    return contacts
