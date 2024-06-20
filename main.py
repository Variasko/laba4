from fastapi import *
from database import *
from sqlalchemy.orm import Session

from models import *
from database import engine

app = FastAPI(title='Лабораторная работа №4')

@app.get('/drivers')
def get_drivers():
    with Session(autoflush=False, bind=engine) as db:
        drivers = db.query(Driver).all()
        response = []
        for i in drivers:
            response.append({
                'LN':i.licence_number,
                'surname':i.surname,
                'name':i.name,
                'registrationAddress':i.registration_address,
                'phone':i.phone
            })
        result = {'drivers':response}
        return result

@app.get('/cars')
def get_cars():
    with Session(autoflush=False, bind=engine) as db:
        cars = db.query(Car).all()
        response = []
        for i in cars:
            response.append({
                'GN':i.goverment_number,
                'brand':i.brand,
                'model':i.model,
                'color':i.color,
                'prodYear':i.production_year,
                'regDate':i.registration_date,
                'driverId':i.driver
            })
        result = {'cars':response}
        return result

