from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app= FastAPI()
models.Base.metadata.create_all(bind=engine)

class EmployeeBase(BaseModel):
    name: str
    email: str
    no_hp: str
    alamat: str
    divisi_id: int

class DivisiBase(BaseModel):
    divisi : str

class ResponseMessage(BaseModel):
    message: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/pegawai/", status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeBase, db: db_dependency):
    db_pegawai = models.Employee(**employee.dict())
    db.add(db_pegawai)
    db.commit()
    return JSONResponse(content={"message": "Add new employee success"}, status_code=status.HTTP_201_CREATED)

@app.put("/pegawai/{no_pegawai}", status_code=status.HTTP_202_ACCEPTED)
async def update_employee(no_pegawai: int, employee: EmployeeBase, db: db_dependency):
    db_pegawai = db.query(models.Employee).filter(models.Employee.no_pegawai == no_pegawai).first()
    if db_pegawai is None:
        raise HTTPException(status_code=404, detail='Pegawai tidak ditemukan')

    # Update the employee record with the new data
    for key, value in employee.dict(exclude_unset=True).items():
        setattr(db_pegawai, key, value)

    db.commit()
    return JSONResponse(content={"message": "Update employee success"}, status_code=status.HTTP_202_ACCEPTED)


@app.delete("/pegawai/{no_pegawai}",status_code=status.HTTP_200_OK)
async def delete_employee(no_pegawai: int, db: db_dependency):
    db_pegawai = db.query(models.Employee).filter(models.Employee.no_pegawai==no_pegawai).first()
    if db_pegawai is None :
        raise HTTPException(status_code=404, detail='Pegawai tidak ditemukan')
    db.delete(db_pegawai)
    db.commit()
    return JSONResponse(content={"message": "Delete employee success"}, status_code=status.HTTP_200_OK)

@app.get("/pegawai/",status_code=status.HTTP_200_OK)
async def read_employee(db: db_dependency):
    result = db.query(models.Employee, models.Divisi).join(models.Divisi).all()
    if result is None :
        raise HTTPException(status_code=404, detail='Tidak ada pegawai ditemukan')
    employee_list = []
    for employee, divisi in result:
        employee_data = {
            "no_pegawai": employee.no_pegawai,
            "no_hp": employee.no_hp,
            "divisi": divisi.divisi if divisi else None,
            "email": employee.email,
            "name": employee.name,
            "alamat": employee.alamat,
        }
        employee_list.append(employee_data)

    return employee_list

@app.get("/pegawai/{no_pegawai}",status_code=status.HTTP_200_OK)
async def read_employee(no_pegawai: int, db: db_dependency):
    employee = db.query(models.Employee).filter(models.Employee.no_pegawai==no_pegawai).first()
    if employee is None :
        raise HTTPException(status_code=404, detail='Pegawai tidak ditemukan')
    return employee

@app.get("/pegawai/divisi/{divisi}", status_code=status.HTTP_200_OK)
async def read_divisi(divisi_id:int, db:db_dependency):
    result = db.query(models.Employee, models.Divisi).join(models.Divisi).filter(models.Employee.divisi_id == divisi_id).all()
    if result is None :
        raise HTTPException(status_code=404, detail='Tidak ada pegawai ditemukan')
    employee_list = []
    for employee, divisi in result:
        employee_data = {
            "no_pegawai": employee.no_pegawai,
            "no_hp": employee.no_hp,
            "divisi": divisi.divisi if divisi else None,
            "email": employee.email,
            "name": employee.name,
            "alamat": employee.alamat,
        }
        employee_list.append(employee_data)

    return employee_list

@app.post("/divisi/",status_code=status.HTTP_201_CREATED)
async def create_divisi(divisi: DivisiBase, db: db_dependency):
    db_divisi = models.Divisi(**divisi.dict())
    db.add(db_divisi)
    db.commit()

@app.get("/divisi/",status_code=status.HTTP_200_OK)
async def read_divisi(db: db_dependency):
    divisi = db.query(models.Divisi).all()
    if divisi is None :
        raise HTTPException(status_code=404, detail='Tidak ada divis ditemukan')
    return divisi

