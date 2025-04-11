import os
import re
import sqlite3

import qrcode
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel
from qreader import QReader
import cv2

UPLOAD_FOLDER = './uploads'
QR_FOLDER = './qrs'

# Убедитесь, что папка для загрузок существует
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

qreader = QReader()
app = FastAPI()

conn = sqlite3.connect('database.sqlite', check_same_thread=False)
cur = conn.cursor()


class ForCameras(BaseModel):
    place: str


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


def generate_qr(data, filename):
    qr = qrcode.QRCode(
        version=1,  # Размер QR-кода (1 — наименьший, 40 — наибольший)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Высокий уровень коррекции ошибок
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)


def QRscan(filepath):
    image = cv2.cvtColor(cv2.imread(filepath), cv2.COLOR_BGR2RGB)
    return qreader.detect_and_decode(image=image)


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
def qrcodicki(sign_up_request: SignUpRequestStud):
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
    # qr code
    cur.execute("""INSERT INTO Student (surname, name, fathername, class, login, password)
     VALUES (?, ?, ?, ?, ?, ?);""", stud)

    conn.commit()
    cur.execute("""SELECT * FROM Student WHERE name = ? AND surname = ?;""", (name, surname,))
    id = cur.fetchone()[0]
    filename = os.path.join(QR_FOLDER, f"{id}_qr.png")  # Полный путь к файлу
    generate_qr(id, filename)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Спасибо за регистрацию"
        },
    )


@app.post("/api/getQR", tags=["B2B"])
def qrcodicki(sign_up_request: SignInRequest):
    login = sign_up_request.login
    password = sign_up_request.password
    patternem = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'
    if len(login) > 120 or len(password) < 8 or len(password) > 30 or " " in password or not re.match(patternem, login):
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Ошибка в данных запроса."
            },
        )
    cur.execute("""SELECT * FROM Student WHERE login = ?;""", (login,))
    if not cur.fetchone():
        return JSONResponse(
            status_code=409,
            content={
                "status": "error",
                "message": "На этот логин никто не зарегестрирован"
            },
        )
    cur.execute("""SELECT * FROM Student WHERE login = ? AND password = ?;""", (login, password,))
    id = cur.fetchone()[0]
    if not id:
        return JSONResponse(
            status_code=409,
            content={
                "status": "error",
                "message": "Неправильный пароль."
            },
        )
    filename = f"{id}_qr"
    if not os.path.exists(filename):
        filename = os.path.join(QR_FOLDER, f"{id}_qr.png")
        generate_qr(id, filename)
    return JSONResponse(
        status_code=200,
        content={
            "message": filename
        },
    )


@app.post("/api/upload")
async def upload_file(place: str = Form(...), file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    students = QRscan(filepath)
    for id in students:
        if place[11:-2] == "Столовая":
            cur.execute("""UPDATE School_attendance SET lunch = 1 WHERE id = ?;""", (id,))
        elif place[11:-2] == "Вход":
            cur.execute("""UPDATE School_attendance SET come = 1 WHERE id = ?;""", (id,))
        elif place[11:-2] == "Выход":
            cur.execute("""UPDATE School_attendance SET out = 1 WHERE id = ?;""", (id,))
        conn.commit()

    return {"message": "Данные обновлены"}


@app.get("/api/ping")
def send():
    return {"status": "ok"}


if __name__ == "__main__":
    server_address = "127.0.0.1:8080"  # 127.0.0.1:8080
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))
cur.close()
conn.close()
