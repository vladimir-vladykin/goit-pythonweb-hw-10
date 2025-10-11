from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import ContactModel, ContactModelResponse
from src.database.db import get_db
from src.services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactModelResponse])
async def get_contacts(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    contact_service = ContactService(db)
    return await contact_service.get_contacts(skip, limit)


@router.get("/search", response_model=List[ContactModelResponse])
async def search_contacts(
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    if first_name is None and last_name is None and email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one search query should be presented",
        )
    contact_service = ContactService(db)
    return await contact_service.search_contacts(
        first_name, last_name, email, skip, limit
    )


@router.get("/closest_birthdays", response_model=List[ContactModelResponse])
async def get_closest_birthdays_contacts(db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    return await contact_service.get_closest_brithday_contacts()


@router.get("/{contact_id}", response_model=ContactModelResponse)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    return contact


@router.post(
    "/", response_model=ContactModelResponse, status_code=status.HTTP_201_CREATED
)
async def create_contact(body: ContactModel, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    return await contact_service.create_contact(body)


@router.delete("/{contact_id}", response_model=ContactModelResponse)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contact = await contact_service.delete_contact(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    return contact


@router.put("/{contact_id}", response_model=ContactModelResponse)
async def update_contact(
    contact_id: int, body: ContactModel, db: AsyncSession = Depends(get_db)
):
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, details="Contact not found"
        )

    return contact
