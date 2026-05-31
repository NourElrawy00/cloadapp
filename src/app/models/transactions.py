from app.extensions import db
import enum
from app.models.base import BaseModel

# Enums
class InvoiceStatus(enum.Enum):
    issued    = 'issued'     # Sent to client, awaiting payment
    partial   = 'partial'    # Some payments received, not fully paid
    paid      = 'paid'       # Fully paid
    overdue   = 'overdue'    # Past due date with remaining balance
    cancelled = 'cancelled'  # Voided
 
class PaymentMethod(enum.Enum):
    cash          = 'cash'
    bank_transfer = 'bank_transfer'
    cheque        = 'cheque'
    other         = 'other'

# Buy model
class Buy(BaseModel):
    __tablename__ = 'buy'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    date = db.Column(db.Date, nullable=False)
    reference = db.Column(db.String(80), nullable=False)

    items = db.relationship('BuyItem', backref='buy', lazy=True, cascade='all, delete-orphan')

class BuyItem(BaseModel):
    __tablename__ = 'buy_item'

    id = db.Column(db.Integer, primary_key=True)
    buy_id = db.Column(db.Integer, db.ForeignKey('buy.id'), nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    price_buy = db.Column(db.Numeric(10, 2), nullable=False)

class Buycart(BaseModel):
    __tablename__ = 'buy_cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    price_buy = db.Column(db.Numeric(10, 2), nullable=False)

# Delivery model
class Delivery(BaseModel):
    __tablename__ = 'delivery'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    date = db.Column(db.Date, nullable=False)
    reference = db.Column(db.String(80), nullable=False)

    items = db.relationship('DeliveryItem', backref='delivery', lazy=True, cascade='all, delete-orphan')
    client = db.relationship('Client', backref='deliveries')

class DeliveryItem(BaseModel):
    __tablename__ = 'delivery_item'

    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'), nullable=False)
    buy_item_id = db.Column(db.Integer, db.ForeignKey('buy_item.id'), nullable=True)
    warehouse_item_id = db.Column(db.Integer, db.ForeignKey('warehouse_item.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    quantity = db.Column(db.Numeric(10, 2), nullable=False)

class Deliverycart(BaseModel):
    __tablename__ = 'delivery_cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    buy_item_id = db.Column(db.Integer, db.ForeignKey('buy_item.id'), nullable=True)
    warehouse_item_id = db.Column(db.Integer, db.ForeignKey('warehouse_item.id'), nullable=True)

    quantity = db.Column(db.Numeric(10, 2), nullable=False)

# Invoice model
class Invoice(BaseModel):
    __tablename__ = 'invoice'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    date = db.Column(db.Date, nullable=False)
    number = db.Column(db.String(80), nullable=False)
    po_number = db.Column(db.String(80), nullable=True)
    status = db.Column(db.Enum(InvoiceStatus), nullable=False, default=InvoiceStatus.issued)

    items    = db.relationship('InvoiceItem', backref='invoice', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment',     backref='invoice', lazy=True, cascade='all, delete-orphan')
    client   = db.relationship('Client', backref='invoices')

class InvoiceItem(BaseModel):
    __tablename__ = 'invoice_item'

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    delivery_item_id = db.Column(db.Integer, db.ForeignKey('delivery_item.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    price_sell = db.Column(db.Numeric(10, 2), nullable=False)

class Invoicecart(BaseModel):
    __tablename__ = 'invoice_cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    delivery_item_id = db.Column(db.Integer, db.ForeignKey('delivery_item.id'), nullable=False)

    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    price_sell = db.Column(db.Numeric(10, 2), nullable=False)

# Payment model
class Payment(BaseModel):
    __tablename__ = 'payment'
 
    id         = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False, index=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'),    nullable=False, index=True)
 
    date      = db.Column(db.Date,                nullable=False)
    amount    = db.Column(db.Numeric(12, 2),      nullable=False)
    method    = db.Column(db.Enum(PaymentMethod), nullable=False)
 
    reference = db.Column(db.String(120), nullable=True)
    note      = db.Column(db.Text,        nullable=True)
 
    user = db.relationship('User', backref='payments', lazy=True)