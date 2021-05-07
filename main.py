import sqlite3

from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import JSONResponse


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
    # I. Jeśli wartość = null dodaje ją jako None do adresu:
    app.db_connection.row_factory = sqlite3.Row
    # customers = app.db_connection.execute("""
    #     SELECT CustomerID, CompanyName, Address, PostalCode, City, Country FROM Customers
    #     ORDER BY CustomerID
    #     """).fetchall()

    # II. Jeśli któraś wartość = null, zastępuje ją pustym stringiem
    # app.db_connection.row_factory = sqlite3.Row
    customers = app.db_connection.execute("""
    SELECT CustomerID, CompanyName, IFNULL(Address, '') Address, IFNULL(PostalCode, '') PostalCode,
    IFNULL(City, '') City, IFNULL(Country, '') Country FROM Customers
    ORDER BY CustomerID
    """).fetchall()

    # III. Daje null jako adres, jeśli jedna z wartości jest null:
    # customers = app.db_connection.execute("""
    # SELECT CustomerID, CompanyName, Address || ' ' || PostalCode || ' ' || City || ' ' || Country
    # AS FullAddress FROM Customers
    # ORDER BY CustomerID
    # """).fetchall()

    return {"customers": [{"id": x['CustomerID'], "name": x['CompanyName'], "full_address":
        # ad I i II:
        f"{x['Address']} {x['PostalCode']} {x['City']} {x['Country']}"} for x in
                          customers]}
        # ad III:
        # x['FullAddress']} for x in customers]}


@app.get("/products/{id}")
async def products(id: int):
    app.db_connection.row_factory = sqlite3.Row
    product = app.db_connection.execute("SELECT ProductID, ProductName FROM Products "
                                        "WHERE ProductID = :id", {'id': id}).fetchone()
    if product:
        json = {"id": product['ProductID'], "name": product['ProductName']}
        return JSONResponse(content=json)
    raise HTTPException(status_code=404)
