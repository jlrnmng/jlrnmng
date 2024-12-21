from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from mysql.connector import Error, errorcode
import configparser
from tabulate import tabulate

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database connection
connection = None
def connect_to_db():
    global connection
    try:
        db_config = read_db_config()
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print('Connected to MySQL Database')
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Error, Access Denied. Please check your username and password.')
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print('Error, Database does not Exist.')
        else:
            print(e)

# Read database configuration from config.ini
def read_db_config(filename='config.ini', section='mysql'):
    parser = configparser.ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception(f'{section} not found in the {filename} file.')
    return db

connect_to_db()

@app.route('/')
def index():
    tables = []
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
    except Error as e:
        flash(f"Error fetching tables: {str(e)}", 'danger')
    return render_template('index.html', tables=tables)

@app.route('/tables', methods=['GET'])
def list_tables():
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]  # Extract table names
        return render_template('tables.html', tables=tables)
    except Error as e:
        flash(f"Error fetching tables: {str(e)}", 'danger')
        return redirect('/')

@app.route('/view_data', methods=['POST'])
def view_data():
    table_name = request.form['table_name']
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        return render_template('index.html', tables=[], data=tabulate(data, headers=headers, tablefmt='html'))
    except Error as e:
        flash(f"Error fetching data: {str(e)}", 'danger')
    return redirect('/')

@app.route('/add_record', methods=['POST'])
def add_record():
    table_name = request.form['table_name']
    fields = request.form['fields'].split(',')
    values = request.form['values'].split(',')
    try:
        cursor = connection.cursor()
        query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(['%s']*len(values))})"
        cursor.execute(query, values)
        connection.commit()
        flash('Record added successfully!', 'success')
    except Error as e:
        flash(f"Error adding record: {str(e)}", 'danger')
    return redirect('/')

@app.route('/update_record', methods=['POST'])
def update_record():
    # Retrieve form inputs
    table_name = request.form.get('table_name')
    update_fields = request.form.get('update_fields', '').split(',')
    update_values = request.form.get('update_values', '').split(',')
    condition_field = request.form.get('condition_field')
    condition_value = request.form.get('condition_value')

    # Validate required fields
    if not table_name or not update_fields or not update_values or not condition_field or not condition_value:
        flash('All fields are required to update a record!', 'danger')
        return redirect('/')

    try:
        cursor = connection.cursor()
        # Construct the SQL query dynamically
        set_values = ', '.join([f"{field.strip()} = %s" for field in update_fields])
        query = f"UPDATE {table_name.strip()} SET {set_values} WHERE {condition_field.strip()} = %s"

        # Execute the query
        cursor.execute(query, (*[value.strip() for value in update_values], condition_value.strip()))
        connection.commit()

        flash('Record updated successfully!', 'success')
    except Error as e:
        flash(f"Error updating record: {str(e)}", 'danger')

    return redirect('/')

@app.route('/delete_record', methods=['POST'])
def delete_record():
    table_name = request.form['table_name']
    condition_field = request.form['condition_field']
    condition_value = request.form['condition_value']
    try:
        cursor = connection.cursor()
        query = f"DELETE FROM {table_name} WHERE {condition_field} = %s"
        cursor.execute(query, (condition_value,))
        connection.commit()
        flash('Record deleted successfully!', 'success')
    except Error as e:
        flash(f"Error deleting record: {str(e)}", 'danger')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
