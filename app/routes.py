import os
from flask import Blueprint, redirect, render_template, request, url_for
from datetime import datetime, timedelta
from app.forms import AppointmentForm
import sqlite3

bp = Blueprint('main', __name__)
DB_FILE = os.environ.get("DB_FILE")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@bp.route("/")
def main():
    d = datetime.now()
    return redirect(url_for(".daily", year=d.year, month=d.month, day=d.day))

@bp.route("/<int:year>/<int:month>/<int:day>", methods=["GET", "POST"])
def daily(year, month, day):
    form = AppointmentForm()
    if form.validate_on_submit():
        start_datetime = datetime.combine(form.start_date.data, form.start_time.data)
        end_datetime = datetime.combine(form.end_date.data, form.end_time.data)
        conn = get_db_connection()
        conn.execute("INSERT INTO appointments (name, start_datetime, end_datetime, description, private) VALUES (?, ?, ?, ?, ?)",
                     (form.name.data, start_datetime, end_datetime, form.description.data, form.private.data))
        conn.commit()
        conn.close()
        return redirect(url_for(".daily", year=year, month=month, day=day))

    conn = get_db_connection()
    start = datetime(year, month, day)
    end = start + timedelta(days=1)
    appointments = conn.execute("SELECT id, name, start_datetime, end_datetime, description FROM appointments WHERE start_datetime BETWEEN ? AND ? ORDER BY start_datetime",
                                (start, end)).fetchall()
    conn.close()

    # Convert appointment datetime strings to datetime objects
    appointments = [(appointment['id'], appointment['name'],
                     datetime.strptime(appointment['start_datetime'], '%Y-%m-%d %H:%M:%S'),
                     datetime.strptime(appointment['end_datetime'], '%Y-%m-%d %H:%M:%S'),
                     appointment['description']) for appointment in appointments]

    previous_day = start - timedelta(days=1)
    next_day = start + timedelta(days=1)
    return render_template("main.html", form=form, appointments=appointments, current_date=start, previous_day=previous_day, next_day=next_day)

@bp.route("/add_appointment", methods=["POST"])
def add_appointment():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    form = AppointmentForm()
    if form.validate_on_submit():
        start_datetime = datetime.combine(form.start_date.data, form.start_time.data)
        end_datetime = datetime.combine(form.end_date.data, form.end_time.data)
        conn = get_db_connection()
        conn.execute("INSERT INTO appointments (name, start_datetime, end_datetime, description, private) VALUES (?, ?, ?, ?, ?)",
                     (form.name.data, start_datetime, end_datetime, form.description.data, form.private.data))
        conn.commit()
        conn.close()
        return redirect(url_for(".daily", year=year, month=month, day=day))
    return redirect(url_for(".main"))

@bp.route("/edit_appointment", methods=["POST"])
def edit_appointment():
    id = request.args.get("id")
    form = AppointmentForm()
    if form.validate_on_submit():
        start_datetime = datetime.combine(form.start_date.data, form.start_time.data)
        end_datetime = datetime.combine(form.end_date.data, form.end_time.data)
        conn = get_db_connection()
        conn.execute("UPDATE appointments SET name = ?, start_datetime = ?, end_datetime = ?, description = ?, private = ? WHERE id = ?",
                     (form.name.data, start_datetime, end_datetime, form.description.data, form.private.data, id))
        conn.commit()
        conn.close()
        return redirect(url_for(".daily", year=start_datetime.year, month=start_datetime.month, day=start_datetime.day))
    return redirect(url_for(".main"))

@bp.route("/delete_appointment")
def delete_appointment():
    id = request.args.get("id")
    conn = get_db_connection()
    appointment = conn.execute("SELECT start_datetime FROM appointments WHERE id = ?", (id,)).fetchone()
    if appointment:
        start_datetime = datetime.strptime(appointment["start_datetime"], "%Y-%m-%d %H:%M:%S")
        conn.execute("DELETE FROM appointments WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for(".daily", year=start_datetime.year, month=start_datetime.month, day=start_datetime.day))
    return redirect(url_for(".main"))
