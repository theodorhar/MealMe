import pytest
from src import user

def init_tests():
    user1 = user.User()
    assert user1._age == None
    user1.set_age(20)
    assert user1._age == 20
    with pytest.raises(TypeError):
        user1.set_age("bad")
    print("PASS: User Tests")
    


