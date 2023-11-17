from pydantic import BaseModel

this ensures that the data conforms to the specified types and rules, automatically validates data, allows specifying of default value for attributes as seen in the post(basemodel) class, pydantic-specific features. 
schema/pydantic models define the structure of a request & response which ensures that when a user wants to create a post, the request only goes through if there is a title and content

orm_mode = true will ensure the pydantic model reads the data even if it is not a dictionary

import List from typing to allow response_model for get_posts to be List(schemas.Post) since the return is a list

Base in models.py is a requirement to work any sql model

utils.py is used to store all the hashing logic