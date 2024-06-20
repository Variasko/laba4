from datetime import datetime, timedelta

from fastapi import *

from sqlalchemy import func
from sqlalchemy.orm import Session

from database import *
from database import engine

app = FastAPI(title='Лабораторная работа №4')

@app.get('/drivers')
def get_drivers():
    with Session(autoflush=False, bind=engine) as db:
        drivers = db.query(Driver).all()
        response = []
        for i in drivers:
            response.append({
                'id':i.id,
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
                'id':i.id,
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
@app.get('/violations')
def get_violations():
    with Session(autoflush=False, bind=engine) as db:
        violations = db.query(Violation).all()
        response = []
        for i in violations:
            response.append({
                'id':i.id,
                'min_fine':i.min_fine,
                'max_fine':i.max_fine,
                'warningNeeded':i.warning_needed,
                'min_suspension':i.min_suspension,
                'max_suspension':i.max_suspension,
                'violationTypeId':i.violation_type_id,
                'violationCode':i.violation_code
            })
        result = {'violations':response}
        return result
@app.get('/fines')
def get_fines():
    with Session(autoflush=False, bind=engine) as db:
        fines = db.query(Fine).all()
        response = []
        for i in fines:
            response.append({
                'id':i.id,
                'violationId':i.violation_id,
                'dateTime':i.date_time,
                'districtId':i.district_id,
                'fineAmount':i.fine_amount,
                'isPaid':i.is_paid,
                'suspensionPeriod':i.suspension_period,
                'inspectorId':i.inspector_id,
                'driverId':i.driver_id
            })
        result = {'fines':response}
        return result

#ЗАДАНИЯ СЛОЖНЕЕ!!!
@app.get('/drivers_with_multiple_cars')
def get_drivers_with_multiple_cars():
    with Session(autoflush=False, bind=engine) as db:
        drivers = db.query(Driver).join(Car).group_by(Driver.id).having(func.count(Car.id) > 1).all()
        response = []
        for driver in drivers:
            response.append({
                'id': driver.id,
                'licenseNumber': driver.licence_number,
                'surname': driver.surname,
                'name': driver.name,
                'registrationAddress': driver.registration_address,
                'phone': driver.phone
            })
        result = {'drivers': response}
        return result
@app.get('/violation_counts')
def get_violation_counts(start_date: str, end_date: str):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    with Session(autoflush=False, bind=engine) as db:
        violation_counts = db.query(Violation.violation_type_id, func.count(Fine.id)).join(Fine).filter(Fine.date_time.between(start_date, end_date)).group_by(Violation.violation_type_id).all()
        response = []
        for violation_count in violation_counts:
            response.append({
                'violationTypeId': violation_count[0],
                'count': violation_count[1]
            })
        result = {'violation_counts': response}
        return result
@app.get('/cars_by_year')
def get_cars_by_year(year: int):
    with Session(autoflush=False, bind=engine) as db:
        cars = db.query(Car).filter(Car.production_year == year).order_by(Car.production_year.desc()).all()
        response = []
        for car in cars:
            response.append({
                'id': car.id,
                'governmentNumber': car.goverment_number,
                'brand': car.brand,
                'model': car.model,
                'color': car.color,
                'productionYear': car.production_year,
                'registrationDate': car.registration_date,
                'driverId': car.driver_id
            })
        result = {'cars': response}
        return result
@app.get('/max_fine_by_violation')
def get_max_fine_by_violation():
    with Session(autoflush=False, bind=engine) as db:
        max_fines = db.query(Violation.violation_type_id, func.max(Violation.max_fine)).group_by(Violation.violation_type_id).all()
        response = []
        for max_fine in max_fines:
            response.append({
                'violationTypeId': max_fine[0],
                'maxFineAmount': max_fine[1]
            })
        result = {'max_fines': response}
        return result
@app.get('/drivers_with_multiple_violations')
def get_drivers_with_multiple_violations():
    with Session(autoflush=False, bind=engine) as db:
        one_month_ago = datetime.now() - timedelta(days=30)
        drivers = db.query(Driver, func.count(Fine.id)).join(Fine).filter(Fine.date_time >= one_month_ago).group_by(Driver.id).having(func.count(Fine.id) > 3).all()
        response = []
        for driver, count in drivers:
            response.append({
                'driverId': driver.id,
                'licenseNumber': driver.license_number,
                'surname': driver.surname,
                'name': driver.name,
                'violationCount': count
            })
        result = {'drivers': response}
        return result
@app.get('/district_with_most_violations')
def get_district_with_most_violations(start_date: str, end_date: str):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    with Session(autoflush=False, bind=engine) as db:
        district = db.query(District, func.count(Fine.id)).join(Fine).filter(Fine.date_time.between(start_date, end_date)).group_by(District.id).order_by(func.count(Fine.id).desc()).first()
        if district:
            response = {
                'districtId': district[0].id,
                'districtName': district[0].name,
                'violationCount': district[1]
            }
            result = {'district': response}
        else:
            result = {'district': None}
        return result
@app.get('/drivers_with_long_suspensions')
def get_drivers_with_long_suspensions():
    with Session(autoflush=False, bind=engine) as db:
        drivers = db.query(Driver).join(Fine).filter(Fine.suspension_period > 180).group_by(Driver.id).having(func.count(Fine.id) > 0).all()
        response = []
        for driver in drivers:
            response.append({
                'id': driver.id,
                'licenseNumber': driver.licence_number,
                'surname': driver.surname,
                'name': driver.name,
                'registrationAddress': driver.registration_address,
                'phone': driver.phone
            })
        result = {'drivers': response}
        return result
@app.get('/total_fine_amount')
def get_total_fine_amount(start_date: str, end_date: str):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    with Session(autoflush=False, bind=engine) as db:
        total_fine_amount = db.query(func.sum(Fine.fine_amount)).filter(Fine.date_time.between(start_date, end_date)).scalar()
        result = {'total_fine_amount': total_fine_amount}
        return result
@app.get('/unpaid_fines_by_driver/{driver_id}')
def get_unpaid_fines_by_driver(driver_id: int):
    with Session(autoflush=False, bind=engine) as db:
        fines = db.query(Fine).filter(Fine.driver_id == driver_id, Fine.is_paid == False).all()
        response = []
        for fine in fines:
            response.append({
                'id': fine.id,
                'violationId': fine.violation_id,
                'dateTime': fine.date_time,
                'districtId': fine.district_id,
                'fineAmount': fine.fine_amount,
                'isPaid': fine.is_paid,
                'suspensionPeriod': fine.suspension_period,
                'inspectorId': fine.inspector_id
            })
        result = {'unpaid_fines': response}
        return result
@app.get('/most_fined_violations')
def get_most_fined_violations():
    with Session(autoflush=False, bind=engine) as db:
        violations = db.query(Violation, func.count(Fine.id)).join(Fine).group_by(Violation.id).order_by(func.count(Fine.id).desc()).all()
        response = []
        for violation, count in violations:
            response.append({
                'violationId': violation.id,
                'violationCode': violation.violation_code,
                'violationName': violation.violation_type.name,
                'fineCount': count
            })
        result = {'most_fined_violations': response}
        return result
@app.post('/new_driver')
def new_driver(ln: int, surname:str, name: str, regAdd: str, phone: str):
    with Session(autoflush=False, bind=engine) as db:
        try:
            new_driver = Driver(licence_number=ln, surname=surname, name=name, registration_address=regAdd, phone=phone)
            db.add(new_driver)
            db.commit()
            return {'status': 200, 'message': 'Новый водитель добавлен'}
        except:
            return {'status': 500, 'message': 'Iternal Server Error'}
@app.post('/new_car')
def new_car(gov_num: str, brand: str, model: str, color:str, prodYear:int, regDate: str, driverId: int):
    with Session(autoflush=False, bind=engine) as db:
        try:
            new_car(goverment_number=gov_num, brand=brand, model=model, color=color, production_year=prodYear, registration_date=regDate, driver_id=driverId)
            db.add(new_car)
            db.commit()
            return {'status': 200, 'message': 'Новый водитель добавлен'}
        except:
            return {'status': 500, 'message': 'Iternal Server Error'}

@app.get('/districts')
def get_districs():
    with Session(autoflush=False, bind=engine) as db:
        districts = db.query(District).all()
        response = []
        for i in districts:
            response.append({
                'id':i.id,
                'name':i.name
            })
        result = {'districts':response}
        return result
@app.post('/new_district')
def new_district(name: str):
    with Session(autoflush=False, bind=engine) as db:
        try:
            new_district = District(name=name)
            db.add(new_district)
            db.commit()
            return {'status' : 200, 'message' : 'Новый район добавлен'}
        except:
            return {'status' : 500, 'message' : 'Iternal Server Error'}
@app.get('/inspectors')
def get_inspectors():
    with Session(autoflush=False, bind=engine) as db:
        inspectors = db.query(Inspector).all()
        response = []
        for i in inspectors:
            response.append({
                'id':i.id,
                'surname':i.surname,
                'name':i.name,
                'service_number':i.service_number
            })
        result = {'inspectors':response}
        return result
@app.post('/new_inspector')
def new_inspector(surname: str, name: str, service_number: int):
    with Session(autoflush=False, bind=engine) as db:
        try:
            new_inspector = Inspector(name=name, surname=surname, service_number=service_number)
            db.add(new_inspector)
            db.commit()
            return {'status': 200, 'message': 'Новый район добавлен'}
        except:
            return {'status': 500, 'message': 'Iternal Server Error'}
@app.get('/violation_types')
def get_violation_types():
    with Session(autoflush=False, bind=engine) as db:
        violation_types = db.query(ViolationType).all()
        response = []
        for i in violation_types:
            response.append({
                'id':i.id,
                'name':i.name
            })
        result = {'violation_types':response}
        return result
@app.post('/new_violation_type')
def new_violation_type(name: str):
    with Session(autoflush=False, bind=engine) as db:
        try:
            new_violation_type = ViolationType(name=name)
            db.add(new_violation_type)
            db.commit()
            return {'status': 200, 'message': 'Новый район добавлен'}
        except:
            return {'status': 500, 'message': 'Iternal Server Error'}