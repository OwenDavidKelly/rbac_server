import pytest
import auth
import bcrypt

# Fixtures

@pytest.fixture
def one_user():
    hashed_password = bcrypt.hashpw("password_1".encode('utf8'), bcrypt.gensalt())
    cursor = auth.mydb.cursor(prepared=True)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)", ("user_1", hashed_password))
    auth.mydb.commit()
    yield cursor.lastrowid

@pytest.fixture
def del_user():
    yield "user_1"
    cursor = auth.mydb.cursor()
    cursor.execute("DELETE FROM users WHERE username=\"user_1\"")
    auth.mydb.commit()

@pytest.fixture
def one_role():
    cursor = auth.mydb.cursor()
    cursor.execute("INSERT INTO roles (name) VALUES (\"role_1\")")
    auth.mydb.commit()
    yield cursor.lastrowid

@pytest.fixture
def del_role():
    yield "role_1"
    cursor = auth.mydb.cursor()
    cursor.execute("DELETE FROM roles WHERE name=\"role_1\"")
    auth.mydb.commit()

# Unit Tests

def test_add_user(del_user):
    # Act
    auth.add_user("user_1", "password_1")

    # Assert
    cursor = auth.mydb.cursor()
    cursor.execute("SELECT username FROM users WHERE username=\"user_1\"")
    result = cursor.fetchall()
    assert result[0][0] == "user_1"

def test_add_role(del_role):
    # Act
    auth.add_role("role_1")

    # Assert
    cursor = auth.mydb.cursor()
    cursor.execute("SELECT name FROM roles WHERE name=\"role_1\"")
    result = cursor.fetchall()
    assert result[0][0] == "role_1"
    
@pytest.mark.parametrize("read, write", [
    (0, 0),
    (1, 0),
    (0, 1),
    (1, 1)
])
def test_add_user_role(read, write, one_user, del_user, one_role, del_role):
    # Act
    auth.add_user_role(one_user, one_role, read, write)

    # Assert
    cursor = auth.mydb.cursor()
    cursor.execute("SELECT role_id, r_access, w_access FROM user_role WHERE user_id=\"" + str(one_user) + "\"")
    result = cursor.fetchall()
    assert result[0][0] == one_role
    assert result[0][1] == read
    assert result[0][2] == write

def test_login_valid(one_user, del_user):
    # Act
    login = auth.login("user_1", "password_1")

    # Assert
    assert login["status"] == True
    assert login["uid"] == one_user

def test_login_invalid_password(one_user, del_user):
    # Act
    login = auth.login("user_1", "wrong_password")

    # Assert
    assert login["status"] == False

def test_login_invalid_user(one_user, del_user):
    # Act
    login = auth.login("wrong_user", "password_1")

    # Assert
    assert login["status"] == False

def test_get_role_id(one_role, del_role):
    # Assert
    assert auth.get_role_id("role_1") == one_role

@pytest.mark.parametrize("read, write", [
    (0, 0),
    (1, 0),
    (0, 1),
    (1, 1)
])
def test_get_roles(read, write, one_user, del_user, one_role, del_role):
    # Act
    auth.add_user_role(one_user, one_role, read, write)
    roles_r = auth.get_roles(one_user, "read")
    roles_w = auth.get_roles(one_user, "write")

    # Assert
    if read == 0:
        assert roles_r == []
    elif read == 1:
        assert "role_1" in roles_r
    if write == 0:
        assert roles_w == []
    elif write == 1:
        assert "role_1" in roles_w