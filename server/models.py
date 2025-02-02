from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)
    recipes = db.relationship(
        "Recipe", back_populates="user", cascade="all, delete-orphan"
    )
    
    
    @hybrid_property
    def password_hash(self):
        raise AttributeError('Cannot access password_hash attribute directly')
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('UTF-8'))
        self._password_hash = password_hash.decode('UTF-8')
        
    def authenticate(self,password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
    
    def __repr__(self):
        return f"<User {self.id}: Username : {self.username}, Bio: {self.bio}"
class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String)
    minutes_to_complete = db.Column(db.Integer)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="recipes")
     
    @validates('instructions')
    def checking_length(self, key, instructions):
        if len(instructions) < 50:
            raise ValueError("Instructions must be more than 50 characters")
        return instructions