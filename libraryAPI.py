from flask import Flask, request, jsonify, request
from flask_restful import Api, Resource
import mysql.connector

app = Flask(__name__)
api=Api(app)

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


@app.route("/auth", methods=['POST'])
def login():
    #if request.method == 'POST':
    
    conn=connectDB()
    cursor=conn.cursor(buffered=True)
    query="SELECT MemberID FROM tblmemberinfo WHERE email=%s;"
    cursor.execute(query, (request.form['email'],))    
    
    message="no user" 
    memberID=cursor.fetchone()
    if(memberID):         
        message=''
        memberID=memberID[0]
       
        query="SELECT password FROM tblmemberlogin WHERE MemberID=%s;"
        #return str(type(request.form['email']))        
        cursor.execute(query, (memberID,))
        db_password=cursor.fetchone()
        if(db_password):                            
            
            query="SELECT MemberName, MemberType, Phone, Gender FROM tblmemberinfo WHERE MemberID=%s;"
            cursor.execute(query,(memberID,))                 
            for row in cursor:
                #print(row, type(row))
                for column in row:
                    if(column):
                        message+=column+'|'
                    else:
                        message+='null|'
            message=message[:-1]   
        else:
            message="invalid"       
    conn.close()
    return message
        
    
@app.route("/register", methods=['POST'])
def register():
    conn=connectDB()
    cursor=conn.cursor(buffered=True)
    query="SELECT email from tblmemberinfo WHERE email=%s"
    cursor.execute(query,(request.form['email'],))
    if(not cursor.fetchone()):
        query="SELECT count(*) FROM tblmemberinfo;"
        cursor.execute(query)
        count=cursor.fetchone()[0]

        query="INSERT INTO tblmemberinfo (Memberid, MemberName, Email, Mobile, Gender, Address, City, Age, Occupation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(query,(count+1, request.form['membername'],request.form['email'],request.form['mobile'],request.form['gender'],
                                request.form['address'],request.form['city'],request.form['age'],request.form['occupation'],))
        query="INSERT INTO tblmemberlogin (memberid, password) VALUES (%s, %s)"
        cursor.execute(query,(count+1, request.form['password']))
        return "registered"
    return jsonify({"message":"already registered"})

@app.route("/search", methods=['GET'])
def books_search():
    pass
    
       
            

#api.add_resource(Auth, "/auth")
#api.add_resource(Register, "/register")
#api.add_resource(SearchBooks, "/search")


if __name__ == "__main__":
    app.run(debug=True)