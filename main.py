from uuid import UUID

from fastapi import FastAPI, Response
from pydantic import BaseModel


def is_valid_uuid(uuid_to_test, version=4):
    """
    function taken from stack overflow: https://stackoverflow.com/questions/19989481/how-to-determine-if-a-string-is-a-valid-v4-uuid
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """

    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


class Key(BaseModel):
    key: str


app = FastAPI()


kv_store = {}
with open("data.txt", "r") as f:
    data = f.readlines()
    for line in data:
        split_line = line.split()
        kv_store[split_line[0]] = " ".join(split_line[1:])
import sys

print("size of kv_store: ", sys.getsizeof(kv_store))


@app.post("/get_value")
async def get_value(key: Key, response: Response):
    """
    Return the value for given uuid4 key

    args:
        key (BaseModel): Data model that defines the request fields. Only value is key, which is the
            uuid
        response (Response): used to change the response code when the uuid is invalid or not found in db
    returns:
        dict: return value with key value, for successful request, else return a dict with key "message" with information about the failure.
    """
    ## Directions specifically point out the key must be a uuid version 4
    if not is_valid_uuid(key.key):
        ## Change code to 400 to make it clear they didn't get a value back, but they can update and try again
        response.status_code = 400
        return {
            "message": f"provided key '{key}' is not a valud uuid. All keys should be a valid uuid (version 4)"
        }

    value = kv_store.get(key.key)
    if value is None:
        ## Change code to 400 to make it clear they didn't get a value back, but they can update and try again
        response.status_code = 400
        return {
            "message": f"uuid '{key}' not found in db. Please update and try again."
        }
    return {"value": value}
