from database_connection.db import get_db

class mongo_info:
    def cargo_inserting(self, data, cargo_id):
        try:
            conn=get_db()
            collections = conn["cargo"]
            name = data.cargo_name.lower()
            if collections.find_one({"cargo_name": name}):
                return {"message": f"{name} this name already exist"}
            collections.insert_one({
                "cargo_id": cargo_id,
                "cargo_name": name,
                "description": data.description,
                "quantity": data.quantity,
                "archive": False
            })
            return {
                "message": "data inserted"
            }
        except Exception as e:
            return {
                "message": f"error->{str(e)}"
            }


    def cargo_updateing(self, data):
        try:
            conn = get_db()
            collections = conn["cargo"]
            existing_cargo_id = collections.find_one({"cargo_id": data.cargo_id})
            if not existing_cargo_id:
                return {
                    "message": "cargo_not_found"
                }
            existing_name = collections.find_one({"cargo_name": data.cargo_name})
            if existing_name:
                    return {
                        "message": "name already used"
                    }
            collections.update_one(
                        {"cargo_id": data.cargo_id},
                        {"$set": {
                            "cargo_name": data.cargo_name,
                            "description": data.description,
                            "quantity": data.quantity,
                            "archive": False
                        }}
                    )
            return {
                "message": "updated"
            }
        except Exception as e:
            return {
                "message":f"{str(e)}"
            }

    def cargo_deleteing(self, data):
        try:
            conn=get_db()
            collections = conn["cargo"]
            collections.update_one(
                {"cargo_id": data.cargo_id},
                {"$set": {
                    "archive": True
                }}
            )
            return {
                "message": "deleted"
            }
        except Exception as e:
            return {
                "message":f"{str(e)}"
            }
    def cargo_listing(self):
        try:
            conn=get_db()
            collections = conn["cargo"]
            result_list=collections.find({})
            result=[]
            for row in result_list:
                    row["_id"] = str(row["_id"])
                    result.append(row)
            return result
        except Exception as e:
            return {
                "message":f"{str(e)}"
            }

    def cargo_list_pagination(self, filter_query, sort_list, limit, offset):
        try:
            conn = get_db()
            collections = conn["cargo"]
            return collections.find(filter_query).sort(sort_list).skip(offset).limit(limit)
        except Exception as e:
            return {
                "message":f"{str(e)}"
            }







