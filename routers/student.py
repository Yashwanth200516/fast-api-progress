from fastapi import APIRouter,HTTPException,Depends
from database import collection
from models import Students
from utils.jwt_handler import get_current_user

router=APIRouter()

@router.get("/students")
def get_students(current_user=Depends(get_current_user)):
    student_list=[]
    for student in collection.find():
        student["_id"]=str(student["_id"])
        student_list.append(student)
    return student_list

@router.get('/students/{student_id}')
def get_student_by_id(student_id:str,current_user=Depends(get_current_user)):
    student=collection.find_one({'usn':student_id.upper()})
    if student:
        student['_id']=str(student['_id'])
        return student
    raise HTTPException(
        status_code=404,
        detail='student not found'
    )

@router.post('/students')
def add_student(student:Students,current_user=Depends(get_current_user)):
    existing = collection.find_one(
    {"usn": student.usn.upper()}
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="USN already exists"
        )
    student.name=student.name.title()
    student.usn=student.usn.upper()
    student.address=student.address.title()
    collection.insert_one(student.model_dump())
    return{'detail':'student added successfully'}

@router.delete('/students/{student_id}')
def delete_student(student_id:str,current_user=Depends(get_current_user)):
    result=collection.delete_one({'usn':student_id.upper()})
    if result.deleted_count==1:
        return {'detail':'student deleted sucessfully'}
    
    raise HTTPException(
        status_code=404,
        detail='student not found'
    )

@router.put('/students/{student_id}')
def update_student(student_id: str, student: Students,current_user=Depends(get_current_user)):
    student.name = student.name.title()
    student.usn = student_id.upper()#usn cant change it should be unique
    student.address = student.address.title()
    result = collection.update_one(
        {'usn': student_id.upper()},
        {'$set': student.model_dump()}
    )

    if result.matched_count==1:
        return {'detail': 'student updated successfully'}

    raise HTTPException(
        status_code=404,
        detail='student not found'
    )