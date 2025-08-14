from cargo_handler.cargo_handler import cargo_info
from model.model import Cargo,login_detail, cargo_ud, read_cargo,arranged_cargo_names,arranged_cargo_quantity,gen_tock,cargo_dl
from fastapi import APIRouter, Depends
from AppConfiguration.config import cargo_api

router = APIRouter()
c = cargo_info()


@router.post(cargo_api.login)
def cargo_admin_login(data:login_detail):
    try:
        return c.login(data)
    except Exception as e:
        return {
            "message":"login failed",
            "error":f"{str(e)}"
        }



@router.post(cargo_api.insertion)
def cargo_inject(data: Cargo,_:None=Depends(c.verify_token)):
    try:
        return c.cargo_insert(data)
    except Exception as e:
        return {
            "message": "failed",
            "error":f"{str(e)}"
        }


@router.post(cargo_api.updatepos)
def cargo_up(data: cargo_ud,_:None=Depends(c.verify_token)):
    try:
        return c.cargo_update(data)
    except Exception as e:
        return {
            "message": f"{str(e)}"
        }






@router.post(cargo_api.deletes)
def cargo_del(data:cargo_dl,_:None=Depends(c.verify_token)):
    try:
        return  c.cargo_delete(data)

    except Exception as e:
        return {
            "message": f"{str(e)}"
        }


@router.get("/fetch")
def cargo_list(_:None=Depends(c.verify_token)):
    try:
        return c.cargo_list()
    except Exception as e:
        return {
            "message": f"{str(e)}"
        }


@router.post(cargo_api.read_cargo_list)
def read_pag_cargo(data: read_cargo,_:None=Depends(c.verify_token)):
    try:
        offset = (data.page - 1) * data.rec_size
        limit = data.rec_size
        value_name=data.filter.cargo_name
        value_description=data.filter.description
        sorting=data.sort


        return c.read_cargo_list_pagination(limit=limit, offset=offset,value_name=value_name,value_description=value_description,sorting=sorting)
    except Exception as e:
        return {
            "message": f"{str(e)}"
        }


@router.post(cargo_api.name_method_arranged)
def cargo_name_arrangement(data:arranged_cargo_names,_:None=Depends(c.verify_token)):
    try:
        return c.arranged_cargo_name(data)
    except Exception as e:
        return {
            "message":f"{str(e)}"
        }

@router.post(cargo_api.quantity_method_arranged)
def cargo_quantity_arrangement(data:arranged_cargo_quantity,_:None=Depends(c.verify_token)):
    try:
        return c.arranged_cargo_quantity(data)
    except Exception as e:
        return {
            "message":f"{str(e)}"
        }




