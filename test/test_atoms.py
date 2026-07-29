import unittest
from steer_core.Constants.Units import AU_TO_KG

from steer_materials.Atoms import Atom


class TestAtom(unittest.TestCase):

    def setUp(self):
        self.atom = Atom(symbol="Pu", atomic_mass=244.0)

    def test_atom_properties(self):
        self.assertEqual(self.atom.name, "Plutonium")
        self.assertEqual(self.atom.symbol, "Pu")
        self.assertEqual(self.atom.atomic_number, 94)
        self.assertAlmostEqual(self.atom._atomic_mass, 244.0 * AU_TO_KG) 

    def test_atomic_mass_conversion(self):
        # Test that the atomic mass is correctly converted to kg
        expected_mass_kg = 244.0 * AU_TO_KG
        self.assertAlmostEqual(self.atom._atomic_mass, expected_mass_kg)

    def test_name_setter(self):
        self.atom.name = "Uranium"
        self.assertEqual(self.atom.symbol, "U")
        self.assertEqual(self.atom.atomic_number, 92)
        self.assertAlmostEqual(self.atom._atomic_mass, 238.02891 * AU_TO_KG)

    def test_mass_setter(self):
        self.atom.atomic_mass = 238.02891
        self.assertAlmostEqual(self.atom._atomic_mass, 238.02891 * AU_TO_KG)
        self.assertEqual(self.atom.symbol, "U")
        self.assertEqual(self.atom.atomic_number, 92)

    def test_symbol_setter(self):
        self.atom.symbol = "U"
        self.assertEqual(self.atom.name, "Uranium")
        self.assertEqual(self.atom.atomic_number, 92)
        self.assertAlmostEqual(self.atom._atomic_mass, 238.02891 * AU_TO_KG)
        
