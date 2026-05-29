from app.extensions import db
from app.models.base import BaseModel

# warehouse model
class Warehouse(BaseModel):
    __tablename__ = 'warehouse'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    
    items = db.relationship('WarehouseItem', backref='warehouse', lazy=True, cascade='all, delete-orphan')

class WarehouseItem(BaseModel):
    __tablename__ = 'warehouse_item'

    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    stock = db.Column(db.Numeric(10, 2), nullable=False)
    min_stock = db.Column(db.Numeric(10, 2), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)