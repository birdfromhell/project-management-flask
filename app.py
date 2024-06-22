from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)
    
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur_client = mysql.connection.cursor()
    cur.execute('SELECT tb_m_project.*, tb_m_client.client_name FROM tb_m_project INNER JOIN tb_m_client ON tb_m_project.client_id = tb_m_client.client_id')
    cur_client.execute('SELECT * FROM tb_m_client')
    data = cur.fetchall()
    data_client = cur_client.fetchall()
    return render_template('index.html', projects=data, clients=data_client)

@app.route('/add_project', methods=['POST'])
def add_project():
    if request.method == 'POST':
        print("Form Data Received:", request.form)
        project_name= request.form ['project_name']
        client = request.form ['client']
        project_start = request.form ['project_start']
        status = request.form ['status']

        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO tb_m_project (project_name, client_id, project_start, project_status) VALUES(%s,%s,%s,%s)',
                    (project_name, client, project_start, status))
        mysql.connection.commit()
        flash('Project Berhasil Ditambahkan')

    return redirect(url_for('index'))

@app.route('/edit_project/<project_id>', methods=['POST'])
def edit_project(project_id):
    if request.method == 'POST':
        project_name= request.form ['project_name']
        client = request.form ['client']
        project_start = request.form ['project_start']
        project_end = request.form ['project_end']
        status = request.form ['status']
    
    cur=mysql.connection.cursor()
    sql = 'UPDATE tb_m_project SET project_name=%s, client_id=%s, project_start=%s, project_end=%s, project_status=%s WHERE project_id=%s'
    data = (project_name, client, project_start, project_end, status, project_id)
    cur.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('index'))


@app.route('/delete_project/<project_id>')
def delete_project(project_id):
    cur=mysql.connection.cursor()
    cur.execute(f'DELETE from tb_m_project WHERE project_id = {project_id}')
    mysql.connection.commit()
    flash('Project Berhasil Di hapus')
    return redirect(url_for('index'))

@app.route('/change_status/<project_id>')
def change_status(project_id):
    cur = mysql.connection.cursor()
    cur.execute(f'SELECT project_status FROM tb_m_project WHERE project_id = {project_id}')
    status = cur.fetchone()
    if status[0] == 'DONE':
        status = 'OPEN'
    elif status[0] == 'OPEN':
        status = 'DOING'
    else:
        status = 'DONE'
    cur.execute(f'UPDATE tb_m_project SET project_status = "{status}" WHERE project_id = {project_id}')
    mysql.connection.commit()
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(port=3000, debug=True)

