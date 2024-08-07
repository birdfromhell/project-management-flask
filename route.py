from flask import render_template, request, url_for, redirect, flash, session
from flask_login import login_user, login_required
from .app import app, mysql
from .models import User

@app.route('/')
@login_required
def index():
        cur = mysql.connection.cursor()
        cur_client = mysql.connection.cursor()
        cur.execute("""SELECT tb_m_project.*, tb_m_client.client_name, DATE_FORMAT(project_start, "%d %b %Y") AS formatted_start, DATE_FORMAT(project_end, "%d %b %Y") AS formatted_end 
        FROM tb_m_project INNER JOIN tb_m_client ON tb_m_project.client_id = tb_m_client.client_id;""")
        cur_client.execute('SELECT * FROM tb_m_client')
        data = cur.fetchall()
        data_client = cur_client.fetchall()
        cur.close()
        cur_client.close()
        return render_template('index.html', projects=data, clients=data_client)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember') == 'on'
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            user_obj = User()
            user_obj.id = user[0]
            session.permanent = True
            login_user(user_obj,remember=remember)
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah!', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/add_project', methods=['POST'])
def add_project():
    if request.method == 'POST':
        print("Form Data Received:", request.form)
        project_name= request.form ['project_name']
        client = request.form ['client']
        status = request.form ['status']

        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO tb_m_project (project_name, client_id, project_status) VALUES(%s,%s,%s)',
                    (project_name, client, status))
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
        cur.execute(f'UPDATE tb_m_project SET project_status = "{status}", project_start = CURDATE() WHERE project_id = {project_id}')
    else:
        status = 'DONE'
        cur.execute(f'UPDATE tb_m_project SET project_status = "{status}", project_end = CURDATE() WHERE project_id = {project_id}')
    cur.execute(f'UPDATE tb_m_project SET project_status = "{status}" WHERE project_id = {project_id}')
    mysql.connection.commit()
    return redirect(url_for('index'))