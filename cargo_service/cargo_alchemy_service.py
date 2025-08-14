from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from model.model_sqlalch import read_cargo
from database_connection.db_sqlalchemy import get_db
from cargo_handler.cargo_handler_alchemy import PostgresInfoSQLA


router = APIRouter()

@router.post("/read-cargo-list")
def read_pag_cargo(data: read_cargo, db: Session = Depends(get_db)):
    try:
        offset = (data.page - 1) * data.rec_size
        limit = data.rec_size

        value_name = f"%{data.filter.cargo_name}%" if data.filter.cargo_name else "%"
        value_description = f"%{data.filter.description}%" if data.filter.description else "%"
        sorting = data.sort or "cargo_name"

        return PostgresInfoSQLA().cargo_list_pagination(
            db=db,
            limit=limit,
            offset=offset,
            search_pattern_name=value_name,
            search_pattern_description=value_description,
            order_by_clause=sorting
        )
    except Exception as e:
        return {"message": f"Error: {str(e)}"}
