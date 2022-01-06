from typing import List

from app.models import Category
from fastack import ModelController
from fastack_sqlmodel.globals import db
from fastack_sqlmodel.session import Session
from fastapi import Request, Response
from pydantic import BaseModel, conint, constr
from sqlalchemy.sql.elements import and_


class BodyCategorySchema(BaseModel):
    name: constr(max_length=150)


class CategoryController(ModelController):
    def retrieve(self, request: Request, id: int) -> Response:
        session: Session = db.open()
        with session:
            category: Category = (
                session.query(Category).where(Category.id == id).first()
            )
            if not category:
                return self.json("Not Found", status=404)

            return self.json("Detail Category", category)

    def list(
        self, request: Request, page: conint(gt=0) = 1, page_size: conint(gt=0) = 10
    ) -> Response:
        session: Session = db.open()
        with session:
            categories: List[Category] = (
                session.query(Category).order_by(Category.date_created.desc()).all()
            )
            return self.get_paginated_response(categories, page, page_size)

    def create(self, request: Request, body: BodyCategorySchema) -> Response:
        session: Session = db.open()
        with session.begin():
            category: Category = (
                session.query(Category).where(Category.name == body.name).first()
            )
            if category:
                return self.json("Already exist", status=400)

            data = body.dict()
            category = Category.create(session, **data)

        return self.json("Created", category)

    def update(self, request: Request, id: int, body: BodyCategorySchema) -> Response:
        session: Session = db.open()
        with session.begin():
            qs = (
                session.query(Category)
                .where(and_(Category.name == body.name, Category.id != id))
                .exists()
            )
            found = session.query(qs).scalar()
            if found:
                return self.json("Already exist", status=400)

            category: Category = (
                session.query(Category).where(Category.id == id).first()
            )
            if not category:
                return self.json("Not Found", status=404)

            data = body.dict()
            category.update(session, **data)

        return self.json("Updated", category)

    def destroy(self, request: Request, id: int) -> Response:
        session: Session = db.open()
        with session.begin():
            category: Category = (
                session.query(Category).where(Category.id == id).first()
            )
            if not category:
                return self.json("Not Found", status=404)

            category.delete(session)

        return self.json("Deleted")
