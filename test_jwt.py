# from jose import jwt
#
# # Create Token
# payload = {"user_id": 123, "username": "admin"}
# secret_key = "my_secret"
#
# # Encode
# token = jwt.encode(payload, secret_key, algorithm="HS256")
# print("JWT Token:", token)
#
# # Decode
# decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
# print("Decoded Payload:", decoded)



































from bson import ObjectId
from docxtpl import DocxTemplate
from starlette.responses import FileResponse
import os

def read_cargo_list_pagination(self, limit: int, offset: int, value_name: str, value_description: str, sorting: str):
    file_path = "output.docx"

    try:
        conn = get_db()

        if os.getenv("DB_TYPE") == "postgres":
            curr = conn.cursor()
            search_pattern_name = f"%{value_name}%"
            search_pattern_description = f"%{value_description}%"

            arrangement_info = sorting.split(",")
            order = []
            for item in arrangement_info:
                item = item.strip()
                if item.startswith("-"):
                    order.append(f"{item[1:]} DESC")
                else:
                    order.append(f"{item[1:]} ASC")
            order_by_clause = " , ".join(order)

            query = f"""
                SELECT cargo_name, description
                FROM cargo
                WHERE cargo_name ILIKE %s AND description ILIKE %s
                ORDER BY {order_by_clause}
                LIMIT %s OFFSET %s
            """

            curr.execute(query, (search_pattern_name, search_pattern_description, limit, offset))
            result = curr.fetchall()

            cargo_list = []
            for row in result:
                cargo_item = {
                    "cargo_name": row[0],
                    "description": row[1]
                }
                cargo_list.append(cargo_item)

        elif os.getenv("DB_TYPE") == "mongo":
            collection = conn["cargo"]

            # Build filter query
            filter_query = {
                "cargo_name": {"$regex": value_name, "$options": "i"},
                "description": {"$regex": value_description, "$options": "i"},
            }

            # Build sorting
            arrangement_info = sorting.split(",")
            sort_list = []
            for item in arrangement_info:
                item = item.strip()
                if item.startswith("-"):
                    sort_list.append((item[1:], -1))  # Descending
                else:
                    sort_list.append((item, 1))      # Ascending

            # Execute query with pagination
            cursor = collection.find(filter_query).sort(sort_list).skip(offset).limit(limit)

            cargo_list = []
            for doc in cursor:
                doc.pop("_id", None)  # Remove _id from response
                cargo_item = {
                    "cargo_name": doc.get("cargo_name"),
                    "description": doc.get("description")
                }
                cargo_list.append(cargo_item)

        # Generate Word document
        doc = DocxTemplate("cargo_handler/cargo_template.docx")
        context = {"cargo_list": cargo_list}
        doc.render(context)
        doc.save(file_path)

        return FileResponse(
            path=file_path,
            filename="cargo_list.docx",
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        return {"message": f"{str(e)}"}





















def read_cargo_list_pagination(self, limit: int, offset: int, value_name: str, value_description: str, sorting: str):
    file_path = "output.docx"
    try:
        conn = get_db()
        db_type = os.getenv("DB_TYPE")
        cargo_list = []

        if db_type == "postgres":
            curr = conn.cursor()
            search_pattern_name = f"%{value_name}%"
            search_pattern_description = f"%{value_description}%"

            arrangement_info = sorting.split(",")
            valid_columns = ["cargo_name", "description", "quantity"]  # Example allowed fields
            order = []
            for item in arrangement_info:
                item = item.strip()
                field = item[1:] if item.startswith("-") else item
                if field not in valid_columns:
                    continue  # skip invalid fields
                order.append(f"{field} {'DESC' if item.startswith('-') else 'ASC'}")
            order_by_clause = " , ".join(order)

            query = f"""
                SELECT cargo_name, description
                FROM cargo
                WHERE archive = False AND cargo_name ILIKE %s AND description ILIKE %s
                ORDER BY {order_by_clause}
                LIMIT %s OFFSET %s
            """

            curr.execute(query, (search_pattern_name, search_pattern_description, limit, offset))
            result = curr.fetchall()

            for row in result:
                cargo_list.append({"cargo_name": row[0], "description": row[1]})

        elif db_type == "mongo":
            collection = conn["cargo"]
            filter_query = {
                "cargo_name": {"$regex": value_name, "$options": "i"},
                "description": {"$regex": value_description, "$options": "i"},
                "archive": False
            }
            arrangement_info = sorting.split(",")
            sort_list = []
            for item in arrangement_info:
                item = item.strip()
                sort_list.append((item[1:], -1) if item.startswith("-") else (item, 1))

            cursor = collection.find(filter_query).sort(sort_list).skip(offset).limit(limit)
            for doc in cursor:
                doc.pop("_id", None)
                cargo_list.append({"cargo_name": doc.get("cargo_name"), "description": doc.get("description")})

        if not cargo_list:
            return {"message": "No cargo records found."}

        doc = DocxTemplate("cargo_handler/cargo_template.docx")
        doc.render({"cargo_list": cargo_list})
        doc.save(file_path)

        return FileResponse(path=file_path, filename="cargo_list.docx",
                            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    except Exception as e:
        return {"message": f"{str(e)}"}



