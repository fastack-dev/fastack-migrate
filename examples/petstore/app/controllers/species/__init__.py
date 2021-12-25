from typing import List

from app.models import Species
from fastack import CRUDController
from fastack_sqlmodel.session import Session
from fastapi import Request, Response
from pydantic import BaseModel, conint, constr
from sqlalchemy.sql.elements import and_


class BodySpeciesSchema(BaseModel):
    name: constr(max_length=150)


class SpeciesController(CRUDController):
    def retrieve(self, request: Request, id: int) -> Response:
        session: Session = request.state.db.open()
        with session:
            species: Species = session.query(Species).where(Species.id == id).first()
            if not species:
                return self.json("Not Found", status=404)

            return self.json("Detail Species", species)

    def list(
        self, request: Request, page: conint(gt=0) = 1, page_size: conint(gt=0) = 10
    ) -> Response:
        session: Session = request.state.db.open()
        with session:
            categories: List[Species] = (
                session.query(Species).order_by(Species.date_created.desc()).all()
            )
            return self.get_paginated_response(categories, page, page_size)

    def create(self, request: Request, body: BodySpeciesSchema) -> Response:
        session: Session = request.state.db.open()
        with session.begin():
            species: Species = (
                session.query(Species).where(Species.name == body.name).first()
            )
            if species:
                return self.json("Already exist", status=400)

            data = body.dict()
            species = Species.create(session, **data)

        return self.json("Created", species)

    def update(self, request: Request, id: int, body: BodySpeciesSchema) -> Response:
        session: Session = request.state.db.open()
        with session.begin():
            qs = (
                session.query(Species)
                .where(and_(Species.name == body.name, Species.id != id))
                .exists()
            )
            found = session.query(qs).scalar()
            if found:
                return self.json("Already exist", status=400)

            species: Species = session.query(Species).where(Species.id == id).first()
            if not species:
                return self.json("Not Found", status=404)

            data = body.dict()
            species.update(session, **data)

        return self.json("Updated", species)

    def destroy(self, request: Request, id: int) -> Response:
        session: Session = request.state.db.open()
        with session.begin():
            species: Species = session.query(Species).where(Species.id == id).first()
            if not species:
                return self.json("Not Found", status=404)

            species.delete(session)

        return self.json("Deleted")
