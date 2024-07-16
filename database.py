from dotenv import load_dotenv
load_dotenv()

# Regardless of the lint error you receive,
# load_dotenv must run before running this
# so that the environment variables are
# properly loaded.
from app import app, db
from app.models import Employee, Menu, MenuItem, MenuItemType, Table

with app.app_context():
    db.drop_all()
    db.create_all()

    # Use the password property to ensure it gets hashed
    employee = Employee(name="Margot", employee_number=1234, password="password")
    db.session.add(employee)
    db.session.commit()

    # Verify the stored hashed password
    stored_employee = Employee.query.filter_by(employee_number=1234).first()
    print(f"Stored hashed password: {stored_employee.hashed_password}")

    # Create instances of MenuItemType
    beverages = MenuItemType(name="Beverages")
    entrees = MenuItemType(name="Entrees")
    sides = MenuItemType(name="Sides")

    # Add the MenuItemType instances to the session and commit
    db.session.add(beverages)
    db.session.add(entrees)
    db.session.add(sides)
    db.session.commit()

    # Create an instance of Menu
    dinner = Menu(name="Dinner")

    # Create instances of MenuItem
    fries = MenuItem(name="French fries", price=3.50, type=sides, menu=dinner)
    drp = MenuItem(name="Dr. Pepper", price=1.0, type=beverages, menu=dinner)
    jambalaya = MenuItem(name="Jambalaya", price=21.98, type=entrees, menu=dinner)

    # Add the Menu and MenuItem instances to the session
    db.session.add(dinner)
    db.session.add(fries)
    db.session.add(drp)
    db.session.add(jambalaya)

    # Commit the session to the database
    db.session.commit()


# Create instances of Table
    tables = [Table(number=i, capacity=(i % 4) + 2) for i in range(1, 11)]

    # Add the Table instances to the session
    db.session.add_all(tables)
    db.session.commit()
