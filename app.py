from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from db1 import get_connection
from datetime import date

app = Flask(__name__)
app.secret_key = "mobile_shopping_change_this_secret"

# ---------------- DATABASE ----------------

def query(sql, params=None, fetch=False):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql, params or {})

        if fetch:
            return cursor.fetchall()

        conn.commit()
        return True

    finally:
        cursor.close()
        conn.close()


# ---------------- LOGIN REQUIRED ----------------

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))

        if session.get("role") != "ADMIN":
            flash("Admin permission required")
            return redirect(url_for("dashboard"))

        return func(*args, **kwargs)
    return wrapper


# ---------------- HOME ----------------

@app.route("/")
def home():
    return redirect(url_for("login"))


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        con = get_connection()
        cur = con.cursor()

        cur.execute("""
            SELECT USER_ID, USERNAME, PASSWORD, USER_ROLE
            FROM USERS
            WHERE UPPER(USERNAME) = UPPER(:username)
        """, {"username": username})

        user = cur.fetchone()

        cur.close()
        con.close()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["role"] = (user[3] or "").upper()

            return redirect(url_for("dashboard"))

        flash("Invalid username or password")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
@login_required
def dashboard():

    counts = {}

    tables = {
        "products": "PRODUCT",
        "users": "USERS",
        "customers": "CUSTOMER",
        "employees": "EMPLOYEE",
        "stock": "STOCK",
        "orders": "ORDERS"
    }

    for key, table in tables.items():
        result = query(
            f"SELECT COUNT(*) FROM {table}",
            fetch=True
        )
        counts[key] = result[0][0]

    return render_template(
        "dashboard.html",
        counts=counts
    )


# ---------------- PRODUCTS ----------------

@app.route("/products", methods=["GET", "POST"])
@login_required
def products():

    if request.method == "POST":

        product_id = int(request.form["product_id"])
        user_id = int(request.form["user_id"])
        name = request.form["product_name"]
        color = request.form.get("color") or None
        model = request.form.get("model") or None
        price = float(request.form["price"])

        query("""
            INSERT INTO PRODUCT
            (PRODUCT_ID, USER_ID, PRODUCT_NAME, COLOR, MODEL, PRICE)
            VALUES
            (:pid, :uid, :name, :color, :model, :price)
        """, {
            "pid": product_id,
            "uid": user_id,
            "name": name,
            "color": color,
            "model": model,
            "price": price
        })

        flash("Product added successfully")

        return redirect(url_for("products"))

    rows = query("""
        SELECT PRODUCT_ID, USER_ID, PRODUCT_NAME,
               COLOR, MODEL, PRICE
        FROM PRODUCT
        ORDER BY PRODUCT_ID
    """, fetch=True)

    return render_template("products.html", products=rows)


@app.route("/products/update/<int:pid>", methods=["POST"])
@login_required
def update_product(pid):

    query("""
        UPDATE PRODUCT
        SET USER_ID=:uid,
            PRODUCT_NAME=:name,
            COLOR=:color,
            MODEL=:model,
            PRICE=:price
        WHERE PRODUCT_ID=:pid
    """, {
        "uid": int(request.form["user_id"]),
        "name": request.form["product_name"],
        "color": request.form.get("color") or None,
        "model": request.form.get("model") or None,
        "price": float(request.form["price"]),
        "pid": pid
    })

    flash("Product updated")
    return redirect(url_for("products"))


@app.route("/products/delete/<int:pid>", methods=["POST"])
@admin_required
def delete_product(pid):

    query(
        "DELETE FROM PRODUCT WHERE PRODUCT_ID=:pid",
        {"pid": pid}
    )

    flash("Product deleted")
    return redirect(url_for("products"))


# ---------------- USERS ----------------

@app.route("/users", methods=["GET", "POST"])
@admin_required
def users():

    if request.method == "POST":

        password = generate_password_hash(
            request.form["password"]
        )

        query("""
            INSERT INTO USERS
            (USER_ID, USERNAME, PHONE, PASSWORD, USER_ROLE)
            VALUES
            (:uid, :username, :phone, :password, :role)
        """, {
            "uid": int(request.form["user_id"]),
            "username": request.form["username"],
            "phone": request.form.get("phone") or None,
            "password": password,
            "role": request.form["user_role"]
        })

        flash("User added successfully")
        return redirect(url_for("users"))

    rows = query("""
        SELECT USER_ID, USERNAME, PHONE, USER_ROLE
        FROM USERS ORDER BY USER_ID
    """, fetch=True)

    return render_template("users.html", users=rows)


@app.route("/users/delete/<int:uid>", methods=["POST"])
@admin_required
def delete_user(uid):

    query(
        "DELETE FROM USERS WHERE USER_ID=:uid",
        {"uid": uid}
    )

    flash("User deleted")
    return redirect(url_for("users"))


# ---------------- CUSTOMERS ----------------

@app.route("/customers", methods=["GET", "POST"])
@login_required
def customers():

    if request.method == "POST":

        query("""
            INSERT INTO CUSTOMER
            (CUSTOMER_ID, USER_ID, CUSTOMER_NAME,
             C_PHONE, C_ADDRESS)
            VALUES
            (:cid, :uid, :name, :phone, :address)
        """, {
            "cid": int(request.form["customer_id"]),
            "uid": int(request.form["user_id"]),
            "name": request.form["customer_name"],
            "phone": request.form.get("c_phone") or None,
            "address": request.form.get("c_address") or None
        })

        flash("Customer added")
        return redirect(url_for("customers"))

    rows = query("""
        SELECT CUSTOMER_ID, USER_ID, CUSTOMER_NAME,
               C_PHONE, C_ADDRESS
        FROM CUSTOMER ORDER BY CUSTOMER_ID
    """, fetch=True)

    return render_template("customer.html", customers=rows)


@app.route("/customers/delete/<int:cid>", methods=["POST"])
@admin_required
def delete_customer(cid):

    query(
        "DELETE FROM CUSTOMER WHERE CUSTOMER_ID=:cid",
        {"cid": cid}
    )

    flash("Customer deleted")
    return redirect(url_for("customers"))


# ---------------- EMPLOYEES ----------------

@app.route("/employees", methods=["GET", "POST"])
@admin_required
def employees():

    if request.method == "POST":

        query("""
            INSERT INTO EMPLOYEE
            (EMPLOYEE_ID, EMPLOYEE_NAME, E_PHONE, E_SALARY)
            VALUES
            (:eid, :name, :phone, :salary)
        """, {
            "eid": int(request.form["employee_id"]),
            "name": request.form["employee_name"],
            "phone": request.form.get("e_phone") or None,
            "salary": float(request.form["e_salary"])
            if request.form.get("e_salary") else None
        })

        flash("Employee added")
        return redirect(url_for("employees"))

    rows = query("""
        SELECT EMPLOYEE_ID, EMPLOYEE_NAME, E_PHONE, E_SALARY
        FROM EMPLOYEE ORDER BY EMPLOYEE_ID
    """, fetch=True)

    return render_template("employee.html", employees=rows)


@app.route("/employees/delete/<int:eid>", methods=["POST"])
@admin_required
def delete_employee(eid):

    query(
        "DELETE FROM EMPLOYEE WHERE EMPLOYEE_ID=:eid",
        {"eid": eid}
    )

    flash("Employee deleted")
    return redirect(url_for("employees"))


# ---------------- STOCK ----------------

@app.route("/stock", methods=["GET", "POST"])
@login_required
def stock():

    if request.method == "POST":

        query("""
            INSERT INTO STOCK
            (STOCK_ID, PRODUCT_ID, QUANTITY)
            VALUES (:sid, :pid, :qty)
        """, {
            "sid": int(request.form["stock_id"]),
            "pid": int(request.form["product_id"]),
            "qty": int(request.form["quantity"])
        })

        flash("Stock added")
        return redirect(url_for("stock"))

    rows = query("""
        SELECT STOCK_ID, PRODUCT_ID, QUANTITY
        FROM STOCK ORDER BY STOCK_ID
    """, fetch=True)

    return render_template("stock.html", stock=rows)


@app.route("/stock/delete/<int:sid>", methods=["POST"])
@admin_required
def delete_stock(sid):

    query(
        "DELETE FROM STOCK WHERE STOCK_ID=:sid",
        {"sid": sid}
    )

    flash("Stock deleted")
    return redirect(url_for("stock"))


# ---------------- ORDERS ----------------

@app.route("/orders", methods=["GET", "POST"])
@login_required
def orders():

    if request.method == "POST":

        query("""
            INSERT INTO ORDERS
            (ORDER_ID, CUSTOMER_ID, TOTAL_AMOUNT,
             EMPLOYEE_ID, ORDER_DATE, STATUS)
            VALUES
            (:oid, :cid, :amount, :eid, :order_date, :status)
        """, {
            "oid": int(request.form["order_id"]),
            "cid": int(request.form["customer_id"]),
            "amount": float(request.form["total_amount"]),
            "eid": int(request.form["employee_id"]),
            "order_date": date.fromisoformat(
                request.form["order_date"]
            ) if request.form.get("order_date") else None,
            "status": request.form.get("status") or None
        })

        flash("Order added")
        return redirect(url_for("orders"))

    rows = query("""
        SELECT ORDER_ID, CUSTOMER_ID, TOTAL_AMOUNT,
               EMPLOYEE_ID, ORDER_DATE, STATUS
        FROM ORDERS ORDER BY ORDER_ID
    """, fetch=True)

    return render_template("orders.html", orders=rows)


@app.route("/orders/delete/<int:oid>", methods=["POST"])
@admin_required
def delete_order(oid):

    query(
        "DELETE FROM ORDERS WHERE ORDER_ID=:oid",
        {"oid": oid}
    )

    flash("Order deleted")
    return redirect(url_for("orders"))


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)