from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'pedidos'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pendientes')
    data = cur.fetchall()
    return render_template('index.html', contacts=data)

@app.route('/add_pedido')
def add_pedido():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pendientes')
    data = cur.fetchall()
    return render_template('tomarPedido.html', pendientes=data)

    

@app.route('/add', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        cliente = request.form['cliente']
        telefono = request.form['telefono']
        fechaPedido = request.form['fechaPedido']
        fechaEntrega = request.form['fechaEntrega']
        tema = request.form['tema']
        direccionEntrega = request.form['direccionEntrega']
        observaciones = request.form['observaciones']
        cantidadPersonas = request.form['cantidadPersonas']
        panes = request.form['panes']
        tipoCubierta = request.form['tipoCubierta']
        saborPan = request.form['saborPan']
        relleno = request.form['relleno']
        costo = request.form['costo']
        anticipo = request.form['anticipo']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO pendientes (cliente, telefono, fechaPedido, fechaEntrega, tema, direccionEntrega, observaciones, cantidadPersonas, panes, tipoCubierta, saborPan, relleno, costo, anticipo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (cliente, telefono, fechaPedido, fechaEntrega, tema, direccionEntrega, observaciones, cantidadPersonas, panes, tipoCubierta, saborPan, relleno, costo, anticipo))
        mysql.connection.commit()
        flash('Contact Added Successfully')
        return redirect(url_for('add_pedido'))


@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pendientes WHERE id = %s', [id])
    data = cur.fetchall()
    return render_template('editar.html', contact=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        mysql.connection.commit()
        flash('Contact updated successfully')
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact removed succesfully')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
