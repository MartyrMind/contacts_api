from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..database import add_contact, delete_contact, retrieve_contact, retrieve_contacts, update_contact
from ..models.contact import ContactSchema, UpdateContactModel, ResponseModel, ErrorResponseModel

router = APIRouter()


@router.post("/", response_description="Contact data added into the database")
async def add_contact_data(contact: ContactSchema = Body(...)):
    contact = jsonable_encoder(contact)
    new_contact = await add_contact(contact)
    return ResponseModel(data=new_contact, message="Contact added successfully.")


@router.get("/", response_description="Contacts retrieved")
async def get_contacts():
    contacts = await retrieve_contacts()
    message = "Contact data retrieved successfully" if contacts else "Empty list retrieved"
    return ResponseModel(data=contacts, message=message)


@router.get("/{contact_id}", response_description="Contact data retrieved")
async def get_contact_data(contact_id: str):
    contact = await retrieve_contact(contact_id)
    if contact:
        return ResponseModel(data=contact, message="Contact data retrieved successfully")
    return ErrorResponseModel(error="Contact doesn't exist", code=404, message="An error occurred")


@router.put("/{contact_id}")
async def update_contact_data(contact_id: str, changes: UpdateContactModel = Body(...)):
    changes = {k: v for (k, v) in changes.model_dump().items() if v is not None}
    updated_contact = await update_contact(contact_id, data=changes)
    if updated_contact:
        return ResponseModel(data=f"Contact with ID {contact_id} successfully updated", message="OK")
    return ErrorResponseModel(error="There was an error updating contact data", code=404, message="An error occurred")


@router.delete("/{contact_id}")
async def delete_contact_data(contact_id: str):
    deleted_contact = await delete_contact(contact_id)
    if deleted_contact:
        return ResponseModel(data=f"Contact with ID {contact_id} removed", message="OK")
    return ErrorResponseModel(error=f"Contact with ID {contact_id} doesn't exist", code=404, message="Error occurred")
