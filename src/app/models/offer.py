from app.extensions import db
from app.models.base import BaseModel

# offer model
class Offer(BaseModel):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    date = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    number = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    items = db.relationship('OfferItem', backref='offer', lazy=True, cascade='all, delete-orphan')
    client = db.relationship('Client', backref='offers')

class OfferConfig(BaseModel):
    __tablename__ = 'offer_config'

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False, unique=True)

    contact_name = db.Column(db.String(80), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)

    delivery_period = db.Column(db.String(80), nullable=False)
    validity_period = db.Column(db.String(80), nullable=False)

class OfferItem(BaseModel):
    __tablename__ = 'offer_item'

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)

    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

class Offercart(BaseModel):
    __tablename__ = 'offer_cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)