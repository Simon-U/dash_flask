import dash_mantine_components as dmc


modalPasswordChange = dmc.Modal(
    id="modal-change-password",
    centered=True,
    zIndex=10000,
    children=[
        dmc.Stack(
            [
                dmc.PasswordInput(
                    label="Your old password",
                    placeholder="Your old password",
                    style={"width": 250},
                    id="old-password",
                ),
                dmc.PasswordInput(
                    label="Your new password",
                    description="Must be minimum 8 characters long, include a number, lower and upper letter and one special character",
                    placeholder="Your new password",
                    style={"width": 250},
                    id="new-password",
                ),
                dmc.PasswordInput(
                    label="Confirm your new password",
                    placeholder="Confirm your new password",
                    style={"width": 250},
                    id="confirm-new-password",
                ),
                dmc.Button(
                    "Change Password",
                    id="submitt-password-change",
                    className="btn btn-primary btn-block",
                    n_clicks=0,
                ),
            ],
        )
    ],
)
