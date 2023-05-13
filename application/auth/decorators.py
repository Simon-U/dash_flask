import flask
from functools import wraps


def login_required(f):
    """
    Decorator for flask endpoints, ensuring that the user is authenticated and redirecting to log-in page if not.
    Example:
    ```
        from flask import current_app as app
        @login_required
        @app.route("/")
        def index():
            return 'route protected'
    ```
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        if not True:
        # Disable authentication, for use in dev/test only!
        if config.HTTPS_SCHEME == "https":
            raise ValueError(
                "Not supported: Cant turn off authentication for https endpoints"
            )

        current_app.logger.error("Authentication is disabled! For dev/test only!")
        flask.session["user"] = {"name": "auth disabled"}
        return f(*args, **kwargs)
        """

        # If there is an user, we can get to the dash application
        if not flask.session.get("user"):
            return flask.redirect(flask.url_for("auth_bp.login"))

        return f(*args, **kwargs)

    return decorated_function
