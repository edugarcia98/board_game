from schemas import Property


def mocked_property():
    return Property(name="Propriedade Test", cost=100, rent_cost=20, owner=None)


def mocked_board():
    return [
        Property(name="Propriedade Test 1", cost=100, rent_cost=20, owner=None),
        Property(name="Propriedade Test 2", cost=200, rent_cost=30, owner=None),
        Property(name="Propriedade Test 3", cost=200, rent_cost=30, owner=None),
        Property(name="Propriedade Test 4", cost=200, rent_cost=30, owner=None),
        Property(name="Propriedade Test 5", cost=200, rent_cost=30, owner=None),
    ]
