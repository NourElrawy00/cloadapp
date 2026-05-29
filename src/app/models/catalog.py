from app.extensions import db
from app.models.base import BaseModel

# Product model
class Product(BaseModel):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)

    # Relationships pointing outward to your transactions
    buy_items = db.relationship('BuyItem', backref='product', lazy=True)
    delivery_items = db.relationship('DeliveryItem', backref='product', lazy=True)
    invoice_items = db.relationship('InvoiceItem', backref='product', lazy=True)
    offer_items = db.relationship('OfferItem', backref='product', lazy=True)
    warehouse_items = db.relationship('WarehouseItem', backref='product', lazy=True)