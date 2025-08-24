
from flask import Flask, render_template,request, redirect, url_for, flash, session

from db_config import get_connection

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/borrow')
def borrow():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Borrow")
    data = cursor.fetchall()
    conn.close()
    return render_template('borrow.html', records=data)

@app.route('/staff')
def staff():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Staff")
    data = cursor.fetchall()
    conn.close()
    return render_template('staff.html', staff=data)
@app.route('/books')
def view_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return render_template('books.html', books=books)

@app.route('/members')
def view_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    conn.close()
    return render_template('members.html', members=members)
@app.route('/books', methods=['GET', 'POST'])
def search_books():
    results = []
    if request.method == 'POST':
        title = request.form['title']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Books WHERE Title LIKE %s"
        cursor.execute(query, ('%' + title + '%',))
        results = cursor.fetchall()
        conn.close()
    return render_template('books.html', results=results)
@app.route('/members', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Members (Name, Email, Phone) VALUES (%s, %s, %s)", (name, email, phone))
        conn.commit()
        conn.close()
        return redirect('/members')
    return render_template('members.html')
@app.route('/borrow', methods=['GET', 'POST'])
def borrow_form():
    message = ""
    if request.method == 'POST':
        member_id = request.form['member_id']
        book_id = request.form['book_id']
        borrow_date = request.form['borrow_date']
        return_date = request.form['return_date']

        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Borrow (MemberID, BookID, BorrowDate, ReturnDate)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (member_id, book_id, borrow_date, return_date))
        conn.commit()
        conn.close()
        message = "Borrow record added successfully!"

    return render_template('borrow.html', message=message)
@app.route('/staff', methods=['GET', 'POST'])
def staff_page():
    message = ""
    records = []

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        email = request.form['email']
        phone = request.form['phone']
        join_date = request.form['join_date']

        query = """
            INSERT INTO Staff (Name, Role, Email, Phone, JoinDate)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, role, email, phone, join_date))
        conn.commit()
        message = "Staff member added successfully!"

    cursor.execute("SELECT * FROM Staff ORDER BY JoinDate DESC LIMIT 10")
    records = cursor.fetchall()
    conn.close()

    return render_template('staff.html', message=message, records=records)
if __name__ == '__main__':
    app.run(debug=True)