from app.choices import CustomEnum


class UserRole(CustomEnum):
    USER = "USER"
    ORG_ADMIN = "ORG_ADMIN"
    ORG_STAFF = "ORG_STAFF"
    ORG_HR = "ORG_HR"
    SUPER_ADMIN = "SUPER_ADMIN"
