from fastapi import FastAPI, Path, Response
from typing import Annotated, Union, Optional
from pydantic import UUID4, UUID3, UUID1, BaseModel
from dataclasses import dataclass
from fastapi.responses import JSONResponse
import uuid


app = FastAPI()


app = FastAPI()
students = [
    {
        "name": "john",
        "age": 17,
        "year": "year 12",
        "student_id": uuid.uuid4()
    }
]
print(students[0]["student_id"])

# creating class


@dataclass
class Student(BaseModel):
    name: str
    age: int
    year: str
    student_id: UUID4


@dataclass
class NewStudent(BaseModel):
    name: str
    age: int
    year: str

    student_id: Optional[UUID4] = None


@dataclass
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


# get request


@app.get("/")
def index():
    return students


@app.get("/get-student/{student_id}")
def get_student(student_id: Annotated[UUID4 | None, Path(title="The ID of the student you want to View")]):
    student = list(
        filter(lambda student: student["student_id"] == student_id, students))
    if len(student) == 0:
        return {"Data": "Not found"}
    else:
        return student[0]


@app.get("/get-student-by-name")
# async def get_student_by_name(name: Union[str, None, Path(title="student name")] = None):
async def get_student_by_name(name: str):
    print(name)
    student = list(
        filter(lambda student: student["name"] == name, students))
    # student = [student for student in students if student["name"] == name]
    # print(student)
    if len(student) == 0:
        return {"Data": "Not found"}
    else:
        return student[0]


# # post method


@app.post("/create-student")
def create_student(student: NewStudent):

    student.student_id = uuid.uuid4()

    students.append(student)

    return {"res": 200, "Data": students}


@app.put("/update-student/{student_id}")
def update_student(student_id: UUID4, student: UpdateStudent):
    targetStudent = list(
        filter(lambda student: student["student_id"] == student_id, students))
    print(targetStudent)
    if len(targetStudent) == 0:
        return {'Error': "Student does not exist"}
    if targetStudent[0]["name"] != None:
        targetStudent[0]["name"] = student.name
    if targetStudent[0]["age"] != None:
        targetStudent[0]["age"] = student.age
    if targetStudent[0]["year"] != None:
        targetStudent[0]["year"] = student.year

    return {"res": 200}


@app.delete("/update-student/{student_id}")
def delete_student(student_id: UUID4):
    newStudents = list(
        filter(lambda student: student["student_id"] != student_id, students))
    students.clear()
    print(students, "It is empty")
    for student in newStudents:
        students.append(student)

    return {"res": 200, "data": students}
