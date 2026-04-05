from pydantic import BaseModel
from typing import List, Optional

# What the AI "Sees"
class Observation(BaseModel):
    current_directory: str
    available_files: List[str]
    file_content_view: str  
    bugs_flagged_count: int 
    system_message: str     

# What the AI can "Do"
class Action(BaseModel):
    command: str 
    target: str 

# The response sent back after every step
class StepResponse(BaseModel):
    observation: Optional[Observation]
    reward: float
    done: bool