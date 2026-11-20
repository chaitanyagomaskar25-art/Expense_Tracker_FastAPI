from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator,
    model_validator,
    ConfigDict
)

from datetime import date as Date
from enum import Enum
from typing import Literal


# Reusable types

class ExpenseCategory(str, Enum):
    FOOD = "Food"
    TRAVEL = "Travel"
    SHOPPING = "Shopping"
    BILLS = "Bills"
    ENTERTAINMENT = "Entertainment"


ExpenseStatus = Literal["Pending", "Completed", "Failed"]


# Nested models

class User(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


# Common expense model

class ExpenseBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    user: User

    title: str = Field(
        min_length=2,
        max_length=100
    )

    amount: float = Field(gt=0)

    status: ExpenseStatus = "Pending"

    category: ExpenseCategory

    date: Date = Field(default_factory=Date.today)

    notes: str | None = Field(default=None, max_length=500)

    paid: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")

        return value.strip()

    @model_validator(mode="after")
    def check_payment_status(self):
        if self.status == "Completed" and not self.paid:
            raise ValueError(
                "Completed expenses must be marked as paid"
            )

        return self


# Request models

class ExpenseCreate(ExpenseBase):
    pass


class UserUpdate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    ) 

    email: EmailStr | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Name cannot contain only spaces")

        return value.strip() if value is not None else value


class ExpenseUpdate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    user: UserUpdate | None = None

    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    amount: float | None = Field(default=None, gt=0)

    status: ExpenseStatus | None = None

    category: ExpenseCategory | None = None

    date: Date | None = None

    notes: str | None = Field(default=None, max_length=500)

    paid: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Title cannot be empty")

        return value.strip() if value is not None else value


class ExpenseReplace(ExpenseBase):
    status: ExpenseStatus
    date: Date
    paid: bool 


# Response models

class ExpenseResponse(ExpenseBase):
    id: str


class ExpenseListResponse(BaseModel):
    expenses: list[ExpenseResponse]


class ExpenseDetailResponse(BaseModel):
    data: ExpenseResponse


class ExpenseMutationResponse(BaseModel):
    message: str
    data: ExpenseResponse


class MessageResponse(BaseModel):
    message: str


# Report response model

class StatisticsResponse(BaseModel):
    total: float
    average: float
    highest: float
    count: int
