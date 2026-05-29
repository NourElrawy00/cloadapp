from app.extensions import db
from app.models.base import BaseModel

# Client model
class Client(BaseModel):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    agents = db.relationship('ClientAgent', backref='client', lazy=True, cascade='all, delete-orphan')

    def soft_delete(self):
        super().soft_delete()
        for agent in self.agents:
            agent.soft_delete()

    def restore(self):
        super().restore()
        for agent in self.agents:
            agent.restore()

class ClientAgent(BaseModel):
    __tablename__ = 'client_agent'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)

    phones = db.relationship('ClientAgentPhone', backref='client_agent', lazy=True, cascade='all, delete-orphan')
    emails = db.relationship('ClientAgentEmail', backref='client_agent', lazy=True, cascade='all, delete-orphan')


class ClientAgentPhone(BaseModel):
    __tablename__ = 'client_agent_phone'

    id = db.Column(db.Integer, primary_key=True)
    client_agent_id = db.Column(db.Integer, db.ForeignKey('client_agent.id'), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

class ClientAgentEmail(BaseModel):
    __tablename__ = 'client_agent_email'

    id = db.Column(db.Integer, primary_key=True)
    client_agent_id = db.Column(db.Integer, db.ForeignKey('client_agent.id'), nullable=False)
    email_address = db.Column(db.String(120), nullable=False)

# Supplier model
class Supplier(BaseModel):
    __tablename__ = 'supplier'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    agents = db.relationship('SupplierAgent', backref='supplier', lazy=True, cascade='all, delete-orphan')

    def soft_delete(self):
        super().soft_delete()
        for agent in self.agents:
            agent.soft_delete()

    def restore(self):
        super().restore()
        for agent in self.agents:
            agent.restore()

class SupplierAgent(BaseModel):
    __tablename__ = 'supplier_agent'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)

    phones = db.relationship('SupplierAgentPhone', backref='supplier_agent', lazy=True, cascade='all, delete-orphan')
    emails = db.relationship('SupplierAgentEmail', backref='supplier_agent', lazy=True, cascade='all, delete-orphan')


class SupplierAgentPhone(BaseModel):
    __tablename__ = 'supplier_agent_phone'

    id = db.Column(db.Integer, primary_key=True)
    supplier_agent_id = db.Column(db.Integer, db.ForeignKey('supplier_agent.id'), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

class SupplierAgentEmail(BaseModel):
    __tablename__ = 'supplier_agent_email'

    id = db.Column(db.Integer, primary_key=True)
    supplier_agent_id = db.Column(db.Integer, db.ForeignKey('supplier_agent.id'), nullable=False)
    email_address = db.Column(db.String(120), nullable=False)