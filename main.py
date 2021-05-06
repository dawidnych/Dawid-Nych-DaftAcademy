import sqlite3

from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import HTMLResponse

from typing import List

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

    return {"customers": [{"id": x['CustomerID'], "name": x['CompanyName'], "full_address":
        " ".join(f"{x['Address']} {x['PostalCode']} {x['City']} {x['Country']}".split())} for x in customers]}
