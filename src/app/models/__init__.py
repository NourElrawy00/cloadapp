from app.extensions import db

from app.models.base import BaseModel
from app.models.catalog import Product
from app.models.crm import (
    Client, ClientAgent, ClientAgentPhone, ClientAgentEmail,
    Supplier, SupplierAgent, SupplierAgentPhone, SupplierAgentEmail,
)
from app.models.transactions import (
    Buy, BuyItem,
    Delivery, DeliveryItem,
    Invoice, InvoiceItem, InvoiceStatus,
    Payment, PaymentMethod,
)
from app.models.offer import Offer, OfferItem, OfferConfig, Offercart
from app.models.users import User, UserRole
from app.models.warehouse import Warehouse, WarehouseItem, StockMovement, MovementType
from app.models.log import Logs, LogAction, LogEntity

__all__ = [
    'BaseModel',
    'Product',
    'Client', 'ClientAgent', 'ClientAgentPhone', 'ClientAgentEmail',
    'Supplier', 'SupplierAgent', 'SupplierAgentPhone', 'SupplierAgentEmail',
    'Buy', 'BuyItem',
    'Delivery', 'DeliveryItem',
    'Invoice', 'InvoiceItem', 'InvoiceStatus',
    'Payment', 'PaymentMethod',
    'Offer', 'OfferItem', 'OfferConfig', 'Offercart',
    'User', 'UserRole',
    'Warehouse', 'WarehouseItem', 'StockMovement', 'MovementType',
    'Logs', 'LogAction', 'LogEntity',
]