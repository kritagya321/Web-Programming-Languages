
from flask import Flask, render_template, request, json, redirect
from flaskext.mysql import MySQL
from flask import session
from flask import jsonify

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'TodoList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306#8889
mysql.init_app(app)



app.secret_key = 'secret key can be anything!'


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/showAddItem')
def showAddItem():
    return render_template('additem.html')


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        con = mysql.connect()
        cursor = con.cursor()
        

        cursor.execute("SELECT * FROM tbl_user WHERE email = %s", (_email))

        data = cursor.fetchall()


        if len(data) > 0:
            if str(data[0][3]) == _password:
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')


    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

    
@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
 
    # validate the received values
    if _name and _email and _password:

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO tbl_user(name, email, password) VALUES (%s, %s, %s)", (_name, _email, _password))
        

        data = cursor.fetchall()

        if len(data) == 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !'})
        else:
            return json.dumps({'error':str(data[0])})


    else:
        return json.dumps({'html':'<span>Enter the required fields!</span>'})


@app.route('/addItem',methods=['POST'])
def addItem():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO tbl_todo(title,description,userid) VALUES (%s,%s,%s)", (_title,_description,_user))

            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'An error Occured')
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route('/retrieve',methods=['GET', 'POST'])
def retrieve():
    conn = mysql.connect()
    cursor = conn.cursor()
    _user = session.get('user')
    cursor.execute("SELECT id,title,description,completed FROM tbl_todo WHERE userid =(%s)", _user)
    data = cursor.fetchall()
    return jsonify(data)
    #return render_template('userHome.html',context = data)  

    #render_template('userHome.html',user)
    
    #row_headers=[x[0] for x in cur.description] #this will extract row headers
    #####return json_data
@app.route('/deleteItem',methods=['POST'])
def deleteItem():
    try:
        idd = request.args['id']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_todo WHERE id = %s",idd)
        conn.commit()
        return render_template('userHome.html')
    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/updateCheck',methods=['GET'])
def updateCheck():
    print('The proram is here right now')
    id = request.args['id']
    print('The proram is here right now2 with id = ',id)
    newid = id[2:]
    print('The proram is here right now2 with id = ',newid)
    checked = request.args['checked']
    print('THe value of checked is :',checked)
    if checked == 'true':
        updateValue=1
    else:
        updateValue = 0
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE tbl_todo SET tbl_todo.completed = %s WHERE tbl_todo.id = %s",(updateValue,newid))
    conn.commit()
    return render_template('userHome.html')

@app.route('/editItem',methods=['POST'])
def editItem():
    print('The proram is here right now')
    id = request.args['id']
    print('The proram is here right now2 with id = ',id)
    newid = id[2:]
    _title = request.form['inputTitle']
    _description = request.form['inputDescription']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE tbl_todo SET tbl_todo.title = %s,tbl_todo.description = %s  WHERE tbl_todo.id = %s",(_title,_description,newid))
    conn.commit()
    return render_template('userHome.html')

@app.route('/closeEdit',methods=['POST'])
def closeEdit():
    return render_template('userHome.html')


if __name__ == "__main__":
    app.run()   

