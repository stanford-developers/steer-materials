import unittest
from steer_core.Constants.Units import AU_TO_KG

from steer_materials.Atoms import Atom


class TestAtom(unittest.TestCase):

    def setUp(self):
        self.atom = Atom(name="Plutonium", symbol="Pu", atomic_number=94, atomic_mass=244.0)

    def test_atom_properties(self):
        self.assertEqual(self.atom.name, "Plutonium")
        self.assertEqual(self.atom.symbol, "Pu")
        self.assertEqual(self.atom.atomic_number, 94)
        self.assertAlmostEqual(self.atom._atomic_mass, 244.0 * AU_TO_KG) 



