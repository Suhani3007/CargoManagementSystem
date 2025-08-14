
import os
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from docxtpl import DocxTemplate
from starlette.responses import FileResponse

from utils.generate_uuid import generate_uuid
from AppConfiguration.configuration import secret_key
from dotenv import load_dotenv
from db_operation.mongo_persistence import mongo_info
from db_operation.postgres_persistence import  postgres_info

load_dotenv()








class cargo_info:
    bearer = HTTPBearer()
    def login(self,data):
        name = os.getenv("name")
        password = os.getenv("password")
        if data.admin_name==name and data.admin_pass==password:
            payload = {"admin_name": data.admin_name}
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            return {
                "token":f"{token}",
                "admin_name":f"{data.admin_name}"
            }
    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(bearer)):
        try:
            payload = jwt.decode(credentials.credentials,secret_key,algorithms=["HS256"])
            admin_name = payload.get("admin_name")
            if not admin_name:
                raise ValueError("Invalid token: Missing username")
            return admin_name
        except Exception as e:
            raise RuntimeError(f"Token verification failed: {e}")


    def cargo_insert(self,data):
        try:
            print(data)
            cargo_id=generate_uuid()
            if os.getenv("DB_TYPE")=="postgres":
                return postgres_info().cargo_inserting(data, cargo_id)
            elif os.getenv("DB_TYPE")=="mongo":
                return mongo_info().cargo_inserting(data, cargo_id)
        except Exception as e:
            return {
                "message":f"error->{str(e)}"
            }

    def cargo_update(self,data):
        try:
            if os.getenv("DB_TYPE")=="postgres":
                return postgres_info().cargo_updateing(data)
            elif os.getenv("DB_TYPE")=="mongo":
                    return mongo_info().cargo_updateing(data)
        except Exception as e:
            return{
                "message":f"{str(e)}"
            }


    def cargo_delete(self,data):
        try:
            if os.getenv("DB_TYPE") == "postgres":
                return postgres_info().cargo_deleteing(data)
            elif os.getenv("DB_TYPE")=="mongo":
                return mongo_info().cargo_deleteing(data)
        except Exception as e:
            return {
                "message":f"{str(e)}"
            }

    def cargo_list(self):
        try:
            if os.getenv("DB_TYPE") == "postgres":
                return postgres_info().cargo_listing()
            elif os.getenv("DB_TYPE") == "mongo":
               result_list=mongo_info().cargo_listing()
               result=[]
               for row in result_list:
                    row["_id"] = str(row["_id"])
                    result.append(row)
               return result
        except Exception as e:
            return {
                "message":f"{str(e)}"
            }

    def read_cargo_list_pagination(self,limit: int, offset: int,value_name:str,value_description:str,sorting:str):
        file_path="output.docx"
        try:
           if os.getenv("DB_TYPE") == "postgres":
                   search_pattern_name = f"%{value_name}%"
                   search_pattern_description=f"%{value_description}%"
                   arrangement_info=sorting.split(",")
                   order=[]
                   for item in arrangement_info:
                       item = item.strip()
                       if item.startswith("-"):
                           order.append(f"{item[1:]} DESC")
                       else:
                           order.append(f"{item[1:]} ASC")
                   order_by_clause=" , ".join(order)
                   result=postgres_info().cargo_list_pagination(limit, offset, search_pattern_name, search_pattern_description, order_by_clause)
                   cargo_list = []
                   for row in result:
                       cargo_item = {
                           "cargo_name": row[0],
                           "description": row[1]
                       }
                       cargo_list.append(cargo_item)
                   doc = DocxTemplate("cargo_handler/cargo_template.docx")
                   context = {"cargo_list": cargo_list}
                   doc.render(context)
                   doc.save(file_path)

           elif os.getenv("DB_TYPE") == "mongo":
               filter_query = {
                   "cargo_name": {"$regex": value_name, "$options": "i"},
                   "description": {"$regex": value_description, "$options": "i"},
               }
               arrangement_info = sorting.split(",")
               sort_list = []
               for item in arrangement_info:
                   item = item.strip()
                   if item.startswith("-"):
                       sort_list.append((item[1:], -1))  # Descending
                   else:
                       sort_list.append((item, 1))
               cursor = mongo_info().cargo_list_pagination(filter_query, sort_list, limit, offset)
               cargo_list = []
               for doc in cursor:
                    doc.pop("_id", None)  # Remove _id from response
                    cargo_item = {
                        "cargo_name": doc.get("cargo_name"),
                        "description": doc.get("description")
                    }
                    cargo_list.append(cargo_item)

               doc = DocxTemplate("cargo_handler/cargo_template.docx")
               context = {"cargo_list": cargo_list}
               doc.render(context)
               doc.save(file_path)


           return FileResponse(path=file_path, filename="cargo_list.docx",media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

        except Exception as e:
            return {"message": f"{str(e)}"}


    # def arranged_cargo_name(self,data):
    #     try:
    #         method = data.enter_descending_or_ascending.lower()
    #         if method=="descending" or method=="-":
    #             conn=get_db()
    #             curr=conn.cursor()
    #             curr.execute("select cargo_name from cargo order by cargo_name DESC")
    #             result=curr.fetchall()
    #             conn.commit()
    #             return {
    #                 "message":f"{result}"
    #             }
    #         if method=="ascending":
    #             conn=get_db()
    #             curr=conn.cursor()
    #             curr.execute("select cargo_name from cargo order by cargo_name ASC")
    #             result=curr.fetchall()
    #             conn.commit()
    #             return {
    #                 "message":f"{result}"
    #             }
    #     except Exception as e:
    #         return {
    #             "message":f"{str(e)}"
    #         }
    #
    #
    # def arranged_cargo_quantity(self,data):
    #     try:
    #         method=data.enter_descending_or_ascending.lower()
    #         if method=="descending" or method=="-":
    #             conn=get_db()
    #             curr=conn.cursor()
    #             curr.execute("select cargo_name,quantity from cargo order by quantity DESC")
    #             result=curr.fetchall()
    #             conn.commit()
    #             return {
    #                 "message":f"{result}"
    #             }
    #         if method=="ascending":
    #             conn=get_db()
    #             curr=conn.cursor()
    #             curr.execute("select cargo_name,quantity from cargo order by quantity ASC")
    #             result=curr.fetchall()
    #             conn.commit()
    #             return {
    #                 "message":f"{result}"
    #             }
    #     except Exception as e:
    #         return {
    #             "message":f"{str(e)}"
    #         }
    #
    #
    #
    #
    #
    #
    #
