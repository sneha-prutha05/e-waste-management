from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

paid_fines = set()


# ✅ Database connection function
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root43_prutha",
        database="ewaste_management"
    )

# 🏠 Home Page
@app.route('/')
def home():
    return render_template('home.html')

# 👤 Register User@app.route('/register_user', methods=['GET', 'POST'])
@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            user_type = request.form['user_type']

            # Connect to database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root43_prutha",
                database="ewaste_management",
                autocommit=True
            )
            cursor = connection.cursor()
            query = """
                INSERT INTO users (name, email, phone, address, user_type)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (name, email, phone, address, user_type)
            cursor.execute(query, values)

            # ✅ Get the auto-generated user_id
            user_id = cursor.lastrowid

            cursor.close()
            connection.close()

            # Pass both name and user_id to success page
            return render_template("success.html", name=name, user_id=user_id)

        except mysql.connector.Error as err:
            return f"Database Error: {err}"
        except Exception as e:
            return f"Error: {e}"

    # For GET request
    return render_template("register_user.html")


@app.route('/view_users')
def view_users():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root43_prutha",
            database="ewaste_management"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("view_users.html", users=users)
    except mysql.connector.Error as err:
        return f"Database Error: {err}"

# register items    
@app.route('/register_item', methods=['GET', 'POST'])
def register_item():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            item_name = request.form['item_name']
            item_type = request.form['item_type']
            condition_desc = request.form['condition_desc']

            connection = get_connection()
            cursor = connection.cursor()

            # ✅ Insert new item with default status = 'Pending'
            query = """
                INSERT INTO Ewaste_Items (user_id, item_name, item_type, condition_desc, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (user_id, item_name, item_type, condition_desc, 'Pending')
            cursor.execute(query, values)
            connection.commit()

            item_id = cursor.lastrowid
            cursor.close()
            connection.close()

            return render_template('success_item.html', item_name=item_name, item_id=item_id)

        except mysql.connector.Error as err:
            return f"Database Error: {err}"
        except Exception as e:
            return f"Error: {e}"

    # 🔹 GET request: show registration form
    return render_template('register_item.html')

# ---------------- VIEW REGISTERED ITEMS ----------------
@app.route('/view_items')
def view_items():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch all registered e-waste items
        cursor.execute("""
            SELECT e.item_id, e.user_id, u.name AS user_name, e.item_name, 
                   e.item_type, e.condition_desc, e.status, e.date_added
            FROM Ewaste_Items e
            JOIN Users u ON e.user_id = u.user_id
            ORDER BY e.date_added DESC
        """)
        items = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('view_items.html', items=items)
    except mysql.connector.Error as err:
        return f"Database Error: {err}"
    
    # ---------------- REGISTER RECYCLING CENTER ----------------
# ---------------- REGISTER RECYCLING CENTER ----------------
@app.route('/register_center', methods=['GET', 'POST'])
def register_center():
    if request.method == 'POST':
        try:
            center_name = request.form['center_name']
            location = request.form['location']
            contact_person = request.form['contact_person']
            phone = request.form['phone']
            email = request.form['email']

            connection = get_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO Recycling_Centers (center_name, location, contact_person, phone, email)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (center_name, location, contact_person, phone, email)
            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            return render_template('success_center.html', center_name=center_name)

        except mysql.connector.Error as err:
            return f"Database Error: {err}"
        except Exception as e:
            return f"Error: {e}"
        
            # 🔹 GET request
    return render_template('register_center.html')   
@app.route('/view_centers')
def view_centers():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT center_id, center_name, location, contact_person, phone, email
            FROM Recycling_Centers
            ORDER BY center_id DESC
        """)
        centers = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('view_centers.html', centers=centers)

    except mysql.connector.Error as err:
        return f"Database Error: {err}"

# ---------------- VIEW RECYCLER INFO ----------------
@app.route('/view_recyclers')
def view_recyclers():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT user_id, name, email, phone, address
            FROM Users
            WHERE user_type = 'Recycler'
            ORDER BY user_id DESC
        """)
        recyclers = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('view_recyclers.html', recyclers=recyclers)

    except mysql.connector.Error as err:
        return f"Database Error: {err}"
    
@app.route('/view_user_items')
def view_user_items():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root43_prutha",
            database="ewaste_management"
        )

        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                u.user_id, 
                u.name AS user_name, 
                u.phone AS contact, 
                i.item_id, 
                i.item_name, 
                i.item_type, 
                i.condition_desc, 
                i.status, 
                i.collection_confirm, 
                i.recycling_confirm, 
                i.date_added
            FROM users u
            JOIN ewaste_items i ON u.user_id = i.user_id
        """
        cursor.execute(query)
        records = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('view_user_items.html', records=records)

    except mysql.connector.Error as err:
        return f"Database Error: {err}"
    

# ✅ Fetch items to show in dropdown
def get_items():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT item_id, item_name FROM ewaste_items")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items

# ✅ Route to load main confirmation page
@app.route("/status_confirmation")
def status_confirmation():
    items = get_items()
    return render_template("status_confirmation.html", items=items)


# ✅ Route for Collection Confirmation (Citizen + Recycler)
@app.route("/confirm_collection", methods=["POST"])
def confirm_collection():
    item_id = request.form.get("item_id")
    confirm_type = request.form.get("confirm_type")
    citizen_id = request.form.get("citizen_id", "")
    recycler_id = request.form.get("recycler_id", "")
    message = ""

    conn = get_connection()
    cursor = conn.cursor()

    # Update based on who confirmed
    if confirm_type == "citizen":
        cursor.execute("""
            UPDATE ewaste_items
            SET citizen_confirm = 1, collection_confirm = 'Confirmed'
            WHERE item_id = %s
        """, (item_id,))
        message = f"✅ Citizen (ID {citizen_id}) confirmed collection for Item {item_id}."
    elif confirm_type == "recycler":
        cursor.execute("""
            UPDATE ewaste_items
            SET recycler_confirm = 1, collection_confirm = 'Confirmed'
            WHERE item_id = %s
        """, (item_id,))
        message = f"✅ Recycler (ID {recycler_id}) confirmed collection for Item {item_id}."

    conn.commit()

# ✅ Check if both citizen and recycler confirmed
    cursor.execute("""
        SELECT citizen_confirm, recycler_confirm 
        FROM ewaste_items WHERE item_id = %s
    """, (item_id,))
    result = cursor.fetchone()

    if result and result[0] == 1 and result[1] == 1:
        message = f"🎉 Item ID {item_id} collection confirmed successfully by both Citizen and Recycler!"

    cursor.close()
    conn.close()

    # Stay on same tab with fields retained
    return render_template(
        "status_confirmation.html",
        items=get_items(),
        message=message,
        selected_item=item_id,
        citizen_id=citizen_id,
        recycler_id=recycler_id,
        active_tab="collection"
    )


# ✅ Route for Recycling Confirmation (Recycler + Center)
@app.route("/confirm_recycling", methods=["POST"])
def confirm_recycling():
    item_id = request.form.get("item_id")
    confirm_type = request.form.get("confirm_type")
    recycler_id = request.form.get("recycler_id", "")
    center_id = request.form.get("center_id", "")
    message = ""

    conn = get_connection()
    cursor = conn.cursor()

    # Update based on who confirmed
    if confirm_type == "recycler":
        cursor.execute("""
            UPDATE ewaste_items
            SET recycler_recycle_confirm = 1, recycling_confirm = 'Confirmed'
            WHERE item_id = %s
        """, (item_id,))
        message = f"✅ Recycler (ID {recycler_id}) confirmed recycling for Item {item_id}."
    elif confirm_type == "center":
        cursor.execute("""
            UPDATE ewaste_items
            SET center_confirm = 1, recycling_confirm = 'Confirmed'
            WHERE item_id = %s
        """, (item_id,))
        message = f"✅ Center (ID {center_id}) confirmed recycling for Item {item_id}."

    conn.commit()

    # ✅ Check if both recycler and center confirmed
    cursor.execute("""
        SELECT recycler_recycle_confirm, center_confirm 
        FROM ewaste_items WHERE item_id = %s
    """, (item_id,))
    result = cursor.fetchone()

    if result and result[0] == 1 and result[1] == 1:
        cursor.execute("UPDATE ewaste_items SET status = 'Recycled' WHERE item_id = %s", (item_id,))
        conn.commit()
        message = f"♻️ Item ID {item_id} recycled successfully by Recycler and Center!"

    cursor.close()
    conn.close()

    # Render success message on same tab
    return render_template(
        "status_confirmation.html",
        items=get_items(),
        message=message,
        selected_item=item_id,
        recycler_id=recycler_id,
        center_id=center_id,
        active_tab="recycling"
    )
    
@app.route("/confirm_collection", methods=["POST"])
def audit_confirm_collection():
    item_id = request.form.get("item_id")
    confirm_type = request.form.get("confirm_type")
    citizen_id = request.form.get("citizen_id", "")
    recycler_id = request.form.get("recycler_id", "")
    message = ""

    conn = get_connection()
    cursor = conn.cursor()

    # ✅ Update main table
    if confirm_type == "citizen":
        cursor.execute("""
            UPDATE ewaste_items
            SET citizen_confirm = 1, collection_confirm = 'Confirmed'
            WHERE item_id = %s
        """, (item_id,))
        user_id = citizen_id
        message = f"✅ Citizen (ID {citizen_id}) confirmed collection for Item {item_id}."
    elif confirm_type == "recycler":
        cursor.execute("""
            UPDATE ewaste_items
            SET recycler_confirm = 1, collection_confirm = 'Confirmed'
            WHERE item_id = %s
        """, (item_id,))
        user_id = recycler_id
        message = f"✅ Recycler (ID {recycler_id}) confirmed collection for Item {item_id}."

    # ✅ Insert into ewaste_audit (for status change)
    cursor.execute("""
        INSERT INTO ewaste_audit (item_id, user_id, old_status, change_type)
        VALUES (%s, %s, 'Collected', 'UPDATE')
    """, (item_id, user_id))

    # ✅ Insert into item_log (for action history)
    cursor.execute("""
        INSERT INTO item_log (item_id, user_id, action)
        VALUES (%s, %s, %s)
    """, (item_id, user_id, message))

    conn.commit()
    cursor.close()
    conn.close()

    return render_template(
        "status_confirmation.html",
        items=get_items(),
        message=message,
        selected_item=item_id,
        citizen_id=citizen_id,
        recycler_id=recycler_id,
        active_tab="collection"
    )

@app.route("/confirm_recycling", methods=["POST"])
def audit_confirm_recycling():
    item_id = request.form.get("item_id")
    confirm_type = request.form.get("confirm_type")
    recycler_id = request.form.get("recycler_id", "")
    center_id = request.form.get("center_id", "")
    message = ""

    conn = get_connection()
    cursor = conn.cursor()

    # ✅ Update ewaste_items
    if confirm_type == "recycler":
        cursor.execute("""
            UPDATE ewaste_items
            SET recycler_recycle_confirm = 1, recycling_confirm = 'Confirmed'
            WHERE item_id = %s
        """, (item_id,))
        user_id = recycler_id
        message = f"✅ Recycler (ID {recycler_id}) confirmed recycling for Item {item_id}."
    elif confirm_type == "center":
        cursor.execute("""
            UPDATE ewaste_items
            SET center_confirm = 1, recycling_confirm = 'Confirmed', status = 'Recycled'
            WHERE item_id = %s
        """, (item_id,))
        user_id = center_id
        message = f"✅ Center (ID {center_id}) confirmed recycling for Item {item_id}."

    # ✅ Insert into ewaste_audit
    cursor.execute("""
        INSERT INTO ewaste_audit (item_id, user_id, old_status, change_type)
        VALUES (%s, %s, 'Recycled', 'UPDATE')
    """, (item_id, user_id))

    # ✅ Insert into item_log
    cursor.execute("""
        INSERT INTO item_log (item_id, user_id, action)
        VALUES (%s, %s, %s)
    """, (item_id, user_id, message))

    conn.commit()
    cursor.close()
    conn.close()

    return render_template(
        "status_success.html",
        items=get_items(),
        message=message,
        selected_item=item_id,
        recycler_id=recycler_id,
        center_id=center_id,
        active_tab="recycling"
    )

@app.route("/view_audit_log")
def view_audit_log():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM ewaste_audit ORDER BY changed_on DESC")
    ewaste_audit = cursor.fetchall()

    cursor.execute("SELECT * FROM item_log ORDER BY log_time DESC")
    item_log = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "view_audit_log.html",
        ewaste_audit=ewaste_audit,
        item_log=item_log
    )

# ✅ Booking page (book item)
@app.route("/bookings", methods=["GET", "POST"])
def bookings():
    message = ""

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        item_id = request.form.get("item_id")
        citizen_id = request.form.get("citizen_id", "")
        recycler_id = request.form.get("recycler_id", "")

        # Insert booking
        cursor.execute("""
            INSERT INTO bookings (item_id, citizen_id, recycler_id, booking_date, status)
            VALUES (%s, %s, %s, NOW(), 'Booked')
        """, (item_id, citizen_id, recycler_id))
        conn.commit()

        # Update item status
        cursor.execute("UPDATE ewaste_items SET status = 'Collected' WHERE item_id = %s", (item_id,))
        conn.commit()

        message = f"✅ Booking confirmed for Item ID {item_id}."

    # Fetch pending items
    cursor.execute("SELECT item_id, item_name FROM ewaste_items WHERE status = 'Pending'")
    items = cursor.fetchall()

    # Fetch all bookings
    cursor.execute("""
        SELECT b.booking_id, b.item_id, e.item_name, b.citizen_id, b.recycler_id,
               b.booking_date, b.status
        FROM bookings b
        JOIN ewaste_items e ON b.item_id = e.item_id
        ORDER BY b.booking_date DESC
    """)
    bookings = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("bookings.html", items=items, bookings=bookings, message=message)


# ✅ View Bookings page
@app.route("/view_bookings")
def view_bookings():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT b.booking_id, b.item_id, i.item_name, b.citizen_id, b.recycler_id,
               b.booking_date, b.status
        FROM bookings b
        JOIN ewaste_items i ON b.item_id = i.item_id
        ORDER BY b.booking_date DESC
    """)
    bookings = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("view_bookings.html", bookings=bookings)


# 🧠 Database Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root43_prutha",  # add your MySQL password if any
        database="ewaste_management"  # change to your DB name
    )

# 🧩 Function to calculate and insert fine automatically
def calculate_and_update_fines():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

# Get all bookings (assuming booking_date column exists)
    cursor.execute("SELECT user_id, item_id, booking_date FROM bookings")
    bookings = cursor.fetchall()

    for booking in bookings:
        booking_date = booking["booking_date"]
        days_passed = (datetime.now() - booking_date).days

        # Fine logic — Rs.10 per day after 7 days
        fine_amount = 0
        if days_passed > 7:
            fine_amount = (days_passed - 7) * 10

        if fine_amount > 0:
            # Check if fine already exists
            cursor.execute(
                "SELECT * FROM fine_records WHERE user_id=%s AND item_id=%s",
                (booking["user_id"], booking["item_id"]),
            )
            existing = cursor.fetchone()

            if not existing:
                cursor.execute(
                    "INSERT INTO fine_records (user_id, item_id, fine_amount) VALUES (%s, %s, %s)",
                    (booking["user_id"], booking["item_id"], fine_amount),
                )
                conn.commit()

    conn.close()







if __name__ == '__main__':
    app.run(debug=True)
