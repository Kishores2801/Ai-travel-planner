from pydantic import BaseModel, Field, field_validator
from typing import Literal, List,Optional
from prompt_builder import check_city_affordability
# Class Travel Plan Requests
class TravelPlanRequest(BaseModel):
    destination: str = Field(..., min_length=2) # Destination that they are planning visit
    days : int = Field(..., le=90, gt=0) # No of days that they want to be there
    month : str = Field(..., min_length=3) # Preferred month that they are planning to travel
    budget_range: int = Field(..., gt=500) # Budget willing to spend excluding air fare
    people_count : int = Field(..., gl=1) # no of people in trip
    trip_type : Literal["Solo", 'Family', 'Friends', 'Couple'] # Trip type
    interests: List[str] = Field(default_factory=list)
    accommodation_type: Literal["hotel", "hostel", "airbnb", "resort", "free accommodation"] = "hotel"
    dietary_restrictions: Optional[List[str]] = None
    near_city_interest : bool = False # Near City in Interest



    # “Before saving values for destination and month, run this function to clean/validate them”
    @field_validator("destination", "month")
    @classmethod
    def normalize_strings(cls, value : str) -> str:
        return value.strip().lower()

    # Validation is use to validate budget
    @model_validator(mode='after')
    def check_budget_feasibility(self) -> 'TravelPlanRequest':
        daily_pp_budget = self.budget_range / (self.days * self.people_count)
        
        if not check_city_affordability(city=self.destination, daily_budget=daily_pp_budget, trip_type=self.trip_type):
            raise ValueError(f"The ${daily_pp_budget} is insufficient for {self.destination}.")
        return self




