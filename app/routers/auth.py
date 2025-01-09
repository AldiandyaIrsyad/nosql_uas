from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .. import services as svc
from .. import models as mdl
from ..core.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/register", response_class=HTMLResponse)
async def register_page(
    request: Request,
    indicator_service: svc.IndicatorService = Depends(svc.get_indicator_service),
    current_user: mdl.UserModel = Depends(get_current_user)
):
    # First await the async result, then convert to list
    provinces = await indicator_service.get_unique_provinces()
    provinces_list = list(provinces)

    return templates.TemplateResponse("register.html", {
        "request": request,
        "provinces": provinces_list,
        "current_user": current_user
    })

@router.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    province: str = Form(...),
    service: svc.UserService = Depends(svc.get_user_service),
    indicator_service: svc.IndicatorService = Depends(svc.get_indicator_service),
    current_user: mdl.UserModel = Depends(get_current_user)
):
    try:
        user_data = mdl.UserCreate(
            email=email, 
            username=username, 
            password=password,
            province=province
        )
        await service.register(user_data)
        return templates.TemplateResponse("register_success.html", {
            "request": request,
            "current_user": current_user
        })
    except HTTPException as e:

        provinces = await indicator_service.get_unique_provinces()
        provinces_list = list(provinces)
        
        return templates.TemplateResponse("register.html", {
            "request": request,
            "provinces": provinces_list,
            "error": e.detail,
            "current_user": current_user
        })

@router.get("/login", response_class=HTMLResponse)
async def login_page(
    request: Request,
    current_user: mdl.UserModel = Depends(get_current_user)
):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "current_user": current_user
    })

@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    service: svc.UserService = Depends(svc.get_user_service)
):
    try:
        token = await service.authenticate(email, password)
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {token.access_token}",
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=1800  # 30 minutes
        )
        return response
    except HTTPException:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid email or password"}
        )
@router.post("/logout")
async def logout():
    response = RedirectResponse(url="/auth/login", status_code=303)
    response.delete_cookie("access_token")
    return response