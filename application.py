from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///time.db")


@app.route("/")
def index():
    """View all time-off exchanges"""

    # select all history, joining employees and history tables, order by desc transact_id
    history = db.execute(
        "SELECT transact_id, fullname, hours, type, method, reason, start_date, end_date FROM history \
        JOIN employees ON history.employee_id = employees.id ORDER BY transact_id DESC")

    return render_template("index.html", history=history)


@app.route("/totals", methods=["GET", "POST"])
def totals():
    """ View UTO and PTO for any employee """

    # if GET, display employee drop-down
    if request.method == "GET":

        # get the current list of employees
        list = db.execute("SELECT fullname FROM employees")
        return render_template("total_get.html", list=list)

    # if POST, display that employee's time-off totals and request history
    if request.method == "POST":

        name = request.form.get("employee")

        # check for valid input
        if not name:
            return error("No employee selected")

        # select this employee's totals
        totals = db.execute("SELECT * FROM employees WHERE fullname = :name", name=name)

        # select this employee's history, joining employees and history tables, order by desc transact_id
        history = db.execute(
            "SELECT transact_id, fullname, hours, type, method, reason, start_date, end_date FROM history \
            JOIN employees ON history.employee_id = employees.id WHERE employees.fullname = :name ORDER BY transact_id DESC", name=name)

        return render_template("total_post.html", history=history, name=name, totals=totals)


@app.route("/employee", methods=["GET", "POST"])
def employee():
    """ Add a new employee """

    # if GET, display new employee form
    if request.method == "GET":
        return render_template("employee.html")

    # if POST, add new employee info to db
    else:
        # save form inputs
        fullname = request.form.get("fullname")
        eligible = request.form.get("eligible")
        start_pto = request.form.get("start_pto")

        # check for valid input
        if not fullname or not eligible or not start_pto:
            return error("Some employee information is missing")

        # Query database to see if employee already exists
        rows = db.execute("SELECT * FROM employees WHERE fullname = :fullname",
                          fullname=fullname)
        if len(rows) != 0:
            return error("An employee with this name already exists")

        # having passed all error checks, add new employee to db
        db.execute("INSERT INTO employees (fullname, eligible, start_pto, pto_left) VALUES (:fullname, :eligible, :start_pto, :start_pto)",
                   fullname=fullname, eligible=eligible, start_pto=start_pto)

        # alert user of success
        return success("New employee successfully added")


@app.route("/add", methods=["GET", "POST"])
def add():
    """ Add earned PTO """

    # if GET, display employee drop-down
    if request.method == "GET":

        # get the current list of employees
        list = db.execute("SELECT fullname FROM employees ORDER BY fullname")
        return render_template("add.html", list=list)

    # if POST, update databases
    else:

        # save input from form
        fullname = request.form.get("employee")
        hours = request.form.get("hours")
        reason = request.form.get("reason")

        # check for valid input
        if not fullname or not hours or not reason:
            return error("Some information is missing")

        # cast hours to int
        hours = int(hours)

        # get employee totals from employees database
        row = db.execute("SELECT * FROM employees WHERE fullname = :fullname", fullname=fullname)
        left = row[0]["pto_left"]
        earned = row[0]["pto_earned"]

        # add earned PTO to previous totals
        left += hours
        earned += hours

        # update employee database with total remaining PTO
        db.execute("UPDATE employees SET pto_left = :left, pto_earned = :earned WHERE fullname = :fullname",
                   left=left, earned=earned, fullname=fullname)

        # update history database
        db.execute("INSERT INTO history (employee_id, hours, type, method, reason) VALUES (:id, :hours, 'paid', 'added', :reason)",
                   id=row[0]["id"], hours=hours, reason=reason)

        return success("Employee PTO hours updated")


@app.route("/subtract", methods=["GET", "POST"])
def subtract():
    """ Subtract used PTO or UTO """

    # if GET method, display subtract form
    if request.method == "GET":

        # get the current list of employees
        list = db.execute("SELECT fullname FROM employees ORDER BY fullname")

        return render_template("subtract.html", list=list)

    else:
        # save form inputs
        fullname = request.form.get("employee")
        hours = request.form.get("hours")
        start = request.form.get("start")
        end = request.form.get("end")
        reason = request.form.get("reason")
        type = request.form.get("type")

        # check for valid input
        if not fullname or not hours or not start or not end or not type or not reason:
            return error("some information is missing")

        # cast hours to int
        hours = int(hours)

        # update employee's hour totals (paid or unpaid)
        row = db.execute("SELECT * FROM employees WHERE fullname = :fullname", fullname=fullname)

        # if paid time off
        if type == 'paid':
            left = row[0]["pto_left"]
            used = row[0]["pto_used"]

            # subtract hours from previous pto_left total, add hours to used total, update db
            left -= hours
            used += hours
            db.execute("UPDATE employees SET pto_left = :left, pto_used = :used WHERE fullname = :fullname",
                       left=left, used=used, fullname=fullname)

        # if unpaid time off
        if type == 'unpaid':
            used = row[0]["uto_used"]

            # add form hours to uto hours, update db
            used += hours
            db.execute("UPDATE employees SET uto_used = :used WHERE fullname = :fullname", used=used, fullname=fullname)

        # update history table
        db.execute("INSERT INTO history (employee_id, hours, type, method, reason, start_date, end_date) \
                   VALUES (:id, :hours, :type, 'subtracted', :reason, :start, :end)", id=row[0]["id"],
                   hours=hours, type=type, reason=reason, start=start, end=end)

        # success
        return success("Employee hours updated")


def error(message):
    """ Alert errors/ invalid inputs """
    return render_template("error.html", message=message)


def success(message):
    """ Alert information successfully updated """
    return render_template("success.html", message=message)