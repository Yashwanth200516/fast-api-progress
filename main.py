from fastapi import FastAPI,HTTPException
from models import Students
from database import collection

app=FastAPI()




@app.get('/')
def home():
    return {'message':'home page'}

@app.get("/students")
def get_students():
    student_list=[]
    for student in collection.find():
        student["_id"]=str(student["_id"])
        student_list.append(student)
    return student_list

@app.get('/students/{student_id}')
def get_student_by_id(student_id:str):
    student=collection.find_one({'usn':student_id.upper()})
    if student:
        student['_id']=str(student['_id'])
        return student
    raise HTTPException(
        status_code=404,
        detail='student not found'
    )

@app.post('/add-student')
def add_student(student:Students):
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

@app.delete('/students/{student_id}')
def delete_student(student_id:str):
    result=collection.delete_one({'usn':student_id.upper()})
    if result.deleted_count==1:
        return {'detail':'student deleted sucessfully'}
    
    raise HTTPException(
        status_code=404,
        detail='student not found'
    )

@app.put('/students/{student_id}')
def update_student(student_id: str, student: Students):
    student.name = student.name.title()
    student.usn = student.usn.upper()
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