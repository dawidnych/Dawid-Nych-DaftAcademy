import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional


app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/categories")
async def categories():
    app.db_connection.row_factory = sqlite3.Row
    categories = app.db_connection.execute("""
    SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID
    """).fetchall()
    return {"categories": [{"id": x['CategoryID'], "name": x['CategoryName']} for x in categories]}


@app.get("/customers")
async def customers():
    app.db_connection.row_factory = sqlite3.Row
    customers = app.db_connection.execute("""
    SELECT CustomerID, CompanyName, IFNULL(Address, '') Address, IFNULL(PostalCode, '') PostalCode,
    IFNULL(City, '') City, IFNULL(Country, '') Country FROM Customers
    ORDER BY CAST(CustomerID as INTEGER)
    """).fetchall()
    return {"customers": [{"id": x['CustomerID'], "name": x['CompanyName'], "full_address":
        f"{x['Address']} {x['PostalCode']} {x['City']} {x['Country']}"} for x in customers]}


@app.get("/products/{id}")
async def products(id: int):
    app.db_connection.row_factory = sqlite3.Row
    product = app.db_connection.execute("SELECT ProductID, ProductName FROM Products "
                                        "WHERE ProductID = :id", {'id': id}).fetchone()
    if product:
        json = {"id": product['ProductID'], "name": product['ProductName']}
        return JSONResponse(content=json)
    raise HTTPException(status_code=404)


@app.get("/employees")
async def employees(limit: Optional[int] = -1, offset: Optional[int] = 0, order: str = "EmployeeID"):
    if order != "EmployeeID":
        if order == "first_name":
            order = "FirstName"
        elif order == "last_name":
            order = "LastName"
        elif order == "city":
            order = "City"
        else:
            raise HTTPException(status_code=400)

    app.db_connection.row_factory = sqlite3.Row
    employees = app.db_connection.execute(f"""
    SELECT EmployeeID, LastName, FirstName, City FROM Employees
    ORDER BY {order}
    LIMIT {limit} OFFSET {offset}
    """).fetchall()

    return {"employees": [{"id": x['EmployeeID'], "last_name": x['LastName'], "first_name":
        x['FirstName'], "city": x['City']} for x in employees]}


@app.get("/products_extended")
async def products_extended():
    app.db_connection.row_factory = sqlite3.Row
    employees = app.db_connection.execute("""
       SELECT Products.ProductID, Products.ProductName, Categories.CategoryName, 
       Suppliers.CompanyName FROM Products
       JOIN Categories ON Products.CategoryID = Categories.CategoryID
       JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID
       ORDER BY Products.ProductID
       """).fetchall()
    return {"products_extended": [{"id": x['ProductID'], "name": x['ProductName'], "category":
        x['CategoryName'], "supplier": x['CompanyName']} for x in employees]}
