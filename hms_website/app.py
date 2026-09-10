from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import db

app = Flask(__name__)
app.secret_key = "change-this-to-something-random"  # <-- change for production


# ---------------------------------------------------------------
# Access-control decorator
# ---------------------------------------------------------------
def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))
            if role and session.get("role") != role:
                flash("You don't have access to that page.")
                return redirect(url_for("index"))
            return f(*args, **kwargs)
        return wrapped
    return decorator


# ---------------------------------------------------------------
# Public landing page (Image 1 style) — hospital info + doctor list + booking
# ---------------------------------------------------------------
@app.route("/")
def index():
    search_query = request.args.get("q", "").strip()
    department_id = request.args.get("department_id", "").strip()

    sql = """
        SELECT d.doctor_id, d.first_name, d.last_name, d.specialization, dp.department_name
        FROM Doctors d
        LEFT JOIN Departments dp ON d.department_id = dp.department_id
        WHERE 1=1
    """
    params = []

    if search_query:
        # Match first name, last name, and the full "First Last" combo (so a search
        # for "John Smith" matches even though the two parts live in separate columns),
        # plus specialization and department.
        sql += """ AND (
                CONCAT(d.first_name, ' ', d.last_name) LIKE %s
                OR d.first_name LIKE %s
                OR d.last_name LIKE %s
                OR d.specialization LIKE %s
                OR dp.department_name LIKE %s
            )"""
        like = f"%{search_query}%"
        params.extend([like, like, like, like, like])

    if department_id:
        sql += " AND d.department_id = %s"
        params.append(department_id)

    # Only cap the list to 6 when the user hasn't searched/filtered for anything specific,
    # so the landing page stays uncluttered by default but a real search returns every match.
    if not search_query and not department_id:
        sql += " LIMIT 6"

    doctors = db.query(sql, tuple(params))

    departments = db.query("SELECT department_id, department_name FROM Departments ORDER BY department_name")

    return render_template(
        "landing.html",
        doctors=doctors,
        departments=departments,
        search_query=search_query,
        selected_department=department_id,
    )


@app.route("/book-appointment", methods=["POST"])
def book_appointment():
    doctor_id = request.form.get("doctor_id")
    date = request.form.get("date")
    time = request.form.get("time")
    reason = request.form.get("symptoms")

    if "user_id" not in session or session.get("role") != "Patient":
        # Remember what they were trying to book so we can finish it automatically
        # once they sign up or log in — no need to re-enter these details.
        session["pending_booking"] = {"doctor_id": doctor_id, "date": date, "time": time, "reason": reason}
        flash("Please log in or create a patient account to book an appointment.")
        return redirect(url_for("auth_choice"))

    _create_appointment(session["patient_id"], doctor_id, date, time, reason)
    flash("Appointment requested successfully!")
    return redirect(url_for("patient_dashboard"))


def _create_appointment(patient_id, doctor_id, date, time, reason):
    db.execute("""
        INSERT INTO Appointments (patient_id, doctor_id, appointment_date, appointment_time, status, reason_for_visit)
        VALUES (%s, %s, %s, %s, 'Scheduled', %s)
    """, (patient_id, doctor_id, date, time, reason))


def _complete_pending_booking():
    """If a booking was queued up before login/signup, create it now. Returns True if one was completed."""
    pending = session.pop("pending_booking", None)
    if pending and pending.get("doctor_id") and pending.get("date") and pending.get("time"):
        _create_appointment(session["patient_id"], pending["doctor_id"], pending["date"],
                             pending["time"], pending.get("reason"))
        return True
    return False


# ---------------------------------------------------------------
# Auth-choice page — shown when a guest tries to book without an account
# ---------------------------------------------------------------
@app.route("/get-started")
def auth_choice():
    return render_template("auth_choice.html")


# ---------------------------------------------------------------
# Auth
# ---------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = db.query("SELECT * FROM Users WHERE username = %s", (username,), fetchone=True)

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["user_id"]
            session["role"] = user["role"]
            session["username"] = user["username"]

            # attach the role-specific id (patient_id / doctor_id / admin_id) to the session
            if user["role"] == "Patient":
                p = db.query("SELECT patient_id, first_name FROM Patients WHERE user_id = %s",
                             (user["user_id"],), fetchone=True)
                session["patient_id"] = p["patient_id"]
                session["display_name"] = p["first_name"]
                if _complete_pending_booking():
                    flash("Logged in and your appointment was booked!")
                return redirect(url_for("patient_dashboard"))

            elif user["role"] == "Doctor":
                d = db.query("SELECT doctor_id, first_name FROM Doctors WHERE user_id = %s",
                             (user["user_id"],), fetchone=True)
                session["doctor_id"] = d["doctor_id"]
                session["display_name"] = d["first_name"]
                return redirect(url_for("doctor_dashboard"))

            elif user["role"] == "Admin":
                a = db.query("SELECT admin_id, first_name FROM Admins WHERE user_id = %s",
                             (user["user_id"],), fetchone=True)
                session["admin_id"] = a["admin_id"]
                session["display_name"] = a["first_name"]
                return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        dob = request.form["dob"]
        gender = request.form["gender"]
        blood_group = request.form.get("blood_group", "")
        address = request.form.get("address", "")
        emergency_name = request.form.get("emergency_contact_name", "")
        emergency_phone = request.form.get("emergency_contact_phone", "")

        existing = db.query("SELECT user_id FROM Users WHERE username = %s", (username,), fetchone=True)
        if existing:
            flash("That username is already taken — please choose another.")
            return render_template("signup.html")

        hashed = generate_password_hash(password)

        # 1. Create the login record
        user_id = db.execute("""
            INSERT INTO Users (username, password_hash, role, email, phone, is_active)
            VALUES (%s, %s, 'Patient', %s, %s, 1)
        """, (username, hashed, email, phone))

        # 2. Create the linked patient record
        patient_id = db.execute("""
            INSERT INTO Patients (user_id, first_name, last_name, dob, gender, blood_group,
                                   address, emergency_contact_name, emergency_contact_phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, first_name, last_name, dob, gender, blood_group,
              address, emergency_name, emergency_phone))

        # 3. Log them straight in
        session["user_id"] = user_id
        session["role"] = "Patient"
        session["username"] = username
        session["patient_id"] = patient_id
        session["display_name"] = first_name

        if _complete_pending_booking():
            flash("Account created and your appointment was booked!")
        else:
            flash("Account created! You can now book appointments.")
        return redirect(url_for("patient_dashboard"))

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ---------------------------------------------------------------
# Patient Dashboard (Image 2 style) — unique & interactive
# ---------------------------------------------------------------
@app.route("/patient/dashboard")
@login_required(role="Patient")
def patient_dashboard():
    patient_id = session["patient_id"]

    patient = db.query("SELECT * FROM Patients WHERE patient_id = %s", (patient_id,), fetchone=True)

    appointments = db.query("""
        SELECT a.*, d.first_name AS doc_fname, d.last_name AS doc_lname, d.specialization
        FROM Appointments a
        JOIN Doctors d ON a.doctor_id = d.doctor_id
        WHERE a.patient_id = %s
        ORDER BY a.appointment_date DESC
    """, (patient_id,))

    records = db.query("""
        SELECT mr.*, d.first_name AS doc_fname, d.last_name AS doc_lname
        FROM Medical_Records mr
        JOIN Doctors d ON mr.doctor_id = d.doctor_id
        WHERE mr.patient_id = %s
        ORDER BY mr.record_date DESC
    """, (patient_id,))

    prescriptions = db.query("""
        SELECT pr.*, mr.diagnosis, mr.record_date, d.first_name AS doc_fname, d.last_name AS doc_lname
        FROM Prescriptions pr
        JOIN Medical_Records mr ON pr.record_id = mr.record_id
        JOIN Doctors d ON mr.doctor_id = d.doctor_id
        WHERE mr.patient_id = %s
        ORDER BY mr.record_date DESC
    """, (patient_id,))

    bills = db.query("""
        SELECT * FROM Billing WHERE patient_id = %s ORDER BY bill_id DESC
    """, (patient_id,))

    upcoming_count = len([a for a in appointments if a["status"] == "Scheduled"])
    completed_count = len([a for a in appointments if a["status"] == "Completed"])
    pending_bills = len([b for b in bills if b["payment_status"] != "Paid"])

    return render_template(
        "patient_dashboard.html",
        patient=patient,
        appointments=appointments,
        records=records,
        prescriptions=prescriptions,
        bills=bills,
        upcoming_count=upcoming_count,
        completed_count=completed_count,
        pending_bills=pending_bills,
    )


@app.route("/patient/bill/<int:bill_id>/pay", methods=["POST"])
@login_required(role="Patient")
def pay_bill(bill_id):
    method = request.form.get("payment_method", "Card")

    bill = db.query("SELECT patient_id, payment_status FROM Billing WHERE bill_id = %s",
                     (bill_id,), fetchone=True)
    if not bill or bill["patient_id"] != session["patient_id"]:
        flash("Bill not found.")
        return redirect(url_for("patient_dashboard"))
    if bill["payment_status"] != "Pending":
        flash("This bill isn't awaiting payment.")
        return redirect(url_for("patient_dashboard") + "#billing")

    # The payment isn't marked Paid yet — it goes to the admin for confirmation first.
    db.execute("""
        UPDATE Billing SET payment_status = 'Awaiting Confirmation', payment_method = %s
        WHERE bill_id = %s
    """, (method, bill_id))

    flash("Payment submitted! It will be marked as Paid once the admin confirms it.")
    return redirect(url_for("patient_dashboard") + "#billing")


# ---------------------------------------------------------------
# Doctor Dashboard (simple, Image 3 style)
# ---------------------------------------------------------------
@app.route("/doctor/dashboard")
@login_required(role="Doctor")
def doctor_dashboard():
    doctor_id = session["doctor_id"]

    doctor = db.query("SELECT * FROM Doctors WHERE doctor_id = %s", (doctor_id,), fetchone=True)

    appointments = db.query("""
        SELECT a.*, p.first_name AS pat_fname, p.last_name AS pat_lname, mr.record_id
        FROM Appointments a
        JOIN Patients p ON a.patient_id = p.patient_id
        LEFT JOIN Medical_Records mr ON mr.appointment_id = a.appointment_id
        WHERE a.doctor_id = %s
        ORDER BY a.appointment_date DESC
    """, (doctor_id,))

    schedule = db.query("SELECT * FROM Doctor_Schedule WHERE doctor_id = %s", (doctor_id,))

    total = len(appointments)
    scheduled = len([a for a in appointments if a["status"] == "Scheduled"])
    completed = len([a for a in appointments if a["status"] == "Completed"])

    return render_template(
        "doctor_dashboard.html",
        doctor=doctor,
        appointments=appointments,
        schedule=schedule,
        total=total,
        scheduled=scheduled,
        completed=completed,
    )


@app.route("/doctor/appointment/<int:appointment_id>/update", methods=["POST"])
@login_required(role="Doctor")
def doctor_update_appointment(appointment_id):
    new_status = request.form.get("status")
    if new_status not in ("Scheduled", "Completed", "Cancelled"):
        flash("Invalid status.")
        return redirect(url_for("doctor_dashboard") + "#appointments")

    appt = db.query("SELECT doctor_id, patient_id FROM Appointments WHERE appointment_id = %s",
                     (appointment_id,), fetchone=True)
    if not appt or appt["doctor_id"] != session["doctor_id"]:
        flash("You can only update your own appointments.")
        return redirect(url_for("doctor_dashboard") + "#appointments")

    db.execute("UPDATE Appointments SET status = %s WHERE appointment_id = %s", (new_status, appointment_id))

    if new_status == "Completed":
        _ensure_bill_for_appointment(appointment_id, appt["patient_id"], session["doctor_id"])

    flash("Appointment status updated.")
    return redirect(url_for("doctor_dashboard") + "#appointments")


def _ensure_bill_for_appointment(appointment_id, patient_id, doctor_id):
    """Create a Pending bill for this appointment if one doesn't already exist."""
    existing = db.query("SELECT bill_id FROM Billing WHERE appointment_id = %s",
                         (appointment_id,), fetchone=True)
    if existing:
        return

    doctor = db.query("SELECT consultation_fee FROM Doctors WHERE doctor_id = %s",
                       (doctor_id,), fetchone=True)
    fee = doctor["consultation_fee"] if doctor and doctor["consultation_fee"] is not None else 0

    db.execute("""
        INSERT INTO Billing (patient_id, appointment_id, amount, payment_status)
        VALUES (%s, %s, %s, 'Pending')
    """, (patient_id, appointment_id, fee))


@app.route("/doctor/appointment/<int:appointment_id>/record", methods=["GET", "POST"])
@login_required(role="Doctor")
def doctor_add_record(appointment_id):
    appt = db.query("""
        SELECT a.*, p.first_name AS pat_fname, p.last_name AS pat_lname
        FROM Appointments a JOIN Patients p ON a.patient_id = p.patient_id
        WHERE a.appointment_id = %s
    """, (appointment_id,), fetchone=True)

    if not appt or appt["doctor_id"] != session["doctor_id"]:
        flash("You can only add records for your own appointments.")
        return redirect(url_for("doctor_dashboard") + "#appointments")

    # If a record already exists for this appointment, send them to the view page instead.
    existing = db.query("SELECT record_id FROM Medical_Records WHERE appointment_id = %s",
                         (appointment_id,), fetchone=True)
    if existing:
        return redirect(url_for("doctor_view_record", record_id=existing["record_id"]))

    if request.method == "POST":
        diagnosis = request.form["diagnosis"].strip()
        treatment = request.form.get("treatment", "").strip()
        notes = request.form.get("notes", "").strip()

        record_id = db.execute("""
            INSERT INTO Medical_Records (patient_id, doctor_id, appointment_id, diagnosis, treatment, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (appt["patient_id"], session["doctor_id"], appointment_id, diagnosis, treatment, notes))

        # Prescription is optional — only add it if a medicine name was actually entered.
        medicine_name = request.form.get("medicine_name", "").strip()
        if medicine_name:
            db.execute("""
                INSERT INTO Prescriptions (record_id, medicine_name, dosage, duration, instructions)
                VALUES (%s, %s, %s, %s, %s)
            """, (record_id, medicine_name, request.form.get("dosage", "").strip(),
                  request.form.get("duration", "").strip(), request.form.get("instructions", "").strip()))

        # Marking the record complete also marks the appointment Completed, so the two stay in sync.
        db.execute("UPDATE Appointments SET status = 'Completed' WHERE appointment_id = %s", (appointment_id,))
        _ensure_bill_for_appointment(appointment_id, appt["patient_id"], session["doctor_id"])

        flash("Medical record saved — the patient can now see it in their dashboard.")
        return redirect(url_for("doctor_dashboard") + "#appointments")

    return render_template("doctor_add_record.html", appt=appt)


@app.route("/doctor/record/<int:record_id>")
@login_required(role="Doctor")
def doctor_view_record(record_id):
    record = db.query("""
        SELECT mr.*, p.first_name AS pat_fname, p.last_name AS pat_lname
        FROM Medical_Records mr JOIN Patients p ON mr.patient_id = p.patient_id
        WHERE mr.record_id = %s
    """, (record_id,), fetchone=True)

    if not record or record["doctor_id"] != session["doctor_id"]:
        flash("Record not found.")
        return redirect(url_for("doctor_dashboard"))

    prescriptions = db.query("SELECT * FROM Prescriptions WHERE record_id = %s", (record_id,))

    return render_template("doctor_view_record.html", record=record, prescriptions=prescriptions)


# ---------------------------------------------------------------
# Admin Dashboard (simple, Image 3 style)
# ---------------------------------------------------------------
@app.route("/admin/dashboard")
@login_required(role="Admin")
def admin_dashboard():
    stats = {
        "patients": db.query("SELECT COUNT(*) AS c FROM Patients", fetchone=True)["c"],
        "doctors": db.query("SELECT COUNT(*) AS c FROM Doctors", fetchone=True)["c"],
        "appointments": db.query("SELECT COUNT(*) AS c FROM Appointments", fetchone=True)["c"],
        "pending_payments": db.query(
            "SELECT COUNT(*) AS c FROM Billing WHERE payment_status = 'Awaiting Confirmation'", fetchone=True
        )["c"],
    }

    doctors = db.query("""
        SELECT d.*, dp.department_name
        FROM Doctors d
        LEFT JOIN Departments dp ON d.department_id = dp.department_id
        ORDER BY d.first_name
    """)

    recent_appointments = db.query("""
        SELECT a.*, p.first_name AS pat_fname, p.last_name AS pat_lname,
               d.first_name AS doc_fname, d.last_name AS doc_lname
        FROM Appointments a
        JOIN Patients p ON a.patient_id = p.patient_id
        JOIN Doctors d ON a.doctor_id = d.doctor_id
        ORDER BY a.appointment_id DESC
        LIMIT 8
    """)

    status_counts = db.query("""
        SELECT status, COUNT(*) AS c FROM Appointments GROUP BY status
    """)

    revenue = db.query("""
        SELECT SUM(amount) AS total, payment_status
        FROM Billing GROUP BY payment_status
    """)

    return render_template(
        "admin_dashboard.html",
        stats=stats,
        doctors=doctors,
        recent_appointments=recent_appointments,
        status_counts=status_counts,
        revenue=revenue,
    )


@app.route("/admin/doctor/<int:doctor_id>")
@login_required(role="Admin")
def admin_doctor_detail(doctor_id):
    doctor = db.query("""
        SELECT d.*, dp.department_name
        FROM Doctors d LEFT JOIN Departments dp ON d.department_id = dp.department_id
        WHERE d.doctor_id = %s
    """, (doctor_id,), fetchone=True)

    if not doctor:
        flash("Doctor not found.")
        return redirect(url_for("admin_dashboard"))

    # Only the 5 most recent appointments for this doctor
    recent_appointments = db.query("""
        SELECT a.*, p.first_name AS pat_fname, p.last_name AS pat_lname
        FROM Appointments a
        JOIN Patients p ON a.patient_id = p.patient_id
        WHERE a.doctor_id = %s
        ORDER BY a.appointment_date DESC, a.appointment_time DESC
        LIMIT 5
    """, (doctor_id,))

    return render_template("admin_doctor_detail.html", doctor=doctor, appointments=recent_appointments)


@app.route("/admin/doctors/add", methods=["GET", "POST"])
@login_required(role="Admin")
def admin_add_doctor():
    departments = db.query("SELECT * FROM Departments ORDER BY department_name")

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        specialization = request.form["specialization"].strip()
        qualification = request.form.get("qualification", "").strip()
        experience_years = request.form.get("experience_years") or 0
        department_id = request.form.get("department_id") or None
        consultation_fee = request.form.get("consultation_fee") or 0
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        existing = db.query("SELECT user_id FROM Users WHERE username = %s", (username,), fetchone=True)
        if existing:
            flash("That username is already taken — please choose another.")
            return render_template("admin_add_doctor.html", departments=departments)

        hashed = generate_password_hash(password)
        user_id = db.execute("""
            INSERT INTO Users (username, password_hash, role, email, phone, is_active)
            VALUES (%s, %s, 'Doctor', %s, %s, 1)
        """, (username, hashed, email, phone))

        db.execute("""
            INSERT INTO Doctors (user_id, first_name, last_name, specialization, qualification,
                                  experience_years, department_id, consultation_fee)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, first_name, last_name, specialization, qualification,
              experience_years, department_id, consultation_fee))

        flash(f"Dr. {first_name} {last_name} was added successfully.")
        return redirect(url_for("admin_dashboard"))

    return render_template("admin_add_doctor.html", departments=departments)


@app.route("/admin/doctors/<int:doctor_id>/delete", methods=["POST"])
@login_required(role="Admin")
def admin_delete_doctor(doctor_id):
    doctor = db.query("SELECT user_id, first_name, last_name FROM Doctors WHERE doctor_id = %s",
                       (doctor_id,), fetchone=True)
    if not doctor:
        flash("Doctor not found.")
        return redirect(url_for("admin_dashboard"))

    try:
        # Deleting the Users row cascades to Doctors, Appointments, Medical_Records, Doctor_Schedule
        db.execute("DELETE FROM Users WHERE user_id = %s", (doctor["user_id"],))
        flash(f"Dr. {doctor['first_name']} {doctor['last_name']} was removed.")
    except Exception:
        flash("Couldn't remove this doctor — check if they're still set as a department head "
              "in the Departments table, then try again.")

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/search")
@login_required(role="Admin")
def admin_search():
    q = request.args.get("q", "").strip()
    patients, appointments = [], []

    if q:
        like = f"%{q}%"
        patients = db.query("""
            SELECT p.*, u.email, u.phone
            FROM Patients p JOIN Users u ON p.user_id = u.user_id
            WHERE CONCAT(p.first_name, ' ', p.last_name) LIKE %s
               OR u.email LIKE %s OR u.phone LIKE %s
            ORDER BY p.first_name
        """, (like, like, like))

        appointments = db.query("""
            SELECT a.*, p.patient_id, p.first_name AS pat_fname, p.last_name AS pat_lname,
                   d.first_name AS doc_fname, d.last_name AS doc_lname
            FROM Appointments a
            JOIN Patients p ON a.patient_id = p.patient_id
            JOIN Doctors d ON a.doctor_id = d.doctor_id
            WHERE CONCAT(p.first_name, ' ', p.last_name) LIKE %s
               OR CONCAT(d.first_name, ' ', d.last_name) LIKE %s
               OR a.status LIKE %s
               OR a.appointment_date LIKE %s
            ORDER BY a.appointment_date DESC
            LIMIT 30
        """, (like, like, like, like))

    return render_template("admin_search.html", q=q, patients=patients, appointments=appointments)


@app.route("/admin/patient/<int:patient_id>")
@login_required(role="Admin")
def admin_patient_detail(patient_id):
    patient = db.query("""
        SELECT p.*, u.email, u.phone, u.username
        FROM Patients p JOIN Users u ON p.user_id = u.user_id
        WHERE p.patient_id = %s
    """, (patient_id,), fetchone=True)

    if not patient:
        flash("Patient not found.")
        return redirect(url_for("admin_search"))

    appointments = db.query("""
        SELECT a.*, d.first_name AS doc_fname, d.last_name AS doc_lname
        FROM Appointments a JOIN Doctors d ON a.doctor_id = d.doctor_id
        WHERE a.patient_id = %s ORDER BY a.appointment_date DESC
    """, (patient_id,))

    records = db.query("""
        SELECT mr.*, d.first_name AS doc_fname, d.last_name AS doc_lname
        FROM Medical_Records mr JOIN Doctors d ON mr.doctor_id = d.doctor_id
        WHERE mr.patient_id = %s ORDER BY mr.record_date DESC
    """, (patient_id,))

    bills = db.query("SELECT * FROM Billing WHERE patient_id = %s ORDER BY bill_id DESC", (patient_id,))

    return render_template("admin_patient_detail.html", patient=patient,
                           appointments=appointments, records=records, bills=bills)


# ---------------------------------------------------------------
# Admin — payment confirmation
# ---------------------------------------------------------------
@app.route("/admin/payments")
@login_required(role="Admin")
def admin_payments():
    pending_confirmation = db.query("""
        SELECT b.*, p.first_name AS pat_fname, p.last_name AS pat_lname
        FROM Billing b JOIN Patients p ON b.patient_id = p.patient_id
        WHERE b.payment_status = 'Awaiting Confirmation'
        ORDER BY b.bill_id DESC
    """)

    recent_confirmed = db.query("""
        SELECT b.*, p.first_name AS pat_fname, p.last_name AS pat_lname
        FROM Billing b JOIN Patients p ON b.patient_id = p.patient_id
        WHERE b.payment_status = 'Paid'
        ORDER BY b.bill_id DESC
        LIMIT 10
    """)

    return render_template("admin_payments.html",
                           pending_confirmation=pending_confirmation,
                           recent_confirmed=recent_confirmed)


@app.route("/admin/payments/<int:bill_id>/confirm", methods=["POST"])
@login_required(role="Admin")
def admin_confirm_payment(bill_id):
    bill = db.query("SELECT payment_status FROM Billing WHERE bill_id = %s", (bill_id,), fetchone=True)
    if not bill:
        flash("Bill not found.")
        return redirect(url_for("admin_payments"))
    if bill["payment_status"] != "Awaiting Confirmation":
        flash("This bill isn't awaiting confirmation.")
        return redirect(url_for("admin_payments"))

    db.execute("""
        UPDATE Billing SET payment_status = 'Paid', payment_date = CURDATE() WHERE bill_id = %s
    """, (bill_id,))
    flash("Payment confirmed and marked as Paid.")
    return redirect(url_for("admin_payments"))


@app.route("/admin/payments/<int:bill_id>/reject", methods=["POST"])
@login_required(role="Admin")
def admin_reject_payment(bill_id):
    bill = db.query("SELECT payment_status FROM Billing WHERE bill_id = %s", (bill_id,), fetchone=True)
    if not bill:
        flash("Bill not found.")
        return redirect(url_for("admin_payments"))

    # Send it back to Pending so the patient can retry the payment.
    db.execute("""
        UPDATE Billing SET payment_status = 'Pending', payment_method = NULL WHERE bill_id = %s
    """, (bill_id,))
    flash("Payment rejected — the bill was reopened for the patient to retry.")
    return redirect(url_for("admin_payments"))


if __name__ == "__main__":
    app.run(debug=True)
