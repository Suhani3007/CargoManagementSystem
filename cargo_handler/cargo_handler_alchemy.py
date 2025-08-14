from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from model.model_sqlalch import Cargo

class PostgresInfoSQLA:

    def cargo_list_pagination(self, db: Session, limit: int, offset: int,
                               search_pattern_name: str, search_pattern_description: str,
                               order_by_clause: str):
        try:
            query = db.query(Cargo).filter(
                Cargo.cargo_name.ilike(search_pattern_name),
                Cargo.description.ilike(search_pattern_description),
                Cargo.archive == False
            )

            for item in order_by_clause.split(','):
                item = item.strip()
                if item.startswith("-"):
                    query = query.order_by(desc(getattr(Cargo, item[1:])))
                else:
                    query = query.order_by(asc(getattr(Cargo, item)))

            cargos = query.offset(offset).limit(limit).all()

            return [
                {
                    "cargo_name": c.cargo_name,
                    "description": c.description
                } for c in cargos
            ]
        except Exception as e:
            return {"message": f"{str(e)}"}
