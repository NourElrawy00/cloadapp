from app.extensions import db
from app.services.helpers import Time

class BaseModel(db.Model):
    __abstract__ = True 

    created_at = db.Column(db.DateTime, nullable=False, default=Time.datetime_now)
    updated_at = db.Column(db.DateTime, nullable=False, default=Time.datetime_now, onupdate=Time.datetime_now)

    deleted = db.Column(db.Boolean, nullable=False, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def soft_delete(self):
        self.deleted = True
        self.deleted_at = Time.datetime_now()

    def restore(self):
        self.deleted = False
        self.deleted_at = None

    @classmethod
    def get_active(cls):
        return cls.query.filter_by(deleted=False).all()