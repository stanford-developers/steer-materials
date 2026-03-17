import pytest
import numpy as np
from steer_materials.Base import _Material, Metal, Solvent


class TestMaterialConstruction:
    """Tests for constructing _Material, Metal, and Solvent instances."""

    def test_metal_valid_construction(self, aluminum):
        assert aluminum.name == "Aluminum"
        assert aluminum.density == 2.7
        assert aluminum.specific_cost == 2.50
        assert aluminum.color == "silver"

    def test_solvent_valid_construction(self, water):
        assert water.name == "Water"
        assert water.density == 1.0
        assert water.specific_cost == 0.01
        assert water.color == "clear"

    def test_negative_density_raises(self):
        with pytest.raises(ValueError):
            Metal(name="Bad", density=-1.0, specific_cost=1.0, color="red")

    def test_zero_density_allowed(self):
        # validate_positive_float allows zero
        m = Metal(name="Zero", density=0.0, specific_cost=1.0, color="red")
        assert m.density == 0.0

    def test_negative_specific_cost_raises(self):
        with pytest.raises(ValueError):
            Metal(name="Bad", density=1.0, specific_cost=-5.0, color="red")

    def test_non_numeric_density_raises(self):
        with pytest.raises(TypeError):
            Metal(name="Bad", density="heavy", specific_cost=1.0, color="red")

    def test_non_numeric_specific_cost_raises(self):
        with pytest.raises(TypeError):
            Metal(name="Bad", density=1.0, specific_cost="cheap", color="red")

    def test_non_string_name_raises(self):
        with pytest.raises(TypeError):
            Metal(name=123, density=1.0, specific_cost=1.0, color="red")

    def test_non_string_color_raises(self):
        with pytest.raises(TypeError):
            Metal(name="Test", density=1.0, specific_cost=1.0, color=42)


class TestMaterialProperties:
    """Tests for property getters and unit conversions."""

    def test_density_returns_g_per_cm3(self):
        # Input 2.7 g/cm³ should come back as 2.7
        m = Metal(name="Al", density=2.7, specific_cost=1.0, color="grey")
        assert m.density == 2.7

    def test_specific_cost_returns_per_kg(self):
        m = Metal(name="Al", density=2.7, specific_cost=3.45, color="grey")
        assert m.specific_cost == 3.45

    def test_density_round_trip(self):
        # Verify internal storage → getter round-trips correctly
        for val in [0.5, 1.0, 7.87, 19.3, 22.59]:
            m = Metal(name="Test", density=val, specific_cost=1.0, color="x")
            assert abs(m.density - val) < 0.01

    def test_last_updated_format(self, aluminum):
        # Should be a string in YYYY-MM-DD HH:MM:SS format
        ts = aluminum.last_updated
        assert len(ts) == 19
        assert ts[4] == "-" and ts[7] == "-" and ts[10] == " "


class TestMaterialSetters:
    """Tests for property setters and propagation."""

    def test_set_density(self, aluminum):
        aluminum.density = 5.0
        assert aluminum.density == 5.0

    def test_set_specific_cost(self, aluminum):
        aluminum.specific_cost = 10.0
        assert aluminum.specific_cost == 10.0

    def test_set_name(self, aluminum):
        aluminum.name = "Steel"
        assert aluminum.name == "Steel"

    def test_set_color(self, aluminum):
        aluminum.color = "blue"
        assert aluminum.color == "blue"

    def test_set_invalid_density_raises(self, aluminum):
        with pytest.raises(ValueError):
            aluminum.density = -1.0

    def test_set_invalid_specific_cost_raises(self, aluminum):
        with pytest.raises(ValueError):
            aluminum.specific_cost = -1.0

    def test_set_non_string_name_raises(self, aluminum):
        with pytest.raises(TypeError):
            aluminum.name = 999

    def test_set_non_string_color_raises(self, aluminum):
        with pytest.raises(TypeError):
            aluminum.color = 999


class TestMaterialRanges:
    """Tests for range calculations."""

    def test_density_range_within_10_percent(self, aluminum):
        low, high = aluminum.density_range
        assert low == pytest.approx(2.7 * 0.9, abs=0.01)
        assert high == pytest.approx(2.7 * 1.1, abs=0.01)

    def test_specific_cost_range(self, aluminum):
        low, high = aluminum.specific_cost_range
        assert low == pytest.approx(2.50 * 0.5, abs=0.01)
        assert high == pytest.approx(2.50 * 2.0, abs=0.01)

    def test_density_hard_range(self, aluminum):
        assert aluminum.density_hard_range == (0, 100)

    def test_specific_cost_hard_range(self, aluminum):
        assert aluminum.specific_cost_hard_range == (0, 1000)


class TestMetalAndSolventSubclasses:
    """Verify Metal and Solvent behave identically to _Material."""

    def test_metal_is_material(self, aluminum):
        assert isinstance(aluminum, _Material)

    def test_solvent_is_material(self, water):
        assert isinstance(water, _Material)

    def test_metal_and_solvent_independent(self, aluminum, water):
        aluminum.name = "Changed"
        assert water.name == "Water"
