from steer_core.Constants.Units import *
from steer_materials.Base import _Material


class Electrolyte(_Material):

    def __init__(
            self, 
            name: str, 
            density: float, 
            specific_cost: float, 
            color: str
        ):

        super().__init__(name, density, specific_cost, color)

