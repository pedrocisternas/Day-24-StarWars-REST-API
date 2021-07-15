from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    favorites = db.relationship('Favorite', backref='user')

    def __repr__(self):
        return '<User %r,%r,%r,%r>' % (self.id, self.username, self.email, self.password)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "favorites": [favorite.serialize() for favorite in self.favorites ]
            # do not serialize the password, its a security breach
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    entity_type = db.Column(db.String(120), unique=False, nullable=False)
    entity_id = db.Column(db.Integer, unique=False, nullable=False)
    username = db.Column(db.String(120), db.ForeignKey('user.username'))

    def __repr__(self):
        return '<Favorite %r,%r,%r,%r,%r>' % (self.id, self.name, self.entity_type, self.entity_id, self.username)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "username": self.username,
            # do not serialize the password, its a security breach
        }