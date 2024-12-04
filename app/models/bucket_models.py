from typing import Optional, List
from pydantic import BaseModel

class AWS(BaseModel):
    name:                               str
    region:                             str                     = 'us-east-1'
    acl:                                Optional[str]           = 'private'
    versioning:                         Optional[bool]          = False
    encryption:                         Optional[str]           = None 
    logging:                            Optional[bool]          = False
    logging_bucket:                     Optional[str]           = None
    lifecycle:                          Optional[List[dict]]    = None
    block_public:                       Optional[bool]          = True
    access_key:                         str
    secret_key:                         str