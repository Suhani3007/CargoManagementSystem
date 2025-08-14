from database_connection.db import get_db



class postgres_info:
    def cargo_inserting(self, data, cargo_id):
        try:
            conn = get_db()
            cur = conn.cursor()
            name = data.cargo_name.lower()
            cur.execute("select 1 from cargo where cargo_name=%s", (name,))
            if cur.fetchone():
                return {
                    "message": f"{name},already exist"
                }
            cur.execute("insert into cargo(cargo_id,cargo_name,description,quantity,archive) values(%s,%s,%s,%s,%s)",
                        (cargo_id, name, data.description, data.quantity, False))
            conn.commit()
            return {
                "message": f"{cargo_id}->>{name} successfully added"
            }
        except Exception as e:
            return  {
                "message":f"{str(e)}"
            }

    def cargo_updateing(self, data):
        try:
            conn = get_db()
            curr = conn.cursor()
            curr.execute("select * from cargo where cargo_id=%s ", (data.cargo_id,))
            if not curr.fetchone():
                return {
                    "message": "cargo not found"
                }
            curr.execute("select 1 from cargo where cargo_name=%s", (data.cargo_name,))
            if curr.fetchone():
                return {
                    "message": f"({data.cargo_name})->name is already used by another user"
                }
            curr.execute("update cargo set cargo_name=%s,description=%s,quantity=%s,archive=%s where cargo_id=%s",
                         (data.cargo_name, data.description, data.quantity, False, data.cargo_id))
            conn.commit()
            return {
                "message": "update done"
            }
        except Exception as e:
            return{
                "message":f"{str(e)}"
            }

    def cargo_deleteing(self,data):
        try:
            conn=get_db()
            curr=conn.cursor()
            curr.execute("update cargo  set archive=%s where cargo_id=%s",(True,data.cargo_id))
            conn.commit()
            return {
                    "message":"deleted"
                }

        except Exception as e:
            return {
                "message":f"{str(e)}"
            }

    def cargo_listing(self):
        try:
            conn=get_db()
            curr=conn.cursor()
            curr.execute("select * from cargo where archive=%s",(False,))
            result=curr.fetchall()
            conn.commit()
            return {
                    "data":f"{result}"
                }
        except Exception as e:
            return {
                "message":f"{str(e)}"
            }

    def cargo_list_pagination(self, limit, offset, search_pattern_name, search_pattern_description, order_by_clause):
        try:
            conn=get_db()
            curr = conn.cursor()
            query = f"""
                            SELECT cargo_name, description
                            FROM cargo
                            WHERE cargo_name ILIKE %s AND description ILIKE %s
                            ORDER BY {order_by_clause}
                            LIMIT %s OFFSET %s
                      """
            return curr.execute(query,(search_pattern_name,search_pattern_description,limit,offset))
        except Exception as e:
            return {
                "message":f"{str(e)}"
            }








