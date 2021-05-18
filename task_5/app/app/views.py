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
async def get_supplier(supplier_id=PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier
