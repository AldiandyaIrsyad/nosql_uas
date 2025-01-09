from .item_service import ItemService, get_item_service
from .user_service import UserService, get_user_service
from .indicator_service import IndicatorService, get_indicator_service

__all__ = [
    'ItemService',
    'UserService',
    'IndicatorService',
    'get_item_service',
    'get_user_service',
    'get_indicator_service'
]


item_service = ItemService()
user_service = UserService()
indicator_service = IndicatorService()