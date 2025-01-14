from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional,List


@dataclass
class UserCreate:
    username: str
    email: str
    password: str


@dataclass
class User:
    id: int
    username: str
    email: str
    created_at: datetime


@dataclass
class CategoryCreate:
    name: str
    description: Optional[str] = None


@dataclass
class Category:
    id: int
    name: str
    description: Optional[str] = None


@dataclass
class ExpenseCreate:
    description: str
    amount: Decimal
    date: datetime
    category_name: str


@dataclass
class Expense:
    id: int
    description: str
    amount: Decimal
    date: datetime
    category_id: int
    owner_id: int
    created_at: datetime

class ExpenseResponse:
    id: int
    description: str
    amount: Decimal
    date: datetime
    category_name: str

class ExpensesResponse:
    expenses: List[ExpenseResponse]
@dataclass
class IncomeCreate:
    description: str
    amount: Decimal
    date: datetime


@dataclass
class Income:
    id: int
    description: str
    amount: Decimal
    date: datetime
    owner_id: int
    created_at: datetime


@dataclass
class BudgetCreate:
    amount: Decimal
    start_date: datetime
    end_date: datetime


@dataclass
class Budget:
    id: int
    amount: Decimal
    start_date: datetime
    end_date: datetime
    owner_id: int
    created_at: datetime
