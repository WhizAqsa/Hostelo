from fastapi import APIRouter, Body, Depends, Request
from mysql.connector import connect, Error
from decouple import config # type: ignore

mess_router = APIRouter()

########################################################

from decouple import config # type: ignore
from mysql.connector import connect, Error

try:
    connection = connect(
        host = config("mySQLServerIP"),
        user = config("apiUserName"),
        password = config("apiPassword")
    )
except Error as e:
    print(e)

cursor = connection.cursor() # type: ignore
cursor.execute("USE Hostelo")

print("Connected to MySQL Server")

########################################################

@mess_router.get("/mess-off-students", tags=["Mess"])
async def get_mess_off_students(request: Request):
    cursor.execute(f"SELECT `student_id`,`name`,`room_number`, DATE_ADD(end_date, INTERVAL 1 DAY) FROM `student` NATURAL JOIN `messoff` WHERE `end_date` > CURRENT_DATE() ORDER BY `end_date` DESC")
    result = cursor.fetchall()
    if result != None:
        return{
                "status": True,
                "msg": "Retrieval successful",
                "data": {
                    "students": result
                }
        }
    else:
        return {
                "status" : False,
                "msg" : "Retrieval Not Successful"
        }

@mess_router.get("/mess-on-date", tags=["Mess"])
async def get_mess_on_date(request: Request):

    cursor.execute(f"""SELECT DATE_ADD(end_date, INTERVAL 1 DAY) as mess_on_date from messoff JOIN student ON student.student_id=messoff.student_id""")
    
    result = cursor.fetchall()

    if result:
        return{
                "status": True,
                "msg": "Retrieval successful",
                "data": {
                    "MESS_ON_DATE": result
                }
        }
    else:
        return {
                "status" : False,
                "msg" : "Retrieval Not Successful"
        }