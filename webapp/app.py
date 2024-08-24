from flask import Flask, render_template_string
import psycopg2
import os

app = Flask(__name__)

# Подключение к базе данных PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'db'),
        database=os.getenv('POSTGRES_DB', 'mydb'),
        user=os.getenv('POSTGRES_USER', 'user'),
        password=os.getenv('POSTGRES_PASSWORD', 'password')
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, position, salary FROM employees')
    employees = cur.fetchall()
    cur.close()
    conn.close()
    
    # Оценка зарплаты
    result = []
    for emp in employees:
        if emp[2] <= 55000:
            salary_status = 'low'
        elif emp[2] <= 75000:
            salary_status = 'medium'
        else:
            salary_status = 'high'
        result.append((emp[0], emp[1], emp[2], salary_status))
    
    # HTML-шаблон для отображения данных
    template = '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Employee Salaries</title>
      </head>
      <body>
        <h1>Employee Salaries</h1>
        <table border="1">
          <tr>
            <th>Name</th>
            <th>Position</th>
            <th>Salary</th>
            <th>Status</th>
          </tr>
          {% for name, position, salary, status in employees %}
          <tr>
            <td>{{ name }}</td>
            <td>{{ position }}</td>
            <td>{{ salary }}</td>
            <td>{{ status }}</td>
          </tr>
          {% endfor %}
        </table>
      </body>
    </html>
    '''
    
    return render_template_string(template, employees=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

