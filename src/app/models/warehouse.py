import enum
from app.extensions import db
from app.models.base import BaseModel


class MovementType(enum.Enum):
    initial    = 'initial'
    buy        = 'buy'
    delivery   = 'delivery'
    adjustment = 'adjustment'
    returning  = 'return'


STOCK_IN_TYPES = {MovementType.initial, MovementType.buy, MovementType.returning}


class Warehouse(BaseModel):
    __tablename__ = 'warehouse'

    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(80),  nullable=False)
    location = db.Column(db.String(255), nullable=True)

    items = db.relationship('WarehouseItem', backref='warehouse', lazy=True, cascade='all, delete-orphan')


class WarehouseItem(BaseModel):
    __tablename__ = 'warehouse_item'

    id           = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False, index=True)
    product_id   = db.Column(db.Integer, db.ForeignKey('product.id'),   nullable=False, index=True)

    stock       = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    min_stock   = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    price       = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    total_value = db.Column(db.Numeric(12, 2), nullable=False, default=0)

    movements = db.relationship('StockMovement', backref='warehouse_item', lazy=True, cascade='all, delete-orphan')

    @property
    def is_low_stock(self):
        return self.stock <= self.min_stock


class StockMovement(BaseModel):
    __tablename__ = 'stock_movement'

    id                = db.Column(db.Integer, primary_key=True)
    warehouse_item_id = db.Column(db.Integer, db.ForeignKey('warehouse_item.id'), nullable=False, index=True)

    quantity      = db.Column(db.Numeric(10, 2), nullable=False)
    unit_price    = db.Column(db.Numeric(10, 4), nullable=False)
    total_price   = db.Column(db.Numeric(12, 2), nullable=False)
    movement_type = db.Column(db.Enum(MovementType), nullable=False)
    stock_after   = db.Column(db.Numeric(10, 2), nullable=False)
    value_after   = db.Column(db.Numeric(12, 2), nullable=False)
    source_id     = db.Column(db.Integer, nullable=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    note          = db.Column(db.Text, nullable=True)

    user = db.relationship('User', backref='stock_movements', lazy=True)