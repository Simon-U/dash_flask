# URLS for the application
# BASE = environ.get("BASE", "0.0.0.0")


class URL:
    BASE = "/"
    LOGIN = "/login"
    SIGNUP = "/signup"
    LOGOUT = "/logout"
    VERIFY_EMAIL = "/vefify-email/<token>"
    DASH = "/dash/"
