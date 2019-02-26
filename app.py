from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key="flash message"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'username'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'agendadb'

mysql = MySQL(app)

@app.route('/')
def Index():
    cur =mysql.connection.cursor()
    cur.execute("SELECT * FROM contactos")
    data =cur.fetchall()
    cur.close()
    return render_template('index.html' , contactos=data)

@app.route('/update',methods=['POST','GET'])
def update():
    if request.method =='POST':
        id_data = request.form['id']
        name = request.form['name']
        lastName = request.form['lastName']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        phoneType = request.form['phoneType']

        cur = mysql.connection.cursor()
        updateQuery = """
        UPDATE contactos 
        SET name = %s ,lastName = %s , address = %s , email = %s , phone = %s , phoneType = %s
        WHERE id = %s"""

        data=(name, lastName, address, email, phone, phoneType, id_data)
        cur.execute(updateQuery,data)
        mysql.connection.commit()

        flash("Data updated successfully")

        return redirect(url_for('Index'))


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        name = request.form['name']
        lastName = request.form['lastName']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        phoneType = request.form['phoneType']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contactos (Name,LastName,Address,Email,Phone,PhoneType) VALUES (%s,%s,%s,%s,%s,%s)",(name,lastName,address,email,phone,phoneType))
        mysql.connection.commit()

        flash("Data inserted succesfully")

        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>',methods=['POST','GET'])
def delete(id_data):
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM contactos WHERE id=%s",(id_data))
    mysql.connection.commit()

    flash("Data deleted succesfully")

    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run()
