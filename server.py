import os
import secrets
import re
import sqlite3
from datetime import timedelta
import pycountry
from typing import Dict, Optional, Union, List
from datetime import datetime
from fastapi import FastAPI, Header, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
import uuid
from pydantic import BaseModel

app = FastAPI()

conn = sqlite3.connect('database.sqlite', check_same_thread=False)
cur = conn.cursor()


class SignUpRequestTeacher(BaseModel):
    surname: str
    name: str
    fathername: str
    login: str
    password: str
    subject: str


class SignUpRequestStud(BaseModel):
    surname: str
    name: str
    fathername: str
    clas: str
    login: str
    password: str


class SignInRequest(BaseModel):
    login: str
    password: str


@app.post("/api/teacher/sign-up", tags=["B2B"])
def star(sign_up_request: SignUpRequestTeacher):
    name = sign_up_request.name
    surname = sign_up_request.surname
    fathername = sign_up_request.fathername
    login = sign_up_request.login
    password = sign_up_request.password
    subject = sign_up_request.subject
    patternem = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'
    if len(name) < 2 or len(name) > 30 or len(surname) < 3 or len(surname) > 30 or len(login) < 8 or len(
            login) > 120 or len(password) < 8 or len(
        password) > 30 or " " in password or not re.match(patternem, login):
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Ошибка в данных запроса."
            },
        )
    cur.execute("""SELECT * FROM Teacher WHERE login = ?;""", (login,))
    if cur.fetchone():
        return JSONResponse(
            status_code=409,
            content={
                "status": "error",
                "message": "Такой логин уже зарегистрирован."
            },
        )
    cur.execute("""SELECT * FROM Teacher WHERE name = ? AND surname = ?;""", (name, surname,))
    if cur.fetchone():
        return JSONResponse(
            status_code=409,
            content={
                "status": "error",
                "message": "Такой учитель уже зарегистрирован."
            },
        )
    teach = (surname, name, fathername, login, password, subject)
    cur.execute("""INSERT INTO Teacher (surname, name, fathername, login, password, school_subject)
     VALUES (?, ?, ?, ?, ?, ?);""", teach)

    conn.commit()
    return JSONResponse(
        status_code=201,
        content={
            "message": "Спасибо за регистрацию"
        },
    )


@app.post("/api/student/sign-up", tags=["B2B"])
def student_regayetsya(sign_up_request: SignUpRequestStud):
    name = sign_up_request.name
    surname = sign_up_request.surname
    fathername = sign_up_request.fathername
    login = sign_up_request.login
    password = sign_up_request.password
    clas = sign_up_request.clas
    patternem = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'
    if len(name) < 2 or len(name) > 30 or len(surname) < 3 or len(surname) > 30 or len(login) < 8 or len(
            login) > 120 or len(password) < 8 or len(
        password) > 30 or " " in password or not re.match(patternem, login):
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Ошибка в данных запроса."
            },
        )
    cur.execute("""SELECT * FROM Student WHERE login = ?;""", (login,))
    if cur.fetchone():
        return JSONResponse(
            status_code=409,
            content={
                "status": "error",
                "message": "Такой логин уже зарегистрирован."
            },
        )
    cur.execute("""SELECT * FROM Student WHERE name = ? AND surname = ?;""", (name, surname,))
    if cur.fetchone():
        return JSONResponse(
            status_code=409,
            content={
                "status": "error",
                "message": "Такой ученик уже зарегистрирован."
            },
        )
    stud = (surname, name, fathername, clas, login, password)
    cur.execute("""INSERT INTO Student (surname, name, fathername, class, login, password)
     VALUES (?, ?, ?, ?, ?, ?);""", stud)

    conn.commit()
    return JSONResponse(
        status_code=201,
        content={
            "message": "Спасибо за регистрацию"
        },
    )


@app.get("/api/ping")
def send():
    return {"status": "ok"}


if __name__ == "__main__":
    server_address = os.getenv("SERVER_ADDRESS", "0.0.0.0:8080")  # 127.0.0.1:8080
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))
cur.close()
conn.close()
