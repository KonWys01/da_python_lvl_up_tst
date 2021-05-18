from sqlalchemy.orm import Session
from sqlalchemy import func
# from . import models
import models, schemas


# Wyklad 5, przyklad
def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )


# Wyklad 5, zadanie 5.1
def get_suppliers(db: Session):
    return db.query(models.Supplier).order_by(models.Supplier.SupplierID).all()


def get_one_supplier(db: Session, supplier_id: int):
    return (
        db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first()
    )


# Wyklad 5, zadanie 5.2
def get_products_with_supplier(db: Session, supplier_id: int):
    return (
        db.query(models.Product).filter(models.Product.SupplierID == supplier_id).order_by(models.Product.ProductID.desc()).all()
    )


# Wyklad 5, zadanie 5.3
def post_suppliers(db: Session, supplier: schemas.SupplierPost):
    id_to_add = db.query(func.max(models.Supplier.SupplierID)).scalar() + 1
    supplier_with_id = models.Supplier(
        SupplierID = id_to_add,
        CompanyName=supplier.CompanyName,
        ContactName=supplier.ContactName,
        ContactTitle=supplier.ContactTitle,
        Address=supplier.Address,
        City=supplier.City,
        PostalCode=supplier.PostalCode,
        Country=supplier.Country,
        Phone=supplier.Phone
    )
    db.add(supplier_with_id)
    db.commit()
    return get_one_supplier(db, supplier_with_id.SupplierID)

