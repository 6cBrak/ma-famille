import secrets
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import Family, FamilyMember, FamilyRole, Person, RelationType, Relationship, User
from app.schemas import (
    AddPersonIn,
    AddRelationshipIn,
    CreateFamilyIn,
    FamilyOut,
    JoinFamilyIn,
    PersonOut,
    RegisterUserIn,
    RelationshipOut,
    UserOut,
)

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Ma Famille API", version="0.1.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


@app.post("/users/register", response_model=UserOut)
def register_user(payload: RegisterUserIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    user = User(**payload.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/families", response_model=FamilyOut)
def create_family(payload: CreateFamilyIn, db: Session = Depends(get_db)):
    owner = db.get(User, payload.owner_user_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    family = Family(name=payload.name, invite_code=secrets.token_hex(4))
    db.add(family)
    db.commit()
    db.refresh(family)

    db.add(FamilyMember(user_id=owner.id, family_id=family.id, role=FamilyRole.ADMIN))
    db.commit()

    return family


@app.post("/families/join", response_model=FamilyOut)
def join_family(payload: JoinFamilyIn, db: Session = Depends(get_db)):
    user = db.get(User, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    family = db.query(Family).filter(Family.invite_code == payload.invite_code).first()
    if not family:
        raise HTTPException(status_code=404, detail="Invitation invalide")

    exists = (
        db.query(FamilyMember)
        .filter(FamilyMember.user_id == user.id, FamilyMember.family_id == family.id)
        .first()
    )
    if not exists:
        db.add(FamilyMember(user_id=user.id, family_id=family.id, role=FamilyRole.MEMBER))
        db.commit()

    return family


def require_membership(db: Session, user_id: int, family_id: int):
    membership = (
        db.query(FamilyMember)
        .filter(FamilyMember.user_id == user_id, FamilyMember.family_id == family_id)
        .first()
    )
    if not membership:
        raise HTTPException(status_code=403, detail="Utilisateur non membre de cette famille")


@app.post("/persons", response_model=PersonOut)
def add_person(payload: AddPersonIn, db: Session = Depends(get_db)):
    require_membership(db, payload.created_by_user_id, payload.family_id)
    person = Person(**payload.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@app.post("/relationships", response_model=RelationshipOut)
def add_relationship(payload: AddRelationshipIn, db: Session = Depends(get_db)):
    if payload.person_a_id == payload.person_b_id:
        raise HTTPException(status_code=400, detail="Une personne ne peut pas être liée à elle-même")

    try:
        relation_type = RelationType(payload.relation_type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="relation_type invalide") from exc

    person_a = db.get(Person, payload.person_a_id)
    person_b = db.get(Person, payload.person_b_id)
    if not person_a or not person_b:
        raise HTTPException(status_code=404, detail="Personne introuvable")
    if person_a.family_id != payload.family_id or person_b.family_id != payload.family_id:
        raise HTTPException(status_code=400, detail="Les deux personnes doivent appartenir à la même famille")

    rel = Relationship(
        family_id=payload.family_id,
        person_a_id=payload.person_a_id,
        person_b_id=payload.person_b_id,
        relation_type=relation_type,
    )
    db.add(rel)
    db.commit()
    db.refresh(rel)
    return rel


@app.get("/tree/{family_id}")
def get_tree(family_id: int, db: Session = Depends(get_db)):
    persons = db.query(Person).filter(Person.family_id == family_id).all()
    relations = db.query(Relationship).filter(Relationship.family_id == family_id).all()
    return {
        "family_id": family_id,
        "persons": [
            {
                "id": p.id,
                "first_name": p.first_name,
                "last_name": p.last_name,
            }
            for p in persons
        ],
        "relationships": [
            {
                "id": r.id,
                "person_a_id": r.person_a_id,
                "person_b_id": r.person_b_id,
                "relation_type": r.relation_type.value,
            }
            for r in relations
        ],
    }
