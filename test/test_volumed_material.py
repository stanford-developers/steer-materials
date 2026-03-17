import pytest
from steer_materials.Base import Metal, _VolumedMaterialMixin


class VolumedMetal(_VolumedMaterialMixin, Metal):
    """Concrete test class combining the mixin with Metal."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@pytest.fixture
def volumed_al():
    return VolumedMetal(
        name="Aluminum", density=2.7, specific_cost=2.50, color="silver", volume=100.0
    )


@pytest.fixture
def mass_al():
    return VolumedMetal(
        name="Aluminum", density=2.7, specific_cost=2.50, color="silver", mass=270.0
    )


@pytest.fixture
def bare_al():
    return VolumedMetal(
        name="Aluminum", density=2.7, specific_cost=2.50, color="silver"
    )


class TestVolumedMaterialInit:
    """Tests for _VolumedMaterialMixin initialization."""

    def test_volume_init_derives_mass_and_cost(self, volumed_al):
        assert volumed_al.volume == 100.0
        assert volumed_al.mass == 270.0
        assert volumed_al.cost == 0.68

    def test_mass_init_derives_volume_and_cost(self, mass_al):
        assert mass_al.volume == 100.0
        assert mass_al.mass == 270.0
        assert mass_al.cost == 0.68

    def test_no_volume_or_mass_gives_none(self, bare_al):
        assert bare_al.volume is None
        assert bare_al.mass is None
        assert bare_al.cost is None

    def test_both_volume_and_mass_raises(self):
        with pytest.raises(ValueError, match="Only one of"):
            VolumedMetal(
                name="Al",
                density=2.7,
                specific_cost=2.50,
                color="silver",
                volume=100.0,
                mass=270.0,
            )


class TestVolumedMaterialSetters:
    """Tests for volume and mass setters."""

    def test_set_volume(self, bare_al):
        bare_al.volume = 100.0
        assert bare_al.volume == 100.0
        assert bare_al.mass == 270.0
        assert bare_al.cost == 0.68

    def test_set_mass(self, bare_al):
        bare_al.mass = 270.0
        assert bare_al.volume == 100.0
        assert bare_al.mass == 270.0
        assert bare_al.cost == 0.68

    def test_set_volume_to_none_clears_all(self, volumed_al):
        volumed_al.volume = None
        assert volumed_al.volume is None
        assert volumed_al.mass is None
        assert volumed_al.cost is None

    def test_set_mass_to_none_clears_all(self, mass_al):
        mass_al.mass = None
        assert mass_al.volume is None
        assert mass_al.mass is None
        assert mass_al.cost is None

    def test_negative_volume_raises(self, bare_al):
        with pytest.raises(ValueError):
            bare_al.volume = -10.0

    def test_negative_mass_raises(self, bare_al):
        with pytest.raises(ValueError):
            bare_al.mass = -10.0

    def test_non_numeric_volume_raises(self, bare_al):
        with pytest.raises(TypeError):
            bare_al.volume = "big"

    def test_non_numeric_mass_raises(self, bare_al):
        with pytest.raises(TypeError):
            bare_al.mass = "heavy"


class TestVolumedMaterialPropagation:
    """Tests for propagation when density or specific_cost changes."""

    def test_density_change_updates_mass_and_cost(self, volumed_al):
        # volume=100 cm³, density 2.7→5.0 g/cm³
        volumed_al.density = 5.0
        assert volumed_al.volume == 100.0
        assert volumed_al.mass == 500.0
        assert volumed_al.cost == 1.25

    def test_specific_cost_change_updates_cost(self, volumed_al):
        # mass=270g, specific_cost 2.50→5.0 $/kg
        volumed_al.specific_cost = 5.0
        assert volumed_al.volume == 100.0
        assert volumed_al.mass == 270.0
        assert volumed_al.cost == 1.35

    def test_density_change_no_effect_without_volume(self, bare_al):
        bare_al.density = 5.0
        assert bare_al.volume is None
        assert bare_al.mass is None
        assert bare_al.cost is None
