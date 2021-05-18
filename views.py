from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

# from . import crud, schemas
import crud, schemas
# from .database import get_db
from database import get_db

router = APIRouter()


# Wyklad 5, przyklad
@router.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shippers(db: Session = Depends(get_db)):
    return crud.get_shippers(db)


# Wyklad 5, zadanie 5.1
@router.get("/suppliers", response_model=List[schemas.Suppliers])
async def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)


@router.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def get_one_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_one_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


# Wyklad 5, zadanie 5.2
@router.get("/suppliers/{supplier_id}/products", response_model=List[schemas.Product])
async def get_products_with_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_product = crud.get_products_with_supplier(db, supplier_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_product
