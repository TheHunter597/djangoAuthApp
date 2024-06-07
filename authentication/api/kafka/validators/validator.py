from enum import Enum
import os
import json
from jsonschema import validate
from authentication.exceptions.bad_request import BadRequest

with open(os.path.join("authentication","api","kafka","validators","userCreatedSchema.json")) as f:
    UserCreatedSchema= json.load(f)

with open(os.path.join("authentication","api","kafka","validators","userUpdatedSchema.json")) as f:
    UserUpdatedSchema= json.load(f)

with open(os.path.join("authentication","api","kafka","validators","userDeletedSchema.json")) as f:
    UserDeletedSchema= json.load(f)
class SchemaType(Enum):
    UserCreatedSchemaType={
        "type":"userCreated",
        "value":UserCreatedSchema
    }
    UserUpdatedSchemaType={
        "type":"userUpdated",
        "value":UserUpdatedSchema
    }
    UserDeletedSchemaType={
        "type":"userDeleted",
        "value":UserDeletedSchema
    }
    @classmethod
    def validate(self,data,type):
        try:
            if self.UserCreatedSchemaType.value["type"] == type:
                validate(data,self.UserCreatedSchemaType.value["value"])
            else :
                raise BadRequest({"message":"Please enter valid schema to validate against in validate function"})
        except Exception as e:
            raise BadRequest({"message":"Validating Schema error","errors":e})