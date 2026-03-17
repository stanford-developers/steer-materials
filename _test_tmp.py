from steer_materials.Base import Metal, _VolumedMaterialMixin

class VM(_VolumedMaterialMixin, Metal):
    def __init__(self, **kw):
        super().__init__(**kw)

# mutual exclusivity
try:
    VM(name='A', density=2.7, specific_cost=2.5, color='s', volume=100, mass=270)
except ValueError as e:
    print(f'Both: {e}')

# None clearing
m = VM(name='A', density=2.7, specific_cost=2.5, color='s', volume=100)
m.volume = None
print('After None:', m.volume, m.mass, m.cost)

# density change propagation
m2 = VM(name='A', density=2.7, specific_cost=2.5, color='s', volume=100)
print('Before density:', m2.volume, m2.mass, m2.cost)
m2.density = 5.0
print('After density:', m2.volume, m2.mass, m2.cost)

# specific_cost change propagation
m3 = VM(name='A', density=2.7, specific_cost=2.5, color='s', volume=100)
print('Before cost change:', m3.volume, m3.mass, m3.cost)
m3.specific_cost = 5.0
print('After cost change:', m3.volume, m3.mass, m3.cost)
