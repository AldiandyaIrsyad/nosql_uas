from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from ..services import IndicatorService, get_indicator_service
from ..models.indicator_model import IndicatorModel
from ..models.user_model import UserModel, AnonymousUser
from ..core.dependencies import get_current_user
import datetime

router = APIRouter(prefix="/indicators", tags=["indicators"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def list_indicators(
    request: Request,
    service: IndicatorService = Depends(get_indicator_service),
    current_user: UserModel = Depends(get_current_user)
):
    

    province = request.query_params.get("province")
    title = request.query_params.get("title")
    indicator = request.query_params.get("indicator")
    year_range = request.query_params.get("year_range")
    print("running")
    
    indicators = await service.filter_indicators(province, title, indicator, year_range)
    print("not running")
    provinces = await service.get_unique_provinces()
    titles = await service.get_unique_title()
    
    return templates.TemplateResponse("indicators/list.html", {
        "request": request,
        "indicators": indicators,
        "provinces": provinces,
        "titles": titles,
        "current_user": current_user
    })


@router.get("/create", response_class=HTMLResponse)
async def create_indicator_page(
    request: Request,
    service: IndicatorService = Depends(get_indicator_service),
    current_user: UserModel = Depends(get_current_user)
):
    if isinstance(current_user, AnonymousUser):
        return RedirectResponse(url="/manage", status_code=303)
    
    current_year = datetime.datetime.now().year
    return templates.TemplateResponse("indicators/create.html", {
        "request": request,
        "current_user": current_user,
        "current_year": current_year,
        "min_year": current_year - 5,
        "max_year": current_year + 5,
        "titles": await service.get_unique_title(),
        "indicators": await service.get_unique_indicator()
    })

@router.post("/create", response_class=HTMLResponse)
async def create_indicator(
    request: Request,
    province: str = Form(...),
    year: int = Form(...),
    title: str = Form(...),
    indicator: str = Form(...),
    value: float = Form(...),
    service: IndicatorService = Depends(get_indicator_service),
    current_user: UserModel = Depends(get_current_user)
):
    if isinstance(current_user, AnonymousUser):
        return RedirectResponse(url="/manage", status_code=303)
    
    print("1")
    new_indicator = IndicatorModel(
        province=province,
        year=year,
        title=title,
        indicator=indicator,
        value=value
    )
    print("2")

    try:
        await service.create_indicator(new_indicator)
        await service.update_indonesia_average(title, year)
        
        return RedirectResponse(url="/indicators/manage", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("indicators/create.html", {
            "request": request,
            "current_user": current_user,
            "error": str(e),
            "current_year": datetime.datetime.now().year,
            "min_year": datetime.datetime.now().year - 5,
            "max_year": datetime.datetime.now().year + 5,
            "titles": await service.get_unique_title(),
            "indicators": await service.get_unique_indicator()
        })

@router.get("/provinces", response_class=HTMLResponse)
async def list_provinces(
    request: Request,
    service: IndicatorService = Depends(get_indicator_service),
    current_user: UserModel = Depends(get_current_user)
):
    provinces = await service.get_unique_provinces()
    return templates.TemplateResponse("indicators/provinces.html", {
        "request": request,
        "provinces": provinces,
        "current_user": current_user
    })

@router.get("/titles")
async def get_titles(
    indicator: str,
    service: IndicatorService = Depends(get_indicator_service),
):
    titles = await service.get_unique_title_by_indicator(indicator)
    return {"titles": titles}

@router.get("/edit/{indicator_id}", response_class=HTMLResponse)
async def edit_indicator_page(
    request: Request,
    indicator_id: str,
    service: IndicatorService = Depends(get_indicator_service),
    current_user: UserModel = Depends(get_current_user)
):
    if isinstance(current_user, AnonymousUser):
        return RedirectResponse(url="/", status_code=303)
    
    indicator = await service.get_indicator_by_id(indicator_id)
    if indicator.province != current_user.province:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    return templates.TemplateResponse("indicators/edit.html", {
        "request": request,
        "current_user": current_user,
        "indicator": indicator
    })

@router.post("/edit/{indicator_id}", response_class=HTMLResponse)
async def edit_indicator(
    request: Request,
    indicator_id: str,
    province: str = Form(...),
    year: int = Form(...),
    title: str = Form(...),
    indicator: str = Form(...),
    value: float = Form(...),
    service: IndicatorService = Depends(get_indicator_service),
    current_user: UserModel = Depends(get_current_user)
):
    if isinstance(current_user, AnonymousUser):
        return RedirectResponse(url="/", status_code=303)
    
    existing_indicator = await service.get_indicator_by_id(indicator_id)
    if existing_indicator.province != current_user.province:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    updated_indicator = IndicatorModel(
        id=indicator_id,
        province=province,
        year=year,
        title=title,
        indicator=indicator,
        value=value
    )
    try:
        await service.update_indicator(updated_indicator)
        await service.update_indonesia_average(title, year)
        return RedirectResponse(url="/indicators/manage", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("indicators/edit.html", {
            "request": request,
            "current_user": current_user,
            "indicator": updated_indicator,
            "error": str(e)
        })

@router.post("/delete/{indicator_id}", response_class=HTMLResponse)
async def delete_indicator(
    request: Request,
    indicator_id: str,
    service: IndicatorService = Depends(get_indicator_service),
    current_user: UserModel = Depends(get_current_user)
):
    if isinstance(current_user, AnonymousUser):
        return RedirectResponse(url="/", status_code=303)
    
    indicator = await service.get_indicator_by_id(indicator_id)
    if indicator.province != current_user.province:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    try:
        await service.delete_indicator(indicator_id)
        await service.update_indonesia_average(indicator.title, indicator.year)
        return RedirectResponse(url="/indicators/manage", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("indicators/manage.html", {
            "request": request,
            "current_user": current_user,
            "error": str(e)
        })

@router.get("/manage", response_class=HTMLResponse)
async def manage_indicators(
    request: Request,
    service: IndicatorService = Depends(get_indicator_service),
    current_user: UserModel = Depends(get_current_user)
):
    if isinstance(current_user, AnonymousUser):
        return RedirectResponse(url="/", status_code=303)
    
    indicators = await service.get_by_province(current_user.province)
    
    return templates.TemplateResponse("indicators/manage.html", {
        "request": request,
        "indicators": indicators,
        "current_user": current_user
    })