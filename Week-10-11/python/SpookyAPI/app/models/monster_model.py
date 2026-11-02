from typing import Annotated

from pydantic import BaseModel, Field, SecretStr


# Just like in Java, this Class will MODEL a Monster and its data

# BUT we're using something called Pydantic for structure and data validation
# (Notice the use of Annotated and Field for constraints)

# Inherit from BaseModel to get the Pydantic functionality
class MonsterModel(BaseModel):
    # This field must be greate than 0
    id: Annotated[int, Field(gt=0)]
    # This field must be between 8 and 30 characters long
    name: Annotated[str, Field(min_length=8, max_length=30)]
    # This field will be hidden when this object is returned,
    # and can be optional ( = none)
    motive: Annotated[SecretStr, Field()] = None