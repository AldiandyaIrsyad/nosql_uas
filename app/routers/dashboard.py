from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from .. import services as svc
from .. import models as mdl
from ..core.dependencies import get_current_user

router = APIRouter(tags=["dashboard"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    title: str = None,
    year: str = None,
    service: svc.IndicatorService = Depends(svc.get_indicator_service),
    current_user: mdl.UserModel = Depends(get_current_user)
):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    titles = await service.get_unique_title()
    provinces = await service.get_unique_provinces()
    years = []
    indicators = []
    
    if title:
        years = await service.get_unique_year_based_on_title(title)
        
    if title and year:
        try:
            year_int = int(year)
            indicators = await service.get_by_title_and_year(title, year_int)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid year format")
        
    if is_ajax:
        return JSONResponse({
            "years": years,
            "indicators": [indicator.model_dump() for indicator in indicators]
        })

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "titles": titles,
        "years": years,
        "provinces": provinces,
        "current_title": title,
        "current_year": year,
        "indicators": indicators,
        "current_user": current_user
    })

@router.get("/graph", response_class=JSONResponse)
async def graph_data(
    title: str,
    province: str,
    service: svc.IndicatorService = Depends(svc.get_indicator_service)
):
    indicators = await service.get_by_title_and_province(title, province)
    return [indicator.model_dump() for indicator in indicators]

@router.get("/national_average", response_class=JSONResponse)
async def national_average(
    title: str,
    year: int,
    service: svc.IndicatorService = Depends(svc.get_indicator_service)
):
    indicator = await service.get_national_average(title, year)
    if indicator:
        return {"year": indicator.year, "value": indicator.value}
    return {"year": None, "value": None}