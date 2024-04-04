import sqlite3
import random
import string

def generate_random_password(length=10):
    """Generate a random password."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_name():
    """Generate a random name."""
    first_names = ["John", "Alice", "Michael", "Emily", "David", "Emma", "Daniel", "Olivia", "James", "Sophia"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    return random.choice(first_names) + " " + random.choice(last_names)

def generate_username_from_name(name):
    """Generate a username from the given name."""
    first_name, last_name = name.lower().split()
    username = first_name[:6] + last_name[:2] + ''.join(random.choices(string.digits, k=3))
    return username

def generate_random_course():
    """Generate a random college course."""
    departments = ["CS", "MATH", "ENGL", "PHYS", "CHEM", "BIO", "HIST", "PSYC", "ART", "ECON"]
    levels = ["10{:02d}", "20{:02d}", "30{:02d}", "40{:02d}"]
    department = random.choice(departments)
    level = random.choice(levels).format(random.randint(1, 90))
    return f"{department}{level}"

def generate_random_grade():
    """Generate a random college letter grade."""
    grades = ['A', 'B', 'C', 'D', 'F']
    return random.choice(grades)

def create_users_table(cursor: sqlite3.Cursor):
    """Create users table."""
    cursor.execute('''CREATE TABLE users (
                        "id"	 INTEGER NOT NULL UNIQUE,
                        "username"	TEXT NOT NULL UNIQUE,
                        "password"	TEXT NOT NULL UNIQUE,
                        "name"	TEXT NOT NULL,
                        "admin"	INTEGER NOT NULL DEFAULT 0,
                        PRIMARY KEY("id" AUTOINCREMENT)
                    )''')

def create_classes_table(cursor: sqlite3.Cursor):
    """Create classes table."""
    cursor.execute('''CREATE TABLE IF NOT EXISTS classes (
                        "id"	INTEGER NOT NULL UNIQUE,
                        "class_code"	TEXT NOT NULL UNIQUE,
                        PRIMARY KEY("id")
                    )''')

def create_grades_table(cursor: sqlite3.Cursor):
    """Create grades table."""
    cursor.execute('''CREATE TABLE grades (
                        "user_id"	INTEGER,
                        "class_id"	INTEGER,
                        "grade"	TEXT CHECK(length("grade") < 3),
                        FOREIGN KEY("user_id") REFERENCES "users"("uid"),
                        FOREIGN KEY("class_id") REFERENCES "classes"("id")
                    )''')

def generate_random_users(num_users):
    """Generate a list of random users."""
    users = []
    for _ in range(num_users):
        real_name = generate_random_name()
        username = generate_username_from_name(real_name)
        password = generate_random_password()
        users.append({"id": random.randint(100, 1000), "username": username, "password": password, "name": real_name})
    return users

def generate_random_courses(num_courses):
    """Generate a list of random college courses."""
    courses = [(random.randint(1000, 90000), generate_random_course()) for _ in range(num_courses)]
    return courses

def select_random_classes(cursor: sqlite3.Cursor, num_classes):
    """Select random class ids from the classes table."""
    cursor.execute("SELECT id FROM classes")
    classes = cursor.fetchall()
    return random.sample(classes, min(num_classes, len(classes)))

def insert_random_users(cursor: sqlite3.Cursor, users):
    """Insert random users into the users table."""
    for user in users:
        cursor.execute("INSERT INTO users (id, username, password, name) VALUES (?, ?, ?, ?)",
                       (user["id"], user["username"], user["password"], user["name"]))

def insert_random_courses(cursor, courses):
    """Insert random courses into the classes table."""
    for course in courses:
        cursor.execute("INSERT INTO classes (id, class_code) VALUES (?, ?)", course)

def insert_grades_for_user(cursor: sqlite3.Cursor, user_id):
    """Insert grades for a user into the grades table."""
    num_grades = random.randint(10, 30)
    classes = select_random_classes(cursor, num_grades)
    for class_id in classes:
        grade = generate_random_grade()
        cursor.execute("INSERT INTO grades (user_id, class_id, grade) VALUES (?, ?, ?)", (user_id, class_id[0], grade))

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('db_authenticator.db')
    c = conn.cursor()

    # Drop existing tables
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS classes")
    c.execute("DROP TABLE IF EXISTS grades")

    # Create users, classes, and grades tables
    create_users_table(c)
    create_classes_table(c)
    create_grades_table(c)

    # Generate Admin User
    c.execute('INSERT OR REPLACE INTO "users" (id, username, password, name, admin) VALUES (91, "admin", "admin_pass", "admin account", 1)')
    # Generate random users and insert into users table
    random_users = generate_random_users(15)
    insert_random_users(c, random_users)

    # Generate random courses and insert into classes table
    try:
        random_courses = generate_random_courses(30)
        insert_random_courses(c, random_courses)
    except sqlite3.IntegrityError:
        try:
            random_courses = generate_random_courses(30)
            insert_random_courses(c, random_courses)
        except sqlite3.IntegrityError:
            random_courses = generate_random_courses(30)
            insert_random_courses(c, random_courses)

    # Insert grades for each user
    c.execute("SELECT id FROM users WHERE admin != 1")
    users = c.fetchall()
    for user_id in users:
        insert_grades_for_user(c, user_id[0])

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()