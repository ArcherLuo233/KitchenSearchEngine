from app import db
class R_T(db.Model):
    __tablename__ = 'r_t'
    tag_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, unique=True, nullable=False)


    def __repr__(self):
        return '<r_t %r>' % self.tag_id