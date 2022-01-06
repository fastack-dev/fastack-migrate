from typing import List, Optional

from app.models import Animal, Category, Species
from fastack.controller import ModelController
from fastack_sqlmodel.globals import db
from fastack_sqlmodel.session import Session
from fastapi import Request, Response
from pydantic import BaseModel, conint, constr
from sqlalchemy import and_


class BodyAnimalSchema(BaseModel):
    name: constr(max_length=150)
    category: Optional[constr(max_length=150)]
    species: Optional[constr(max_length=150)]


class AnimalController(ModelController):
    def retrieve(self, request: Request, id: int) -> Response:
        session: Session = db.open()
        with session:
            animal: Animal = session.query(Animal).where(Animal.id == id).first()
            if not animal:
                return self.json("Not Found", status=404)

            return self.json("Detail Animal", animal)

    def list(
        self, request: Request, page: conint(gt=0) = 1, page_size: conint(gt=0) = 10
    ) -> Response:
        session: Session = db.open()
        with session:
            animals: List[Animal] = (
                session.query(Animal).order_by(Animal.date_created.desc()).all()
            )
            return self.get_paginated_response(animals, page, page_size)

    def create(self, request: Request, body: BodyAnimalSchema) -> Response:
        session: Session = db.open()
        with session.begin():
            found = bool(session.query(Animal).where(Animal.name == body.name).first())
            if found:
                return self.json("Already Exists", status=400)

            data = body.dict()
            category: Category = (
                session.query(Category).where(Category.name == body.category).first()
            )
            if not category:
                category = Category.create(session, name=body.category)

            data["category"] = category

            species: Species = (
                session.query(Species).where(Species.name == body.species).first()
            )
            if not species:
                species = Species.create(session, name=body.species)

            data["species"] = species
            animal = Animal.create(session, **data)

        return self.json("Created", animal)

    def update(self, request: Request, id: int, body: BodyAnimalSchema) -> Response:
        session: Session = db.open()
        with session.begin():
            animal: Animal = session.query(Animal).where(Animal.id == id).first()
            if not animal:
                return self.json("Not Found", status=404)

            found = bool(
                session.query(Animal)
                .where(and_(Animal.name == body.name, Animal.id != id))
                .first()
            )
            if found:
                return self.json("Already Exists", status=400)

            data = body.dict()
            category: Category = (
                session.query(Category).where(Category.name == body.category).first()
            )
            if not category:
                category = Category.create(session, name=body.category)

            data["category"] = category

            species: Species = (
                session.query(Species).where(Species.name == body.species).first()
            )
            if not species:
                species = Species.create(session, name=body.species)

            data["species"] = species
            animal.update(session, **data)

        return self.json("Updated", animal)

    def destroy(self, request: Request, id: int) -> Response:
        session: Session = db.open()
        with session.begin():
            animal: Animal = session.query(Animal).where(Animal.id == id).first()
            if not animal:
                return self.json("Not Found", status=404)

            animal.delete(session)

        return self.json("Deleted")
