from ..utils import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(50), nullable = False, unique=True)
    password_hash = db.Column(db.Text(), nullable = False)
    is_staff = db.Column(db.Boolean(), default=False)
    is_active = db.Column(db.Boolean(), default=False)
    date_created = db.Column(db.DateTime(), default = datetime.utcnow())
    orders = db.relationship('Orders', backref='customer', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()


    
    @classmethod
    def get_by_id(model, id):
        return model.query.get_or_404(id)