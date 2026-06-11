import pytest
from steer_materials.Base import Metal, Solvent


@pytest.fixture
def aluminum():
    return Metal(name="Aluminum", density=2.7, specific_cost=2.50, color="silver")


@pytest.fixture
def water():
    return Solvent(name="Water", density=1.0, specific_cost=0.01, color="clear")
