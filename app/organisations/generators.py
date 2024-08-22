from app.utils import generate_code


def generate_staff_code():
    return generate_code('organisations', 'Organisation', 'staff_access_code', 3)
