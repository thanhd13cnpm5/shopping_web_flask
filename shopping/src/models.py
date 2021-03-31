from sqlalchemy.orm import relationship
from src import *
from _datetime import datetime
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, Text, DECIMAL, Date, ForeignKey, Float


class admin(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=True)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)



class user(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=True)
    username = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    created = Column(Date, default=datetime.today())
    receipts = relationship("Receipt", backref="user")



class catagory(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name_catagory = Column(Text, nullable=True)
    product_cata = relationship("product", backref="catagory", lazy=True)


class product(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False)
    price = Column(DECIMAL, nullable=False)
    discription = Column(Text, nullable=False)
    discount = Column(Integer, nullable=False)
    image = Column(Text, nullable=False)
    created = Column(Date, default=datetime.today())
    catagory_id = Column(Integer, ForeignKey(catagory.id))
    receipt_detail = relationship("ReceiptDetail", backref="product", lazy=True)



class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(Date, default=datetime.today())
    customer_id =Column(Integer, ForeignKey(user.id))
    details = relationship("ReceiptDetail", backref="receipt", lazy=True)

class ReceiptDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id))
    product_id = Column(Integer, ForeignKey(product.id))
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)

ma = Marshmallow(app)
db.create_all()

class userSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'username', 'password', 'email', 'created')

User_Schema = userSchema()
User_Schemas = userSchema(many=True)