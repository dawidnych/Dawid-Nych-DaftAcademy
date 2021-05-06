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
    app.db_connection.row_factory = sqlite3.Row
    customers = app.db_connection.execute("""
    SELECT CustomerID, CompanyName, Address, PostalCode, City, Country FROM Customers
    ORDER BY CustomerID
    """).fetchall()
    # customers = app.db_connection.execute("""
    # SELECT CustomerID, CompanyName, IFNULL(Address, '') Address, IFNULL(PostalCode, '') PostalCode,
    # IFNULL(City, '') City, IFNULL(Country, '') Country FROM Customers
    # ORDER BY CustomerID
    # """).fetchall()

    return {"customers": [{"id": x['CustomerID'], "name": x['CompanyName'], "full_address":
        f"{x['Address']} {x['PostalCode']} {x['City']} {x['Country']}"} for x in customers]}


def product_ids():
    ids = app.db_connection.execute("SELECT ProductID FROM Products").fetchall()
    lst = []
    for id in ids:
        for value in id:
            lst.append(value)
    return lst


@app.get("/products/{id}")
async def products(id: int):
    product_id_lst = product_ids()
    if id in product_id_lst:
        app.db_connection.row_factory = sqlite3.Row
        product = app.db_connection.execute("SELECT ProductID, ProductName FROM Products "
                                            "WHERE ProductID = :id", {'id': id}).fetchone()
        json = {"id": product['ProductID'], "name": product['ProductName']}
        return JSONResponse(content=json)
    else:
        raise HTTPException(status_code=404)
