from .._json import error_envelope

NO_TOKEN = error_envelope(
    "not_configured",
    "No Duo credentials. Send the X-Duo-Ikey, X-Duo-Skey, and X-Duo-Api-Host headers.",
    False,
)
