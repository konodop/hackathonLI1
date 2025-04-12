import os
import sqlite3
from datetime import datetime

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
    tg_id: str
    subject: str


class SignUpRequestStud(BaseModel):
    surname: str
    name: str
    fathername: str
    clas: str
    tg_id: str


class SignInRequest(BaseModel):
    tg_id: str


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
    tg_id = sign_up_request.tg_id
    subject = sign_up_request.subject
    if len(name) < 2 or len(name) > 30 or len(surname) < 3 or len(surname) > 30:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Ошибка в данных запроса."
            },
        )
    cur.execute("""SELECT * FROM Teacher WHERE tg_id = ?;""", (tg_id,))
    if cur.fetchone():
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Такой аккаунт уже зарегистрирован."
            },
        )
    cur.execute("""SELECT * FROM Teacher WHERE name = ? AND surname = ?;""", (name, surname,))
    if cur.fetchone():
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Такой учитель уже зарегистрирован."
            },
        )
    teach = (surname, name, fathername, tg_id, subject)
    cur.execute("""INSERT INTO Teacher (surname, name, fathername, tg_id, school_subject)
     VALUES (?, ?, ?, ?, ?);""", teach)

    conn.commit()
    return JSONResponse(
        status_code=201,
        content={
            "message": "Спасибо за регистрацию"
        },
    )


@app.post("/api/vospit/sign-up", tags=["B2B"])
def star(sign_up_request: SignUpRequestTeacher):
    name = sign_up_request.name
    surname = sign_up_request.surname
    fathername = sign_up_request.fathername
    tg_id = sign_up_request.tg_id
    if len(name) < 2 or len(name) > 30 or len(surname) < 3 or len(surname) > 30:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Ошибка в данных запроса."
            },
        )
    cur.execute("""SELECT * FROM Abuy WHERE tg_id = ?;""", (tg_id,))
    if cur.fetchone():
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Такой аккаунт уже зарегистрирован."
            },
        )
    cur.execute("""SELECT * FROM Abuy WHERE name = ? AND surname = ?;""", (name, surname,))
    if cur.fetchone():
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Такой воспитатель уже зарегистрирован."
            },
        )
    vospit = (surname, name, fathername, tg_id)
    cur.execute("""INSERT INTO Abuy (surname, name, fathername, tg_id)
     VALUES (?, ?, ?, ?);""", vospit)

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
    tg_id = sign_up_request.tg_id
    clas = sign_up_request.clas
    if len(name) < 2 or len(name) > 30 or len(surname) < 3 or len(surname) > 30:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Ошибка в данных запроса."
            },
        )
    cur.execute("""SELECT * FROM Student WHERE tg_id = ?;""", (tg_id,))
    if cur.fetchone():
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Такой аккаунт уже зарегистрирован."
            },
        )
    cur.execute("""SELECT * FROM Student WHERE name = ? AND surname = ?;""", (name, surname,))
    if cur.fetchone():
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Такой ученик уже зарегистрирован."
            },
        )
    stud = (surname, name, fathername, clas, tg_id)
    # qr code
    cur.execute("""INSERT INTO Student (surname, name, fathername, class, tg_id)
     VALUES (?, ?, ?, ?, ?);""", stud)

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


@app.post("/api/profile", tags=["B2B"])
def prof(sign_up_request: SignInRequest):
    tg_id = sign_up_request.tg_id
    print(tg_id)
    cur.execute("""SELECT * FROM Student WHERE tg_id = ?;""", (tg_id,))
    stud = cur.fetchone()
    if stud:
        return JSONResponse(
            status_code=200,
            content={
                "message": "ученик"
            },
        )
    cur.execute("""SELECT * FROM Teacher WHERE tg_id = ?;""", (tg_id,))
    teach = cur.fetchone()
    if teach:
        return JSONResponse(
            status_code=200,
            content={
                "message": "учитель"
            },
        )
    cur.execute("""SELECT * FROM Parent WHERE tg_id = ?;""", (tg_id,))
    par = cur.fetchone()
    if par:
        return JSONResponse(
            status_code=200,
            content={
                "message": "родитель"
            },
        )
    cur.execute("""SELECT * FROM Abuy WHERE tg_id = ?;""", (tg_id,))
    vosp = cur.fetchone()
    if vosp:
        return JSONResponse(
            status_code=200,
            content={
                "message": "воспитатель"
            },
        )
    else:
        return JSONResponse(
            status_code=403,
            content={
                "message": "Не зарегестрирован"
            },
        )


@app.post("/api/getQR", tags=["B2B"])
def qrcodicki(sign_up_request: SignInRequest):
    tg_id = sign_up_request.tg_id
    print(tg_id)
    cur.execute("""SELECT * FROM Student WHERE tg_id = ?;""", (tg_id,))
    id = cur.fetchone()
    if not id:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "На этот аккаунт никто не зарегестрирован"
            },
        )
    filename = os.path.join(QR_FOLDER, f"{id[0]}_qr.png")
    generate_qr(id, filename)
    return JSONResponse(
        status_code=200,
        content={
            "message": filename.replace("\\", "/")
        },
    )


@app.get("/api/skips")
async def skips():
    skip = "00:00:00"
    cur.execute("""SELECT id FROM School_attendance WHERE come = ?;""", (skip,))
    s = cur.fetchall()
    parents = []
    for id in s:
        cur.execute("""SELECT tg_id FROM Parent WHERE son = ?;""", (id[0],))
        parent = cur.fetchone()
        parents.append(parent)
    return JSONResponse(
        status_code=200,
        content={
            "message": parents
        },
    )


@app.get("/api/dorm")
async def indor():
    cur.execute("""SELECT tg_id FROM School_attendance WHERE at_boarding_school = 1;""")
    s = cur.fetchall()
    students = []
    for i in s:
        students.append(id[0])
    return JSONResponse(
        status_code=200,
        content={
            "message": students
        },
    )


@app.post("/api/upload")
async def upload_file(place: str = Form(...), file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    students = QRscan(filepath)
    if place == "Учитель":
        return {"message": students}
    else:
        now = datetime.now().strftime("%H:%M:%S")
        for id_ in students:
            id = int(id_[1:-1].split(", ")[0])
            print(id, id_)
            if place[11:-2] == "Столовая":
                cur.execute(f"""UPDATE School_attendance SET lunch = '{now}' WHERE id = ?;""", (id,))
            elif place[11:-2] == "Вход":
                cur.execute(f"""UPDATE School_attendance SET come = '{now}' WHERE id = ?;""", (id,))
            elif place[11:-2] == "Выход":
                cur.execute(f"""UPDATE School_attendance SET out = '{now}' WHERE id = ?;""", (id,))
            elif place[11:-2] == "Интернат Вход":
                cur.execute(f"""UPDATE School_attendance SET at_boarding_school = 1 WHERE id = ?;""", (id,))
            elif place[11:-2] == "Интернат Выход":
                cur.execute(f"""UPDATE School_attendance SET at_boarding_school = 0 WHERE id = ?;""",
                            (id,))
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
