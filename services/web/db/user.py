from flask_login import UserMixin
from mysql.connector.connection import MySQLConnection

#needs access to: current recipes database to fetch recipes
class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(connection: MySQLConnection, user_id: int):
        if connection == None:
            raise ConnectionError("Database connection is invalid")
        db = connection.cursor()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        )
        return user

    @staticmethod
    def create(connection: MySQLConnection, id_: int, name: str, email: str, profile_pic: str):
        if connection == None:
            raise ConnectionError("Database connection is invalid")
        db = connection.cursor()
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic) "
            "VALUES (?, ?, ?, ?)",
            (id_, name, email, profile_pic),
        )
        db.commit()
    # def __init__(self):
    #     self._age = None
    #     self._name = None
    #     self._location = None
    #     self._id = None
    #     self._recipes_viewed = []
    #     self._recipes_made = []  #if it is in made it must be in viewed
    #     self._recipes_liked = [] #if it is in liked it must be in viewed
    #     self._ingredients_owned = collections.defaultdict(lambda : 0)
    #     self._weight_matrix = np.array([2,2,1,5]) #like,made,view,own weights in order
    # def set_age(self,age:int) -> None:
    #     if type(age) != int:
    #         raise TypeError("age type must be int- type: ",type(age))
    #     if age < 0:
    #         raise ValueError("age must be above 0- age:" ,age)
    #     self._age = age
    # def set_name(self,name:str) -> None:
    #     self._name = name
    # def set_id(self,id:int) -> None:
    #     if type(id) != int:
    #         raise TypeError("id type must be int- type: ",type(id))
    #     self._int = id
    
    # def add_like(self,id:int) -> None:
    #     if type(id) != int:
    #         raise TypeError("id type must be int- type: ",type(id))
    #     if id < 0:
    #         raise ValueError("id must be above 0- id:" ,id)
    #     self._recipes_liked.append(id)
    # def add_view(self,id:int) -> None:
    #     if type(id) != int:
    #         raise TypeError("id type must be int- type: ",type(id))
    #     if id < 0:
    #         raise ValueError("id must be above 0- id:" ,id)
    #     self._recipes_viewed.append(id)
    # def add_make(self,id:int) -> None:
    #     if type(id) != int:
    #         raise TypeError("id type must be int- type: ",type(id))
    #     if id < 0:
    #         raise ValueError("id must be above 0- id:" ,id)
    #     self._recipes_made.append(id)
    # def update_ingredients(self,food:dict) -> None:
    #     for x,count in food.items():
    #         self._ingredients_owned[x] += count
    # def update_weight_matrix(self,weights:list) -> None:
    #     if type(weights) != list:
    #         raise TypeError("type of weights must be list",type(weights))
    #     if len(weights) != 4:
    #         raise ValueError("list must be weight 4- len: ",len(weights))
    #     self._weight_matrix = weights
    
    # #given a list of top ingredients, return a dict that measures favorability of certain ingredients (0-1)
    # #uses inverse tan function to map 0-infinity to 0-1
    # #eg [corn,garlic] = [0.1,0.9]
    # def get_favorability_array(self,relevant_ingredients: list,recipes:DataFrame) -> np.array:
    #     #relevant_ingredients: a list of ingredient (strings) to care about
    #     #recipes: a pandas series of lists of ingredient (strings)
    #     favor = dict.fromkeys(relevant_ingredients,0)
    #     tanfunc = lambda x: np.arctan(x/5)/ (np.pi/2)
    #     for recipe in self._recipes_liked:
    #         query = recipes.query('id ==' + str(recipe))['ingredients']
    #         if len(query) != 1:
    #             raise ValueError("id isn't unique")
    #         for ing in query.iloc()[0]:
    #             if ing in favor:
    #                 favor[ing] += self._weight_matrix[0]
    #     for recipe in self._recipes_made:
    #         query = recipes.query('id ==' + str(recipe))['ingredients']
    #         if len(query) != 1:
    #             raise ValueError("id isn't unique")
    #         for ing in query.iloc()[0]:
    #             if ing in favor:
    #                 favor[ing] += self._weight_matrix[1]
    #     for recipe in self._recipes_viewed:
    #         query = recipes.query('id ==' + str(recipe))['ingredients']
    #         if len(query) != 1:
    #             raise ValueError("id isn't unique")
    #         for ing in query.iloc()[0]:
    #             if ing in favor:
    #                 favor[ing] += self._weight_matrix[2]
    #     for ing in self._ingredients_owned.keys():
    #         if ing in favor:
    #             favor[ing] += self._weight_matrix[3] * self._weight_matrix[3]
    #     return tanfunc(np.fromiter(favor.values(), dtype=float)).astype(float)


