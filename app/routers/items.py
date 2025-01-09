from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from .. import services as svc
from .. import models as mdl
from ..core.dependencies import get_current_user

router = APIRouter(prefix="/items", tags=["items"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def read_root(
    request: Request,
    service: svc.ItemService = Depends(svc.get_item_service),
    current_user: mdl.UserModel = Depends(get_current_user)
):
    items = await service.get_items()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "items": items,
        "current_user": current_user
    })

@router.post("/items")
async def create_item(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    service: svc.ItemService = Depends(svc.get_item_service),
    current_user: mdl.UserModel = Depends(get_current_user)
):
    item = mdl.ItemModel(name=name, description=description)
    await service.create_item(item)
    items = await service.get_items()
    return templates.TemplateResponse(
        "partials/item_list.html", 
        {"request": request, "items": items}
    )