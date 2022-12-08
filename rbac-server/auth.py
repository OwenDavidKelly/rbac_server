import mysql.connector
import bcrypt
import os

mydb = mysql.connector.connect(
  host=os.environ['DB_HOST'],
  user=os.environ['DB_USER'],
  password=os.environ['DB_PASSWORD'],
  database=os.environ['DB_NAME']
)

# Adds a new user to the database
def add_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    cursor = mydb.cursor(prepared=True)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)", (username, hashed_password))
    mydb.commit()
    return True

# Adds a role to the user, giving them access to that category
def add_user_role(user_id, role_id, read, write):
    cursor = mydb.cursor(prepared=True)
    cursor.execute("INSERT INTO user_role (user_id, role_id, r_access, w_access) VALUES (%s,%s,%s,%s)", (user_id, role_id, read, write))
    mydb.commit()
    return True

# Adds a new role to the database
def add_role(name):
    cursor = mydb.cursor(prepared=True)
    cursor.execute("INSERT INTO roles (name) VALUES (%s)", (name,))
    mydb.commit()
    return True

# Checks the given username and password match the ones stored in the database
def login(username, password):
    cursor = mydb.cursor(prepared=True)
    cursor.execute("SELECT uid, password FROM users WHERE username=%s", (username,))
    result = cursor.fetchall()
    if len(result) == 0:
        return {"status": False}
    if not bcrypt.checkpw(password.encode('utf8'), result[0][1].encode('utf8')):
        return {"status": False}
    return {"status": True, "uid": result[0][0]}

# Gets a list of all roles the user has access to, specified by either read or write access
def get_roles(user_id, rw):
    cursor = mydb.cursor(prepared=True)
    if rw == "read":
        cursor.execute("SELECT name FROM roles r INNER JOIN user_role ur ON r.id=ur.role_id WHERE user_id = %s and r_access = 1", (user_id,))
    elif rw == "write":
        cursor.execute("SELECT name FROM roles r INNER JOIN user_role ur ON r.id=ur.role_id WHERE user_id = %s and w_access = 1", (user_id,))
    result = cursor.fetchall()
    roles = []
    for entry in result:
        roles.append(entry[0])
    return roles

# Converts a role name into an id
def get_role_id(role):
    cursor = mydb.cursor(prepared=True)
    cursor.execute("SELECT id FROM roles WHERE name=%s", (role,))
    result = cursor.fetchall()
    if len(result) == 0:
        return -1
    else:
        return result[0][0]

