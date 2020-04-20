
from app import db
class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    pv = db.Column(db.Integer, unique=True, nullable=False)
    img =db.Column(db.String(500))
    rating=db.Column(db.String(255))
    time=db.Column(db.Date)
    cooked=db.Column(db.Integer)
    description=db.Column(db.String(500))
    def __repr__(self):
        return '<recipe %r>' % self.id