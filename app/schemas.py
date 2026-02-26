from datetime import date
from pydantic import BaseModel, EmailStr, Field


class RegisterUserIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    first_name: str
    last_name: str
    birth_date: date | None = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class CreateFamilyIn(BaseModel):
    name: str
    owner_user_id: int


class FamilyOut(BaseModel):
    id: int
    name: str
    invite_code: str

    class Config:
        from_attributes = True


class JoinFamilyIn(BaseModel):
    user_id: int
    invite_code: str


class AddPersonIn(BaseModel):
    family_id: int
    created_by_user_id: int
    first_name: str
    last_name: str
    birth_date: date | None = None


class PersonOut(BaseModel):
    id: int
    family_id: int
    created_by_user_id: int
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class AddRelationshipIn(BaseModel):
    family_id: int
    person_a_id: int
    person_b_id: int
    relation_type: str


class RelationshipOut(BaseModel):
    id: int
    family_id: int
    person_a_id: int
    person_b_id: int
    relation_type: str

    class Config:
        from_attributes = True
