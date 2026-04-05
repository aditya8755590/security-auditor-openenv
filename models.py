from pydantic import BaseModel
from typing import List, Optional

class Observation(BaseModel):
    current_directory: str
    available_files: List[str]
    file_content_view: str  
    bugs_flagged_count: int 
    system_message: str     

class Action(BaseModel):
    command: str 
    target: str 

class StepResponse(BaseModel):
    observation: Optional[Observation]
    reward: float
    done: bool