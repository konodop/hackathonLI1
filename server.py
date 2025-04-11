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


class SignUpRequest(BaseModel):
    surname: str
    name: str
    fathername: str
    login: str
    password: str
    subject: str


class SignInRequest(BaseModel):
    email: str
    password: str


class other(BaseModel):
    age: int
    country: str


class PatchUser(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    avatar_url: Optional[str] = None
    password: Optional[str] = None


class PatchPromo(BaseModel):
    description: Optional[str] = None
    image_url: Optional[str] = None
    target: Optional[Dict[str, Union[str, int, List[str]]]] = None
    max_count: Optional[int] = None
    active_from: Optional[str] = None
    active_until: Optional[str] = None


class PromoRequest(BaseModel):
    description: str
    image_url: Optional[str] = None
    target: Dict[str, Union[str, int, List[str]]]
    max_count: int
    active_from: Optional[str] = None
    active_until: Optional[str] = None
    mode: str
    promo_common: Optional[str] = None
    promo_unique: Optional[List[str]] = None


class SignUpRequestUser(BaseModel):
    name: str
    surname: str
    email: str
    avatar_url: str = None
    other: other
    password: str


def tim(date):
    try:
        if " " in date:
            return False
        datetime.fromisoformat(date.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


@app.post("/api/teacher/sign-up", tags=["B2B"])
def star(sign_up_request: SignUpRequest):
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




#
#
# @app.post("/api/business/auth/sign-in", tags=["B2B"])
# def star(sign_in_request: SignInRequest):
#     email = sign_in_request.email
#     password = sign_in_request.password
#     pattern = r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
#     patternem = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'
#     if len(email) < 8 or len(email) > 120 or len(password) < 8 or len(
#             password) > 60 or not re.match(pattern, password) or not re.match(patternem, email):
#         return JSONResponse(
#             status_code=400,
#             content={
#                 "status": "error",
#                 "message": "Ошибка в данных запроса."
#             },
#         )
#     cur.execute("""SELECT password FROM companies WHERE email = %s;""", (email,))
#     row = cur.fetchone()
#     if not row:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "status": "error",
#                 "message": "Неверный email или пароль."
#             },
#         )
#     if password != row[0]:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "status": "error",
#                 "message": "Неверный email или пароль."
#             },
#         )
#
#     tok = str(secrets.token_urlsafe(64))
#     cur.execute("""SELECT * FROM companies WHERE token = %s;""", (tok,))
#     while cur.fetchone():
#         tok = str(secrets.token_urlsafe(64))
#         cur.execute("""SELECT * FROM companies WHERE token = %s;""", (tok,))
#     cur.execute("""UPDATE companies SET token = %s WHERE email = %s""", (tok, email))
#     conn.commit()
#     return JSONResponse(
#         status_code=200,
#         content={
#             "token": tok,
#         },
#     )
#
#
# @app.exception_handler(RequestValidationError)
# def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=400,
#         content={
#             "status": "error",
#             "message": "Bad request"
#         },
#     )
#
#
# @app.post("/api/business/promo", tags=["B2B"])
# def star(promo_request: PromoRequest, authorization: Optional[str] = Header(None)):
#     if not authorization:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "status": "error",
#                 "message": "Пользователь не авторизован."
#             },
#         )
#     if promo_request.mode != "COMMON" and promo_request.mode != "UNIQUE":
#         return JSONResponse(
#             status_code=400,
#             content={
#                 "status": "error",
#                 "message": "Не верный режим."
#             },
#         )
#     cur.execute("""SELECT * FROM companies WHERE token = %s;""", (authorization.split()[-1],))
#     target = promo_request.target
#     flag = 1
#     country = None
#     if "country" in target:
#         flag = 2
#         country = target["country"]
#         if not any(c.alpha_2 == country.upper() for c in pycountry.countries):
#             flag = 0
#     comp = cur.fetchone()
#     if not comp:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "status": "error",
#                 "message": "Пользователь не авторизован."
#             },
#         )
#     compid = comp[0]
#     name = comp[1]
#     descr = promo_request.description
#     maxcount = promo_request.max_count
#     if 10 <= len(descr) <= 300 and 0 <= maxcount < 100000000 and flag:
#         aurl = promo_request.image_url
#         urlpattern = r'^(https?://)([a-z0-9-]+.)+[a-z]{2,6}(:d+)?(/[^s]*)?$'
#         if aurl is not None:
#             if not re.match(urlpattern, aurl):
#                 return JSONResponse(
#                     status_code=400,
#                     content={
#                         "status": "error",
#                         "message": "Не верная ссылка."
#                     },
#                 )
#
#         guid = str(uuid.uuid4())
#         targ = promo_request.target
#         agefr = None
#         if "age_from" in targ:
#             agefr = int(targ["age_from"])
#         ageuntil = None
#         if "age_until" in targ:
#             ageuntil = int(targ["age_until"])
#         cats = None
#         if "categories" in targ:
#             cats = targ["categories"]
#         mode = promo_request.mode
#         actfr = promo_request.active_from
#         actuntil = promo_request.active_until
#         if agefr and ageuntil:
#             if agefr > ageuntil:
#                 return JSONResponse(
#                     status_code=400,
#                     content={
#                         "status": "error",
#                         "message": "Не верный возраст."
#                     },
#                 )
#         com = promo_request.promo_common
#         uni = promo_request.promo_unique
#         current_time = datetime.now()
#         if actfr:
#             if not tim(actfr):
#                 return JSONResponse(
#                     status_code=400,
#                     content={
#                         "status": "error",
#                         "message": "Не верная дата."
#                     },
#                 )
#             active_from_dt = datetime.fromisoformat(actfr)
#         else:
#             if actuntil:
#                 if not tim(actuntil):
#                     return JSONResponse(
#                         status_code=400,
#                         content={
#                             "status": "error",
#                             "message": "Не верная дата."
#                         },
#                     )
#             active_from_dt = current_time
#         q = 0
#         if actuntil:
#             q = 1
#             active_until_dt = datetime.fromisoformat(actuntil)
#         diff = timedelta(seconds=600)
#         if actuntil and actfr:
#             diff = active_from_dt - active_until_dt
#         active = False
#         if diff.total_seconds() > 0:
#
#             if active_from_dt <= current_time and ((mode == "COMMON" and maxcount > 0) or
#                                                    (mode == "UNIQUE" and len(uni) > 0)):
#                 active = True
#             if q:
#                 if current_time > active_from_dt:
#                     active = False
#         prom = (descr, aurl, agefr, ageuntil, country, cats, maxcount, actfr, actuntil, mode, com, uni, guid, compid,
#                 name, 0, 0, active)
#         cur.execute(
#             """INSERT INTO promos (description, image_url, age_from, age_until, country, categories, max_count,
#              active_from, active_until, mode, promo_common, promo_unique, promo_id, company_id, company_name, like_count
#              , used_count, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
#             prom)
#         conn.commit()
#         return JSONResponse(
#             status_code=201,
#             content={
#                 "id": guid,
#             },
#         )
#     else:
#         return JSONResponse(
#             status_code=400,
#             content={
#                 "status": "error",
#                 "message": "Ошибка в данных запроса."
#             },
#         )
#
#
# @app.get("/api/business/promo/{promoid}", tags=["B2B"])
# def star(promoid: str, authorization: Optional[str] = Header(None)):
#     if not authorization:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "status": "error",
#                 "message": "Пользователь не авторизован."
#             },
#         )
#     cur.execute("""SELECT id FROM companies WHERE token = %s;""", (authorization.split()[-1],))
#     if not 30 < len(promoid) < 40:
#         return JSONResponse(
#             status_code=400,
#             content={
#                 "status": "error",
#                 "message": "Ошибка в данных запроса."
#             },
#         )
#     comp = cur.fetchone()
#     if not comp:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "status": "error",
#                 "message": "Пользователь не авторизован."
#             },
#         )
#     cur.execute("""SELECT * FROM promos WHERE promo_id = %s;""", (promoid,))
#     promo = cur.fetchone()
#     if not promo:
#         return JSONResponse(
#             status_code=404,
#             content={
#                 "status": "error",
#                 "message": "Промокод не найден."
#             },
#         )
#     if not promo[13] == comp[0]:
#         return JSONResponse(
#             status_code=403,
#             content={
#                 "status": "error",
#                 "message": "Промокод не принадлежит этой компании."
#             },
#         )
#     promo_dict = {col.name: value for col, value in zip(cur.description, promo) if value is not None and
#                   col.name != 'active' and col.name != "company_id"}
#     response_content = {
#         'description': promo_dict.get('description'),
#         'image_url': promo_dict.get('image_url'),
#         'target': {
#             'country': promo_dict.get('country'),
#             'categories': promo_dict.get('categories'),
#             'age_from': promo_dict.get('age_from'),
#             'age_until': promo_dict.get('age_until')
#         },
#         'max_count': promo_dict.get('max_count'),
#         'active_from': promo_dict.get('active_from'),
#         'active_until': promo_dict.get('active_until'),
#         'mode': promo_dict.get('mode'),
#         'promo_common': promo_dict.get('promo_common'),
#         'promo_unique': promo_dict.get('promo_unique'),
#         'promo_id': promo_dict.get('promo_id'),
#         'company_name': promo_dict.get('company_name'),
#         'like_count': promo_dict.get('like_count'),
#         'used_count': promo_dict.get('used_count'),
#     }
#     response_content['target'] = {k: v for k, v in response_content['target'].items() if v is not None}
#     response_content = {k: v for k, v in response_content.items() if v is not None}
#     return JSONResponse(
#         status_code=200,
#         content=response_content,
#     )
#
#
# @app.patch("/api/business/promo/{promoid}", tags=["B2B"])
# def star(patchpromo: PatchPromo, promoid: str, authorization: Optional[str] = Header(None)):
#     if not authorization:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "status": "error",
#                 "message": "Пользователь не авторизован."
#             },
#         )
#     cur.execute("""SELECT * FROM promos WHERE promo_id = %s;""", (promoid,))
#     promo = cur.fetchone()
#     cur.execute("""SELECT id FROM companies WHERE token = %s;""", (authorization.split()[-1],))
#     if not 30 < len(promoid) < 40:
#         return JSONResponse(
#             status_code=400,
#             content={
#                 "status": "error",
#                 "message": "Ошибка в данных запроса."
#             },
#         )
#     comp = cur.fetchone()
#     if not comp:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "status": "error",
#                 "message": "Пользователь не авторизован."
#             },
#         )
#     if not promo:
#         return JSONResponse(
#             status_code=404,
#             content={
#                 "status": "error",
#                 "message": "Промокод не найден."
#             },
#         )
#
#     if not promo[13] == comp[0]:
#         return JSONResponse(
#             status_code=403,
#             content={
#                 "status": "error",
#                 "message": "Промокод не принадлежит этой компании."
#             },
#         )
#     description = patchpromo.description
#     df = 0
#     image_url = patchpromo.image_url
#     iu = 0
#     target = patchpromo.target
#     max_count = patchpromo.max_count
#     mc = 0
#     active_from = patchpromo.active_from
#     af = 0
#     active_until = patchpromo.active_until
#     au = 0
#     a = 0
#     co = 0
#     cat = 0
#     agf = 0
#     agu = 0
#     if description is not None:
#         if not 10 <= len(description) <= 300:
#             return JSONResponse(
#                 status_code=400,
#                 content={
#                     "status": "error",
#                     "message": "Ошибка в данных запроса."
#                 },
#             )
#         df = 1
#     if image_url is not None:
#         urlpattern = r'^(https?://)([a-z0-9-]+.)+[a-z]{2,6}(:d+)?(/[^s]*)?$'
#         if not re.match(urlpattern, image_url):
#             return JSONResponse(
#                 status_code=400,
#                 content={
#                     "status": "error",
#                     "message": "Не верная ссылка."
#                 },
#             )
#         iu = 1
#     if active_from is not None:
#         if not tim(active_from):
#             return JSONResponse(
#                 status_code=400,
#                 content={
#                     "status": "error",
#                     "message": "Не верная дата."
#                 },
#             )
#         af = 1
#     if active_until is not None:
#         if not tim(active_until):
#             return JSONResponse(
#                 status_code=400,
#                 content={
#                     "status": "error",
#                     "message": "Не верная дата."
#                 },
#             )
#         au = 1
#     if max_count is not None:
#         if max_count > 1 and promo[9] == "UNIQUE" or max_count < 0 or max_count > 100000000:
#             return JSONResponse(
#                 status_code=400,
#                 content={
#                     "status": "error",
#                     "message": "Не верное количество."
#                 },
#             )
#         mc = 1
#     if active_from is not None or active_until is not None:
#         current_time = datetime.now()
#         if active_from:
#             active_from_dt = datetime.fromisoformat(active_from)
#         else:
#             active_from_dt = current_time
#         q = 0
#         if active_until:
#             q = 1
#             active_until_dt = datetime.fromisoformat(active_until)
#         diff = timedelta(seconds=600)
#         if active_until and active_from:
#             diff = active_from_dt - active_until_dt
#         active = False
#         if diff.total_seconds() > 0:
#
#             if active_from_dt <= current_time:
#                 active = True
#             if q:
#                 if current_time > active_from_dt:
#                     active = False
#         a = 1
#     if target is not None:
#         country = target.get('country')
#         categories = target.get('categories')
#         age_from = target.get('age_from')
#         age_until = target.get('age_until')
#         if age_from and age_until:
#             if age_from > age_until:
#                 return JSONResponse(
#                     status_code=400,
#                     content={
#                         "status": "error",
#                         "message": "Не верный возраст."
#                     },
#                 )
#         if country is not None:
#             if not len(country) == 2:
#                 return JSONResponse(
#                     status_code=400,
#                     content={
#                         "status": "error",
#                         "message": "Не верный код страны."
#                     },
#                 )
#             co = 1
#         if categories is not None:
#             if len(categories) == 0 or len(categories) > 20:
#                 return JSONResponse(
#                     status_code=400,
#                     content={
#                         "status": "error",
#                         "message": "Не верный таргет."
#                     },
#                 )
#             for cat in categories:
#                 print(cat, len(cat))
#                 if not 20 >= len(cat) >= 2:
#                     return JSONResponse(
#                         status_code=400,
#                         content={
#                             "status": "error",
#                             "message": "Не верный таргет."
#                         },
#                     )
#             cat = 1
#         if age_from is not None:
#             if not 0 <= age_from <= 100:
#                 return JSONResponse(
#                     status_code=400,
#                     content={
#                         "status": "error",
#                         "message": "Не верный таргет."
#                     },
#                 )
#             agf = 1
#         if age_until is not None:
#             if not 0 <= age_until <= 100:
#                 return JSONResponse(
#                     status_code=400,
#                     content={
#                         "status": "error",
#                         "message": "Не верный таргет."
#                     },
#                 )
#             agu = 1
#     if df:
#         cur.execute("""UPDATE promos SET description = %s WHERE promo_id = %s""", (description, promoid))
#         conn.commit()
#     if iu:
#         cur.execute("""UPDATE promos SET image_url = %s WHERE promo_id = %s""", (image_url, promoid))
#         conn.commit()
#     if af:
#         cur.execute("""UPDATE promos SET active_from = %s WHERE promo_id = %s""", (active_from, promoid))
#         conn.commit()
#     if au:
#         cur.execute("""UPDATE promos SET active_until = %s WHERE promo_id = %s""", (active_until, promoid))
#         conn.commit()
#     if a:
#         cur.execute("""UPDATE promos SET active = %s WHERE promo_id = %s""", (active, promoid))
#         conn.commit()
#     if mc:
#         cur.execute("""UPDATE promos SET max_count = %s WHERE promo_id = %s""", (max_count, promoid))
#         conn.commit()
#     if co:
#         cur.execute("""UPDATE promos SET country = %s WHERE promo_id = %s""", (country, promoid))
#         conn.commit()
#     if cat:
#         cur.execute("""UPDATE promos SET categories = %s WHERE promo_id = %s""", (categories, promoid))
#         conn.commit()
#     if agf:
#         cur.execute("""UPDATE promos SET age_from = %s WHERE promo_id = %s""", (age_from, promoid))
#         conn.commit()
#     if agu:
#         cur.execute("""UPDATE promos SET age_until = %s WHERE promo_id = %s""", (age_until, promoid))
#         conn.commit()
#
#     cur.execute("""SELECT * FROM promos WHERE promo_id = %s;""", (promoid,))
#     promo = cur.fetchone()
#     promo_dict = {col.name: value for col, value in zip(cur.description, promo) if value is not None}
#     response_content = {
#         'description': promo_dict.get('description'),
#         'image_url': promo_dict.get('image_url'),
#         'target': {
#             'country': promo_dict.get('country'),
#             'categories': promo_dict.get('categories'),
#             'age_from': promo_dict.get('age_from'),
#             'age_until': promo_dict.get('age_until')
#         },
#         'max_count': promo_dict.get('max_count'),
#         'active_from': promo_dict.get('active_from'),
#         'active_until': promo_dict.get('active_until'),
#         'mode': promo_dict.get('mode'),
#         'promo_common': promo_dict.get('promo_common'),
#         'promo_unique': promo_dict.get('promo_unique'),
#         'promo_id': promo_dict.get('promo_id'),
#         'company_id': promo_dict.get('company_id'),
#         'company_name': promo_dict.get('company_name'),
#         'like_count': promo_dict.get('like_count'),
#         'used_count': promo_dict.get('used_count'),
#         'active': promo_dict.get('active')
#     }
#     response_content['target'] = {k: v for k, v in response_content['target'].items() if v is not None}
#     response_content = {k: v for k, v in response_content.items() if v is not None}
#     return JSONResponse(
#         status_code=200,
#         content=response_content,
#     )
#
#
# @app.post("/api/user/auth/sign-up", tags=["B2C"])
# def auth(sign_up_requestuser: SignUpRequestUser):
#     name = sign_up_requestuser.name
#     surname = sign_up_requestuser.surname
#     email = sign_up_requestuser.email
#     password = sign_up_requestuser.password
#     age, country = sign_up_requestuser.other
#     age = age[1]
#     country = country[1]
#     aurl = sign_up_requestuser.avatar_url
#     pattern = r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
#     patternem = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'
#     urlpattern = r'^(https?://)([a-z0-9-]+.)+[a-z]{2,6}(:d+)?(/[^s]*)?$'
#     if aurl is not None:
#         if not re.match(urlpattern, aurl):
#             return JSONResponse(
#                 status_code=400,
#                 content={
#                     "status": "error",
#                     "message": "Не верная ссылка."
#                 },
#             )
#     if (len(name) < 1 or len(name) > 100 or len(surname) < 1 or len(surname) > 120 or
#         len(email) < 8 or len(email) > 120 or len(password) < 8 or len(password) > 60 or
#         not re.match(pattern, password)) or not re.match(patternem, email) or not any(c.alpha_2 == country.upper()
#                                                                                       for c in pycountry.countries):
#         return JSONResponse(
#             status_code=400,
#             content={
#                 "status": "error",
#                 "message": "Ошибка в данных запроса."
#             },
#         )
#     cur.execute("""SELECT * FROM users WHERE email = %s;""", (email,))
#     if cur.fetchone():
#         return JSONResponse(
#             status_code=409,
#             content={
#                 "status": "error",
#                 "message": "Такой email уже зарегистрирован."
#             },
#         )
#     tok = str(secrets.token_urlsafe(64))
#     cur.execute("""SELECT * FROM users WHERE token = %s;""", (tok,))
#     while cur.fetchone():
#         tok = str(secrets.token_urlsafe(64))
#         cur.execute("""SELECT * FROM users WHERE token = %s;""", (tok,))
#     user = (name, surname, email, age, country, password, tok)
#     cur.execute("""INSERT INTO users (name, surname, email, age, country, password, token) VALUES
#      (%s, %s, %s, %s, %s, %s, %s);""", user)
#
#     conn.commit()
#     return JSONResponse(
#         status_code=200,
#         content={
#             "token": tok,
#         },
#     )
#
#
# @app.post("/api/user/auth/sign-in", tags=["B2C"])
# def star(sign_in_request: SignInRequest):
#     email = sign_in_request.email
#     password = sign_in_request.password
#     pattern = r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
#     patternem = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'
#     if len(email) < 8 or len(email) > 120 or len(password) < 8 or len(
#             password) > 60 or not re.match(pattern, password) or not re.match(patternem, email):
#         return JSONResponse(
#             status_code=400,
#             content={
#                 "status": "error",
#                 "message": "Ошибка в данных запроса."
#             },
#         )
#     cur.execute("""SELECT password FROM users WHERE email = %s;""", (email,))
#     row = cur.fetchone()
#     if not row:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "status": "error",
#                 "message": "Неверный email или пароль."
#             },
#         )
#     if password != row[0]:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "status": "error",
#                 "message": "Неверный email или пароль."
#             },
#         )
#
#     tok = str(secrets.token_urlsafe(64))
#     cur.execute("""SELECT * FROM users WHERE token = %s;""", (tok,))
#     while cur.fetchone():
#         tok = str(secrets.token_urlsafe(64))
#         cur.execute("""SELECT * FROM users WHERE token = %s;""", (tok,))
#     cur.execute("""UPDATE users SET token = %s WHERE email = %s""", (tok, email))
#     conn.commit()
#     return JSONResponse(
#         status_code=200,
#         content={
#             "token": tok,
#         },
#     )
#
#
# @app.get("/api/user/profile", tags=["B2C"])
# def star(authorization: Optional[str] = Header(None)):
#     if not authorization:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "status": "error",
#                 "message": "Пользователь не авторизован."
#             },
#         )
#     cur.execute("""SELECT * FROM users WHERE token = %s;""", (authorization.split()[-1],))
#
#     usr = cur.fetchone()
#     if not usr:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "status": "error",
#                 "message": "Пользователь не авторизован."
#             },
#         )
#     usrdict = {col.name: value for col, value in zip(cur.description, usr) if value is not None}
#     response_content = {
#         'name': usrdict.get('name'),
#         'surname': usrdict.get('surname'),
#         'email': usrdict.get('email'),
#         'avatar_url': usrdict.get('avatar_url'),
#         'other': {
#             'age': usrdict.get('age'),
#             'country': usrdict.get('country'),
#         }
#     }
#     return JSONResponse(
#         status_code=200,
#         content=response_content,
#     )
#
#
# @app.patch("/api/user/profile", tags=["B2C"])
# def star(patchuser: PatchUser, authorization: Optional[str] = Header(None)):
#     if not authorization:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "status": "error",
#                 "message": "Пользователь не авторизован."
#             },
#         )
#     tok = (authorization.split()[-1],)
#     cur.execute("""SELECT * FROM users WHERE token = %s;""", tok)
#
#     usr = cur.fetchone()
#     if not usr:
#         return JSONResponse(
#             status_code=401,
#             content={
#                 "status": "error",
#                 "message": "Пользователь не авторизован."
#             },
#         )
#     name = patchuser.name
#     surname = patchuser.surname
#     avatar_url = patchuser.avatar_url
#     password = patchuser.password
#     pa = 0
#     na = 0
#     su = 0
#     au = 0
#     if password is not None:
#         pattern = r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
#         if len(password) > 60 or not re.match(pattern, password):
#             return JSONResponse(
#                 status_code=400,
#                 content={
#                     "status": "error",
#                     "message": "Ошибка в данных запроса."
#                 },
#             )
#         pa = 1
#     if name is not None:
#         if not 1 <= len(name) <= 100:
#             return JSONResponse(
#                 status_code=400,
#                 content={
#                     "status": "error",
#                     "message": "Ошибка в данных запроса."
#                 },
#             )
#         na = 1
#     if surname is not None:
#         if not 1 <= len(surname) <= 120:
#             return JSONResponse(
#                 status_code=400,
#                 content={
#                     "status": "error",
#                     "message": "Ошибка в данных запроса."
#                 },
#             )
#         su = 1
#     if avatar_url is not None:
#         urlpattern = r'^(https?://)([a-z0-9-]+.)+[a-z]{2,6}(:d+)?(/[^s]*)?$'
#         if not re.match(urlpattern, avatar_url):
#             return JSONResponse(
#                 status_code=400,
#                 content={
#                     "status": "error",
#                     "message": "Не верная ссылка."
#                 },
#             )
#         au = 1
#
#     if pa:
#         cur.execute("""UPDATE users SET password = %s WHERE token = %s""", (password, tok))
#         conn.commit()
#     if na:
#         cur.execute("""UPDATE users SET name = %s WHERE token = %s""", (name, tok))
#         conn.commit()
#     if su:
#         cur.execute("""UPDATE users SET surname = %s WHERE token = %s""", (surname, tok))
#         conn.commit()
#     if au:
#         cur.execute("""UPDATE users SET avatar_url = %s WHERE token = %s""", (avatar_url, tok))
#         conn.commit()
#     cur.execute("""SELECT * FROM users WHERE token = %s;""", (tok,))
#
#     usr = cur.fetchone()
#     usrdict = {col.name: value for col, value in zip(cur.description, usr) if value is not None}
#     response_content = {
#         'name': usrdict.get('name'),
#         'surname': usrdict.get('surname'),
#         'email': usrdict.get('email'),
#         'avatar_url': usrdict.get('avatar_url'),
#         'other': {
#             'age': usrdict.get('age'),
#             'country': usrdict.get('country'),
#         }
#     }
#     return JSONResponse(
#         status_code=200,
#         content=response_content,
#     )


@app.get("/api/ping")
def send():
    return {"status": "ok"}


if __name__ == "__main__":
    server_address = os.getenv("SERVER_ADDRESS", "0.0.0.0:8080")  # 127.0.0.1:8080
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))
cur.close()
conn.close()
