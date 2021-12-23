from typing import List, Optional

from fastack.plugins.sqlmodel.base import Model
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship


class Category(Model, table=True):
    __table_args__ = (UniqueConstraint("name"),)

    name: str = Field(max_length=150, nullable=False)
    animals: List["Animal"] = Relationship(back_populates="category")

    def serialize(self, include_animals: bool = True) -> dict:
        data = super().serialize()
        data["name"] = self.name
        if include_animals:
            animals = [x.serialize(include_category=False) for x in self.animals]
            data["animals"] = animals

        return data


class Species(Model, table=True):
    __table_args__ = (UniqueConstraint("name"),)

    name: str = Field(max_length=150, nullable=False)
    animals: List["Animal"] = Relationship(back_populates="species")

    def serialize(self, include_animals: bool = True) -> dict:
        data = super().serialize()
        data["name"] = self.name
        if include_animals:
            animals = [x.serialize(include_species=False) for x in self.animals]
            data["animals"] = animals

        return data


class Animal(Model, table=True):
    __table_args__ = (UniqueConstraint("name"),)

    name: str = Field(max_length=150, nullable=False)
    category_id: Optional[int] = Field(foreign_key="category.id", nullable=True)
    category: Optional[Category] = Relationship(back_populates="animals")
    species_id: int = Field(foreign_key="species.id", nullable=True)
    species: Optional[Species] = Relationship(back_populates="animals")

    def serialize(
        self, include_species: bool = True, include_category: bool = True
    ) -> dict:
        data = super().serialize()
        data["name"] = self.name
        if include_species:
            data["species"] = (
                self.species.serialize(include_animals=False) if self.species else None
            )

        if include_category:
            data["category"] = (
                self.category.serialize(include_animals=False)
                if self.category
                else None
            )

        return data
