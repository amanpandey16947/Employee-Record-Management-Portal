from flask import (
    Flask, render_template, request, redirect, url_for, flash, session,
    make_response, send_from_directory
)
from flask import jsonify
from datetime import date
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import os
from functools import wraps
import io
from werkzeug.utils import secure_filename
import string
import secrets

# Optional Pillow import for image validation/normalization
try:
    from PIL import Image
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "replace-this-with-a-secure-random-value")

# Session configuration
app.permanent_session_lifetime = timedelta(hours=4)

# DB config (update if needed)
DB_HOST = "localhost"
DB_NAME = "DSTPL_emp"
DB_USER = "postgres"
DB_PASS = "aman"
DB_PORT = "5432"

# Upload config
ALLOWED_EXT = {"png", "jpg", "jpeg"}
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB


def _ensure_images_dir():
    images_dir = os.path.join(app.static_folder, "images")
    os.makedirs(images_dir, exist_ok=True)
    return images_dir


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )


def _generate_5char_id():
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(5))


def _generate_unique_filename(conn, ext):
    for _ in range(10):
        token = _generate_5char_id()
        filename = f"{token}.{ext}"
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM employee_info WHERE image = %s LIMIT 1;", (filename,))
        exists = cur.fetchone() is not None
        cur.close()
        if not exists:
            return filename
    return f"{secrets.token_hex(8)}.{ext}"


# -------------------- Utility / auth decorators --------------------
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Admin login required.", "danger")
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)
    return wrapper


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_email"):
            flash("Please sign in to continue.", "warning")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper
# ------------------------------------------------------------------


# -------------------- DB helpers ----------------------------------
def get_rows(status=None):
    """
    Return list of rows. If status is provided ('active' or 'inactive'),
    it will filter by work_status column.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        if status:
            cur.execute(
                "SELECT employee_id, name, designation, email, image, work_status "
                "FROM employee_info WHERE COALESCE(work_status,'active') = %s ORDER BY name;",
                (status,)
            )
        else:
            cur.execute(
                "SELECT employee_id, name, designation, email, image, work_status "
                "FROM employee_info ORDER BY name;"
            )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Database error in get_rows:", e)
        return []


def get_user_by_email(email):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM employee_info WHERE email = %s LIMIT 1;", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    except Exception as e:
        print("Database error in get_user_by_email:", e)
        return None


def get_user_by_id(employee_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM employee_info WHERE employee_id = %s LIMIT 1;", (employee_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    except Exception as e:
        print("Database error in get_user_by_id:", e)
        return None
# ------------------------------------------------------------------


@app.context_processor
def inject_current_year():
    return {"current_year": datetime.now().year}


# -------------------- Public routes --------------------------------
@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/employees")
def employees():
    """Simple public employees listing (active employees only)."""
    rows = get_rows(status="active")
    return render_template("employees.html", rows=rows)
# ------------------------------------------------------------------


# ---------------- Session helpers & user profile/logout -------------
def get_logged_in_user():
    email = session.get("user_email")
    if not email:
        return None
    return get_user_by_email(email)


@app.route("/profile")
@login_required
def profile_view():
    user = get_logged_in_user()
    if not user:
        session.pop("user_email", None)
        flash("User not found. Please login again.", "warning")
        return redirect(url_for("login"))

    resp = make_response(render_template("profile.html", user=user))
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    return resp


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("employees"))
# ------------------------------------------------------------------


# ---------------- Employee login ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    current_email = session.get("user_email")
    requested_email = request.args.get("email", "").strip()

    if current_email and (not requested_email or requested_email == current_email):
        return redirect(url_for("profile_view"))

    email_prefill = requested_email

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please provide both email and password.", "warning")
            return render_template("login.html", email=email)

        user = get_user_by_email(email)
        if not user:
            flash("No user found with that email.", "danger")
            return render_template("login.html", email=email)

        stored = user.get("pass_word")
        if stored is None or stored == "":
            flash("No password set for this user. Contact admin.", "danger")
            return render_template("login.html", email=email)

        if stored == password:
            session.clear()
            session.permanent = True
            session["user_email"] = email
            session["is_admin"] = False
            return redirect(url_for("profile_view"))
        else:
            flash("Incorrect password.", "danger")
            return render_template("login.html", email=email)

    resp = make_response(render_template("login.html", email=email_prefill))
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    return resp
# ------------------------------------------------------------------


# ---------------- Admin login / logout ----------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not email or not password:
            flash("Please enter admin email and password.", "warning")
            return render_template("admin_login.html")

        user = get_user_by_email(email)
        if not user:
            flash("Admin not found.", "danger")
            return render_template("admin_login.html")

        if str(user.get("admin")) not in ("1", "True", "true"):
            flash("You are not an admin.", "danger")
            return render_template("admin_login.html")

        stored = user.get("pass_word")
        if stored is None or stored == "":
            flash("Admin has no password set. Use DB to set initial password.", "danger")
            return render_template("admin_login.html")

        if stored == password:
            session.clear()
            session.permanent = True
            session["is_admin"] = True
            session["admin_email"] = email
            flash("Logged in as admin.", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Incorrect password.", "danger")
            return render_template("admin_login.html")

    resp = make_response(render_template("admin_login.html"))
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    return resp


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("Admin logged out.", "info")
    return redirect(url_for("admin_login"))
# ------------------------------------------------------------------


# ---------------- Admin: ex-employees listing (admin-only) ----------
@app.route("/admin/ex_employees")
@admin_required
def admin_ex_employees():
    rows = get_rows(status="inactive")
    return render_template("ex-employees.html", rows=rows)
# ------------------------------------------------------------------
# @app.route("/employees")
# def employees():
#     """Simple public employees listing (active employees only)."""
#     rows = get_rows(status="active")
#     return render_template("employees.html", rows=rows)



# ---------------- Admin: view ex-employee profile -------------------
# @app.route("/admin/view_ex_profile/<int:employee_id>")
# @admin_required
# def admin_view_ex_profile(employee_id):
#     user = get_user_by_id(employee_id)
#     if not user:
#         flash("User not found.", "danger")
#         return redirect(url_for("admin_ex_employees"))

#     resp = make_response(render_template("ex-profile.html", user=user))
#     resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
#     resp.headers["Pragma"] = "no-cache"
#     return resp
# ------------------------------------------------------------------

@app.route("/admin/view_ex_profile/<int:employee_id>")
@admin_required
def admin_view_ex_profile(employee_id):
    from_page = request.args.get("from_page", "")  # will be "admin_dashboard" when coming from dashboard
    user = get_user_by_id(employee_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("admin_ex_employees"))

    resp = make_response(render_template("ex-profile.html", user=user, from_page=from_page))
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    return resp
# ------------------------------------------------------------------
# ------------------------------------------------------------------




@app.route("/admin/mark_inactive/<int:employee_id>", methods=["POST"])
@admin_required
def admin_mark_inactive(employee_id):
    """
    Mark an employee as inactive and set leaving_date to today's date.
    Returns JSON: { success: True, redirect: '<url>' } on success,
    or { success: False, error: '...' } on failure.
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # check current status
        cur.execute("SELECT work_status FROM employee_info WHERE employee_id = %s LIMIT 1;", (employee_id,))
        row = cur.fetchone()
        if not row:
            return jsonify({"success": False, "error": "Employee not found."}), 404

        current = row.get("work_status") or "active"
        if str(current).lower() == "inactive":
            return jsonify({"success": False, "error": "Employee already inactive."}), 400

        today = date.today()
        cur.execute(
            "UPDATE employee_info SET work_status = %s, leaving_date = %s WHERE employee_id = %s;",
            ("inactive", today, employee_id)
        )
        conn.commit()

        # Return redirect (adjust if you'd rather send admin_ex_employees)
        return jsonify({"success": True, "redirect": url_for("admin_dashboard")})
    except Exception as e:
        print("Error in admin_mark_inactive:", e)
        return jsonify({"success": False, "error": "Server error while updating status."}), 500
    finally:
        try:
            if cur:
                cur.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass







# ---------------- Admin dashboard & helpers ------------------------
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "SELECT employee_id, name, email, admin, pass_word IS NOT NULL AND pass_word <> '' AS has_password "
            "FROM employee_info WHERE COALESCE(work_status, 'active') = 'active' ORDER BY name;"
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print("DB error admin_dashboard:", e)
        rows = []
    resp = make_response(render_template("admin_dashboard.html", rows=rows))
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    return resp


@app.route("/admin/set_password/<int:employee_id>", methods=["GET", "POST"])
@admin_required
def admin_set_password(employee_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT employee_id, name, email FROM employee_info WHERE employee_id = %s LIMIT 1;", (employee_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        print("DB error admin_set_password fetch:", e)
        user = None

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        new_pw = request.form.get("new_password", "")
        confirm = request.form.get("confirm_password", "")
        if not new_pw or not confirm:
            flash("Please provide and confirm the password.", "warning")
            return render_template("admin_set_password.html", user=user)
        if new_pw != confirm:
            flash("Passwords do not match.", "warning")
            return render_template("admin_set_password.html", user=user)

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("UPDATE employee_info SET pass_word = %s WHERE employee_id = %s;", (new_pw, employee_id))
            conn.commit()
            cur.close()
            conn.close()
            flash(f"Password set for {user['email']}.", "success")
            return redirect(url_for("admin_dashboard"))
        except Exception as e:
            print("DB error admin_set_password update:", e)
            flash("Database error while updating password.", "danger")
            return render_template("admin_set_password.html", user=user)

    resp = make_response(render_template("admin_set_password.html", user=user))
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    return resp
# ------------------------------------------------------------------


# ---------------- Admin: upload photo ------------------------------
@app.route("/admin/upload_photo/<int:employee_id>", methods=["GET", "POST"])
@admin_required
def admin_upload_photo(employee_id):
    if request.method == "GET":
        resp = make_response(render_template("admin_upload_photo.html", employee_id=employee_id))
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        resp.headers["Pragma"] = "no-cache"
        return resp

    f = request.files.get("photo")
    if not f:
        flash("No file uploaded.", "warning")
        return redirect(url_for("admin_upload_photo", employee_id=employee_id))

    if request.content_length and request.content_length > MAX_UPLOAD_SIZE:
        flash("File too large (max 5MB).", "warning")
        return redirect(url_for("admin_upload_photo", employee_id=employee_id))

    orig_name = secure_filename(f.filename or "")
    if "." not in orig_name:
        flash("Uploaded file must have an extension (e.g., .png or .jpg).", "warning")
        return redirect(url_for("admin_upload_photo", employee_id=employee_id))

    ext = orig_name.rsplit(".", 1)[1].lower()
    if ext not in ALLOWED_EXT:
        flash("Unsupported file type. Allowed: png, jpg, jpeg.", "warning")
        return redirect(url_for("admin_upload_photo", employee_id=employee_id))

    data = f.read()
    if len(data) == 0:
        flash("Empty file uploaded.", "warning")
        return redirect(url_for("admin_upload_photo", employee_id=employee_id))

    if len(data) > MAX_UPLOAD_SIZE:
        flash("File too large (max 5MB).", "warning")
        return redirect(url_for("admin_upload_photo", employee_id=employee_id))

    img = None
    if PIL_AVAILABLE:
        try:
            img = Image.open(io.BytesIO(data))
            img.verify()
            img = Image.open(io.BytesIO(data))
        except Exception as e:
            print("Pillow validation error:", e)
            img = None

    if not PIL_AVAILABLE and not f.mimetype.startswith("image/"):
        flash("Uploaded file is not a valid image.", "warning")
        return redirect(url_for("admin_upload_photo", employee_id=employee_id))

    final_ext = ext
    try:
        if img and getattr(img, "format", None):
            fmt = img.format.lower()
            if fmt == "jpeg":
                final_ext = "jpg"
            elif fmt in ALLOWED_EXT:
                final_ext = fmt
    except Exception:
        pass

    images_dir = _ensure_images_dir()

    try:
        conn = get_db_connection()
        final_filename = _generate_unique_filename(conn, final_ext)
        final_path = os.path.join(images_dir, final_filename)

        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT image FROM employee_info WHERE employee_id = %s LIMIT 1;", (employee_id,))
        old = cur.fetchone()
        old_filename = old.get("image") if old else None

        if img:
            try:
                if final_ext in ("jpg", "jpeg"):
                    if img.mode in ("RGBA", "LA"):
                        background = Image.new("RGB", img.size, (255, 255, 255))
                        background.paste(img.convert("RGBA"), mask=img.convert("RGBA").split()[3])
                        img_to_save = background
                    else:
                        img_to_save = img.convert("RGB")
                    img_to_save.save(final_path, format="JPEG", quality=85)
                else:
                    fmt_name = img.format or final_ext.upper()
                    img.save(final_path, format=fmt_name)
            except Exception as e:
                print("Error saving via Pillow:", e)
                with open(final_path, "wb") as out:
                    out.write(data)
        else:
            with open(final_path, "wb") as out:
                out.write(data)

        cur.execute("UPDATE employee_info SET image = %s WHERE employee_id = %s;", (final_filename, employee_id))
        conn.commit()

        try:
            if old_filename and old_filename != final_filename:
                old_path = os.path.join(images_dir, old_filename)
                if os.path.isfile(old_path):
                    os.remove(old_path)
        except Exception as e:
            print("Warning: couldn't remove old image:", e)

        cur.close()
        conn.close()
    except Exception as e:
        print("Error saving uploaded image / DB update:", e)
        flash("Server error saving image.", "danger")
        try:
            if os.path.isfile(final_path):
                os.remove(final_path)
        except Exception:
            pass
        return redirect(url_for("admin_upload_photo", employee_id=employee_id))

    flash(f"Photo uploaded and saved as {final_filename}.", "success")
    return redirect(url_for("admin_dashboard"))
# ------------------------------------------------------------------


@app.route("/employee/photo/<int:employee_id>")
def employee_photo(employee_id):
    images_dir = os.path.join(app.static_folder, "images")
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT image FROM employee_info WHERE employee_id = %s LIMIT 1;", (employee_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        print("DB error in employee_photo:", e)
        row = None

    filename = row.get("image") if row and row.get("image") else None
    if filename:
        candidate_path = os.path.join(images_dir, filename)
        if os.path.isfile(candidate_path):
            return send_from_directory(images_dir, filename, conditional=True)

    return redirect(url_for("static", filename="images/default_avatar.png"))
# ------------------------------------------------------------------


@app.after_request
def set_sensitive_headers(response):
    try:
        path = request.path or ""
        sensitive_paths = (
            "/login", "/admin/login", "/admin/dashboard", "/admin/set_password",
            "/profile", "/admin/upload_photo", "/admin"
        )
        if any(path.startswith(p) for p in sensitive_paths):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
    except Exception:
        pass
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
