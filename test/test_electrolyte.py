import unittest

from steer_materials.Electrolytes.Electrolytes import Electrolyte


class TestElectrolyteVolumeMassCost(unittest.TestCase):

    def setUp(self):
        self.electrolyte = Electrolyte(
            name="Test Electrolyte",
            density=1.2,  # g/cm^3
            specific_cost=15.0,  # $/kg
            color="#abcdef",
        )

    def test_volume_setter_updates_mass_and_cost(self):
        self.electrolyte.volume = 10.0

        self.assertAlmostEqual(self.electrolyte.volume, 10.0, places=4)
        self.assertAlmostEqual(self.electrolyte.mass, 12.0, places=2)
        self.assertAlmostEqual(self.electrolyte.cost, 0.18, places=2)

    def test_mass_setter_updates_volume_and_cost(self):
        self.electrolyte.mass = 25.0

        self.assertAlmostEqual(self.electrolyte.mass, 25.0, places=2)
        self.assertAlmostEqual(self.electrolyte.volume, 20.8333, places=3)
        self.assertAlmostEqual(self.electrolyte.cost, 0.38, places=2)

    def test_cost_setter_updates_mass_and_volume(self):
        self.electrolyte.cost = 5.0

        self.assertAlmostEqual(self.electrolyte.cost, 5.0, places=2)
        self.assertAlmostEqual(self.electrolyte.mass, 333.33, places=2)
        self.assertAlmostEqual(self.electrolyte.volume, 277.7778, places=1)


if __name__ == "__main__":
    unittest.main()
