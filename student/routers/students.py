from fastapi import APIRouter, Depends, status, HTTPException,Response
from sqlalchemy.orm import Session
from .. import schemas,models
from ..database import get_db
import json
from typing import Optional

router = APIRouter(
    prefix="/students",
    tags=['Student']
)


# @router.get("",response_model=list[schemas.ShowDetail],status_code=status.HTTP_200_OK)
# def show_all(db: Session = Depends(get_db)):
#     student = db.query(models.Student).all()
#     return student

@router.post("",status_code=status.HTTP_201_CREATED)
def create_student(request: schemas.Details,db: Session = Depends(get_db)):
    store = request.model_dump_json()
    store = json.loads(store)
    # print(store)
    payload = {}
    if store.get("name"):
        if "name" in store.keys() and store["name"] is not None and store["name"] != "string":
            payload["name"] = store.get("name")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Please give the valid name")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Please provide name also")
        
    if store.get("age"):
        if "age" in store.keys() and store["age"] is not None and store["age"] > 1:
            payload["age"] = store.get("age")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Please give the valid age")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Please provide age also")
    print(payload)
    
    if store.get("address"):
        address_payload = {}
        if store["address"]["city"]:
            if "city" in store["address"] and store["address"]["city"] != "string" and store["address"]["city"] is not None:
                address_payload["city"] = store["address"]["city"]
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Please give the valid city")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Please give the valid city also")
            
        if store["address"]["country"]:
            if "country" in store["address"] and store["address"]["country"] != "string" and store["address"]["country"] is not None:
                address_payload["country"] = store["address"]["country"]
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Please give the valid country")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Please give the valid country also")
        print(address_payload)
    
    new_address = models.Address(city=address_payload["city"], country=address_payload["country"])
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    
    new_student = models.Student(name=payload["name"],age=payload["age"],address_id=new_address.id)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    response = {
        "name": new_student.name,
        "age": new_student.age,
        "address": {
            "city": new_address.city,
            "country": new_address.country
        }
    }
    return response

@router.get("",response_model=schemas.StudentListResponse,status_code=status.HTTP_200_OK)
def list_student(country: Optional[str] = None, age: Optional[int] = None, db: Session = Depends(get_db)):
    student = db.query(models.Student).join(models.Address)
    
    if country:
        student = student.filter(models.Address.country == country)
    
    if age != None:
        student = student.filter(models.Student.age >= age)
    
    students = student.all()
    
    if not students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No students found matching the given filters")
    
    
    return {"data": students}

@router.get("/{id}",response_model=schemas.ShowDetail,status_code=status.HTTP_200_OK)
def fetch_student(id: int,db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Student with id no {id} is not present in the db')
    return student


@router.delete("/{id}",status_code=status.HTTP_200_OK)
def destroy(id: int,db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} is already not available in the db")
    db.delete(student)
    db.commit()
    return "Deleted"



@router.patch("/{id}",response_model=schemas.ShowDetail,status_code=status.HTTP_200_OK)
def update_student(id: int, request: schemas.ShowDetail, db: Session = Depends(get_db)):
    store = request.model_dump_json()
    store = json.loads(store)
    # print(store)

    payload = {}
    if "name" in store.keys() and store["name"] is not None and store["name"] != "string":
        payload["name"] = store.get("name")
        
    if "age" in store.keys() and store["age"] is not None and store["age"] > 1:
        payload["age"] = store.get("age")
    

    if store.get("address"):
        address_payload = {}
        if "city" in store["address"] and store["address"]["city"] != "string" and store["address"]["city"] is not None:
            address_payload["city"] = store["address"]["city"]

        if "country" in store["address"] and store["address"]["country"] != "string" and store["address"]["country"] is not None:
            address_payload["country"] = store["address"]["country"]

        if address_payload:
            student = db.query(models.Student).filter(models.Student.id == id).first()
            if not student:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
            
            address = student.address
            if not address:
                address = models.Address()
                db.add(address)
                db.commit()

            for key, value in address_payload.items():
                setattr(address, key, value)

            db.commit()
            db.refresh(address)

        if address_payload:
            payload["address_id"] = address.id

    # print(payload)

    student_query = db.query(models.Student).filter(models.Student.id == id)
    student = student_query.first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    if payload:
        student_query.update(payload)
        db.commit()
        db.refresh(student)

    return student

