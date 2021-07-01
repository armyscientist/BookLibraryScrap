from flask import Flask, request, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api=Api(app)
import mysql.connector

def connectDB():
    conn=mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='ma5t3rb1a5t3r',
            database='hnelibrary'
        )
    conn.autocommit=True
    #cursor=conn.cursor(buffered=True)
    return conn

@app.route("/")
class Auth(Resource):
    def post(self):
        conn=connectDB()
        cursor=conn.cursor(buffered=True)
        query="SELECT t1.password FROM tblmemberlogin AS t1 INNER JOIN tblmemberinfo AS t2 ON t1.MemberID = t2.MemberID WHERE t2.Email=%s;"
        #return str(type(request.form['email']))        
        cursor.execute(query, (request.form['email'],))        
        db_password=cursor.fetchone()
        
        if request.method == 'POST':
            if request.form['password'] !=  db_password:
                message={'message' : 'Invalid Credentials. Please try again.'}
            else:
                message={'message' : 'Logged in Successfully!'}
            return message
        conn.close()
        print(request.form.get())

api.add_resource(Auth, "/auth")


if __name__ == "__main__":
    app.run(debug=True)