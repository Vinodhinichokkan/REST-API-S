from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
'''
@app.route('/',methods=['GET'])
def home():
    return jsonify(
        {
            'name':'Vinodhini',
            'msg':'Welcome to our paradise'
        }

    )

'''
basedir=os.path.abspath(os.path.dirname(__file__))
#print(basedir)          
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_Key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100), unique=True)

    def __init__(self,name,contact):
        self.name=name
        self.contact=contact

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','contact')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

#Add New User

@app.route('/user',methods=['POST'])
def add_user():
    name=request.json['name']
    contact=request.json['contact']
    new_User=User(name,contact)
    db.session.add(new_User)
    db.session.commit()
    return user_schema.jsonify(new_User)
    

#show all User

@app.route('/User',methods=['GET'])
def getAllUser():
    all_Users=User.query.all()
    result=users_schema.dump(all_Users)
    return jsonify(result)

#show User by ID

@app.route('/User/<id>',methods=['GET'])
def getUserById(id):

    User=User.query.get(id)
    return user_schema.jsonify(User)

# update user by Id
  
@app.route('/User/<id>',methods=['PUT'])
def UpdateUser(id):

    User=User.query.get(id)
    name = request.json['name']
    contact= request.json['contact']
    User.name=name
    User.contact=contact
    db.session.commit()
    return user_schema.jsonify(User)

#Delete user by Id

@app.route('/User/<id>',methods=['Delete'])
def DeleteUserById(id):
     User=User.query.get(id)
     db.session.delete(User)
     db.session.commit()
     return user_schema.jsonify(User)






if __name__=='__main__':
    app.run(debug=True,port=5000)