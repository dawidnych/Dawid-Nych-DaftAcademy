from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

router = APIRouter()


@router.get("/suppliers", response_model=List[schemas.Suppliers])
async def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)


@router.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def get_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.get("/suppliers/{supplier_id}/products", response_model=List[schemas.SupplierProduct])
async def get_supplier_product(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    if crud.get_supplier(db, supplier_id) is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db_products = crud.get_supplier_product(db, supplier_id)
    return db_products


@router.post("/suppliers", response_model=schemas.Supplier, status_code=201)
async def post_supplier(new_supplier: schemas.SupplierPost, db: Session = Depends(get_db)):
    db_new_supplier = crud.post_supplier(db, new_supplier)
    return db_new_supplier


@router.put("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def put_supplier(updated_supplier: schemas.SupplierPut, supplier_id: PositiveInt,
                       db: Session = Depends(get_db)):
    db_updated_supplier = crud.put_supplier(db, supplier_id, updated_supplier)
    if db_updated_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_updated_supplier


@router.delete("/suppliers/{supplier_id}", status_code=204)
async def delete_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    if crud.get_supplier(db, supplier_id) is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    crud.delete_supplier(db, supplier_id)
