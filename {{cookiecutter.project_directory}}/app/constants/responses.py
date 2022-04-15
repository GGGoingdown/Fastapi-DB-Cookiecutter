from typing import Mapping, Any, Dict, Union

# Generic schema
from app.schemas import GenericSchema

GET_USER_4XX_RESPONSES: Mapping[Union[str, int], Dict[str, Any]] = {
    401: {
        "model": GenericSchema.DetailResponse,
        "description": "Could not validate credentials",
    },
    403: {
        "model": GenericSchema.DetailResponse,
        "description": "Not enough permissions",
    },
}
