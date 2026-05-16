from pydantic import BaseModel, Field
from typing import Annotated, Optional


class Notes(BaseModel):
    id:Annotated[str, Field(..., description="Note ID", examples=['N001'])]
    title:Annotated[str, Field(..., min_length=3, max_length=100,description="Title of note")]
    content:Annotated[str, Field(..., description="Content of note")]
    category:Annotated[str, Field(..., description="Category of note")]
    author:Annotated[str, Field(..., description="Author of the note")]
    completed:Annotated[bool, Field( default=False,description="Completion status of note")]

class Updated_notes(BaseModel):
    title:Annotated[str, Optional, Field(description="Note title")]
    content:Annotated[str, Optional, Field( description="Note content")]
    category:Annotated[str, Optional, Field(description="Note category")]
    author:Annotated[str, Optional, Field(description="Author of the note")]
    completed:Annotated[bool, Optional, Field(description="Completion status of node")]
