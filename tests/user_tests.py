import pytest
from web import user,load_data
def all_tests():
    init_tests()
    add_tests()
    favorability_array_tests()
def init_tests():
    user1 = user.User()
    assert user1._age == None
    user1.set_age(20)
    assert user1._age == 20
    with pytest.raises(TypeError):
        user1.set_age("bad")
    assert len(user1._recipes_liked) == 0
    assert len(user1._recipes_made) == 0
    assert len(user1._recipes_viewed) == 0
    assert user1.get_favorability_array([],[]).size == 0
    print("PASS: User Tests: Init Tests")
def add_tests():
    user1 = user.User()
    assert user1.get_favorability_array([],[]).size == 0
    user1.add_like(0)
    user1.add_like(2)
    assert len(user1._recipes_liked) == 2
    assert 0 in user1._recipes_liked
    assert 1 not in user1._recipes_liked
    assert 2 in user1._recipes_liked
    with pytest.raises(ValueError):
        user1.add_like(-1)
        user1.add_like(-20)

    user1.add_view(0)
    user1.add_view(1)
    assert 0 in user1._recipes_viewed
    assert 1 in user1._recipes_viewed
    assert 2 not in user1._recipes_viewed
    with pytest.raises(TypeError):
        user1.add_view("hi")
    with pytest.raises(ValueError):
        user1.add_view(-1)
        user1.add_view(-20)

    user1.add_make(0) #These ints are random ints I chose
    user1.add_make(13)
    assert 0 in user1._recipes_made
    assert 13 in user1._recipes_made
    assert 2 not in user1._recipes_made
    with pytest.raises(TypeError):
        user1.add_make("hi")
    with pytest.raises(ValueError):
        user1.add_make(-1)
        user1.add_make(-20)

    print("PASS: User Tests: Add Tests")
def favorability_array_tests():
    recipes = load_data.get_recipe_data()
    user1 = user.User()
    assert user1._weight_matrix.tolist() == [2,2,1,5]
    user1.add_view(0)
    user1.add_view(1)
    user1.add_view(2)
    user1.add_like(0)
    user1.add_make(1)
    matrix = user1.get_favorability_array(['coconut milk','white sugar'],recipes)
    print(matrix)
    print("PRINTED: User Tests: Favorability Matrix")