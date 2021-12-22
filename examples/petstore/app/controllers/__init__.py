from app.controllers.animal import AnimalController
from app.controllers.category import CategoryController
from app.controllers.species import SpeciesController
from fastack import Fastack


def init_controllers(app: Fastack):
    app.include_controller(AnimalController())
    app.include_controller(CategoryController())
    app.include_controller(SpeciesController())
