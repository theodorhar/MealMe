from src import user,content_based_rec,load_data
import pytest
DEBUG = False
def all_tests():
    simple_rec()
def simple_rec():
    recipes = load_data.get_recipe_data(debug = DEBUG)
    load_data.get_recipe_lookup()
    user1 = user.User()
    assert user1._weight_matrix.tolist() == [2,2,1,5]
    for i in range(0,50):
        user1.add_view(i)
    print("LOADED: User")
    print(content_based_rec.get_recommendations(user1,recipes,10))