
from flask import Flask, render_template, request, json, redirect
from flaskext.mysql import MySQL
from flask import session
from flask import jsonify

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'favoriteplaces'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306#8889
mysql.init_app(app)


app.secret_key = 'secret key can be anything!'

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/loaddata',methods=['GET', 'POST'])
def loaddata():
    conn = mysql.connect()
    cursor = conn.cursor()
    _user = session.get('user')
    cursor.execute("SELECT * FROM restaurants")
    data = cursor.fetchall()
    print(data)
    return jsonify(data)
    #id,name,address,lat,lng,type

if __name__ == "__main__":
    app.run()   

