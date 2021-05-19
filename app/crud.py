from sqlalchemy.orm import Session
from sqlalchemy import update, delete

from . import models
from .schemas import SupplierPost, SupplierPut


def get_suppliers(db: Session):
    return db.query(models.Supplier).order_by(models.Supplier.SupplierID).all()


def get_supplier(db: Session, supplier_id: int):
    return db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first()


def get_supplier_product(db: Session, supplier_id: int):
    return db.query(models.Product).join(models.Category).filter(
        models.Product.SupplierID == supplier_id).order_by(models.Product.ProductID.desc()).all()


def post_supplier(db: Session, new_supplier: SupplierPost):
    new_id = db.query(models.Supplier).count()+1
    output = models.Supplier(SupplierID=new_id, CompanyName=new_supplier.CompanyName,
                             ContactName=new_supplier.ContactName,
                             ContactTitle=new_supplier.ContactTitle, Address=new_supplier.Address,
                             City=new_supplier.City,
                             PostalCode=new_supplier.PostalCode,
                             Country=new_supplier.Country,
                             Phone=new_supplier.Phone)
    db.add(output)
    db.commit()
    return output


def put_supplier(db: Session, supplier_id: int, supplier_updated: SupplierPut):
    tmp_dict = {key: value for key, value in supplier_updated.dict().items() if value is not None}
    if bool(tmp_dict):
        db.execute(update(models.Supplier).where(models.Supplier.SupplierID == supplier_id).values(
            **tmp_dict))
        db.commit()
    return get_supplier(db, supplier_id)


def delete_supplier(db: Session, supplier_id: int):
    db.execute(delete(models.Supplier).where(models.Supplier.SupplierID == supplier_id))
    db.commit()
