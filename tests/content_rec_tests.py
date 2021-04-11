from src import user,content_based_rec,data_processing
import pytest
DEBUG = False
def all_tests():
    simple_rec()
def simple_rec():
    raw_data = data_processing.get_raw_data(debug = DEBUG)
    recipes = data_processing.get_recipes(raw_data, debug = DEBUG)
    user1 = user.User()
    assert user1._weight_matrix.tolist() == [2,2,1,5]
    for i in range(0,50):
        user1.add_view(i)
    print("LOADED: User")
    print(content_based_rec.get_recommendations(user1,recipes,10))