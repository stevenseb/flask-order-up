from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import Table, Employee, Order, OrderItem, MenuItem, MenuItemType
from app.forms import TableAssignmentForm, MenuItemAssignmentForm
from datetime import datetime

bp = Blueprint("orders", __name__)

@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    table_form = TableAssignmentForm()
    menu_form = MenuItemAssignmentForm()

    # Get the tables and open orders
    tables = Table.query.order_by(Table.number).all()
    open_orders = Order.query.filter(Order.end_time == None).all()

    # Get the table ids for the open orders
    busy_table_ids = [order.table_id for order in open_orders]

    # Filter the list of tables for only the open tables
    open_tables = [table for table in tables if table.id not in busy_table_ids]

    # Set choices for table assignment form
    table_form.tables.choices = [(t.id, f"Table {t.number}") for t in open_tables]
    table_form.servers.choices = [(e.id, e.name) for e in Employee.query.all()]

    # Query for menu items
    menu_items = MenuItem.query.join(MenuItemType).order_by(MenuItemType.name, MenuItem.name).all()
    menu_form.menu_item_ids.choices = [(item.id, f"{item.name} - ${item.price:.2f}") for item in menu_items]

    # Handle table assignment form submission
    if table_form.validate_on_submit() and table_form.assign.data:
        table_id = table_form.tables.data
        server_id = table_form.servers.data
        new_order = Order(table_id=table_id, employee_id=server_id)
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for("orders.index"))

    return render_template("orders.html", table_form=table_form, menu_form=menu_form, open_orders=open_orders, menu_items=menu_items, show_logout=False)

@bp.route("/close_order/<int:order_id>", methods=["POST"])
@login_required
def close_order(order_id):
    order = Order.query.get(order_id)
    if order:
        order.end_time = datetime.utcnow()
        db.session.commit()
    return redirect(url_for("orders.index"))

@bp.route("/add_items/<int:order_id>", methods=["POST"])
@login_required
def add_items(order_id):
    form = MenuItemAssignmentForm()
    menu_items = MenuItem.query.all()
    form.menu_item_ids.choices = [(item.id, f"{item.name} - ${item.price:.2f}") for item in menu_items]
    if form.validate_on_submit():
        for item_id in form.menu_item_ids.data:
            order_item = OrderItem(order_id=order_id, menu_item_id=item_id, quantity=1)
            db.session.add(order_item)
        db.session.commit()
    return redirect(url_for("orders.index"))

@bp.route("/remove_item/<int:order_item_id>", methods=["POST"])
@login_required
def remove_item(order_item_id):
    order_item = OrderItem.query.get(order_item_id)
    if order_item:
        db.session.delete(order_item)
        db.session.commit()
    return redirect(url_for("orders.index"))
