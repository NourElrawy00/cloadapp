from app.extensions import db
import enum
from app.models.base import BaseModel

class MovementType(enum.Enum):
    initial    = 'initial'     # First stock entry when item is created
    buy        = 'buy'         # Stock in — received from a purchase (Buy)
    delivery   = 'delivery'    # Stock out — dispatched via a Delivery
    adjustment = 'adjustment'  # Manual correction (stocktake, write-off, etc.)
    returning  = 'return'      # Stock returned from a client

# warehouse model
class Warehouse(BaseModel):
    __tablename__ = 'warehouse'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    
    items = db.relationship('WarehouseItem', backref='warehouse', lazy=True, cascade='all, delete-orphan')

class WarehouseItem(BaseModel):
    __tablename__ = 'warehouse_item'

    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    stock = db.Column(db.Numeric(10, 2), nullable=False)
    min_stock = db.Column(db.Numeric(10, 2), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    movements = db.relationship('StockMovement', backref='warehouse_item', lazy=True, cascade='all, delete-orphan')

class StockMovement(BaseModel):
    __tablename__ = 'stock_movement'
 
    id                = db.Column(db.Integer, primary_key=True)
    warehouse_item_id = db.Column(db.Integer, db.ForeignKey('warehouse_item.id'), nullable=False, index=True)
 
    quantity    = db.Column(db.Numeric(10, 2), nullable=False)
    unit_price  = db.Column(db.Numeric(10, 4), nullable=False)
    total_price = db.Column(db.Numeric(12, 2), nullable=False)

    movement_type = db.Column(db.Enum(MovementType), nullable=False)

    stock_after = db.Column(db.Numeric(10, 2), nullable=False)
    value_after = db.Column(db.Numeric(12, 2), nullable=False)

    source_id = db.Column(db.Integer, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    user    = db.relationship('User', backref='stock_movements', lazy=True)
 
    note = db.Column(db.Text, nullable=True)