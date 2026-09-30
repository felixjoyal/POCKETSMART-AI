from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.-]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=1, max_length=128)

class HomeRequest(BaseModel):
    budget: int = Field(gt=0, le=10_000_000)
    rooms: list[str] = Field(default_factory=list, max_length=10)
    lights: int = Field(default=0, ge=0, le=100)
    fans: int = Field(default=0, ge=0, le=100)
    furniture_items: int = Field(default=0, ge=0, le=100)
    style: str = Field(default="Modern", max_length=100)
    notes: str = Field(default="", max_length=1000)

class PartyRequest(BaseModel):
    budget: int = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=10000)
    event_type: str = Field(default="Birthday", max_length=100)
    venue_type: str = Field(default="Indoor", max_length=100)
    catering: bool = True
    decoration: bool = True
    entertainment: bool = True
    notes: str = Field(default="", max_length=1000)

class JewelryRequest(BaseModel):
    budget: int = Field(gt=0, le=10_000_000)
    occasion: str = Field(default="Wedding", max_length=100)
    style: str = Field(default="Elegant", max_length=100)
    preferences: str = Field(default="", max_length=1000)

class RecommendationItem(BaseModel):
    name: str
    category: str
    description: str
    estimated_price: float = Field(ge=0)
    quantity: int = Field(default=1, ge=1)
    platform: str
    search_query: str
    reason: str
    url: str | None = None

class RecommendationSection(BaseModel):
    category: str
    allocation: float = Field(ge=0)
    items: list[RecommendationItem] = Field(default_factory=list)

class RecommendationResponse(BaseModel):
    planner_type: Literal["home", "party", "jewelry"]
    title: str
    budget: float = Field(ge=0)
    estimated_total: float = Field(ge=0)
    remaining_budget: float = Field(ge=0)
    summary: str
    sections: list[RecommendationSection]
    tips: list[str] = Field(default_factory=list)
    disclaimer: str = "Prices and availability are estimates. Verify current details on the linked platform."

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
