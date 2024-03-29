from pydantic import BaseModel, PositiveInt, constr
from typing import Optional


class Shipper(BaseModel):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)

    class Config:
        orm_mode = True


class Suppliers(BaseModel):
    SupplierID: PositiveInt
    CompanyName: Optional[str]

    class Config:
        orm_mode = True


class Supplier(BaseModel):
    SupplierID: PositiveInt
    CompanyName: Optional[str]
    ContactName: Optional[str]
    ContactTitle: Optional[str]
    Address: Optional[str]
    City: Optional[str]
    Region: Optional[str]
    PostalCode: Optional[str]
    Country: Optional[str]
    Phone: Optional[str]
    Fax: Optional[str]
    HomePage: Optional[str]

    class Config:
        orm_mode = True
