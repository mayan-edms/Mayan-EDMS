DEFAULT_AUTHENTICATION_BACKEND = 'mayan.apps.authentication.authentication_backends.AuthenticationBackendModelUsernamePassword'
DEFAULT_AUTHENTICATION_BACKEND_ARGUMENTS = {}

DEFAULT_AUTHENTICATION_DISABLE_PASSWORD_RESET = False
DEFAULT_MAXIMUM_SESSION_LENGTH = 60 * 60 * 24 * 30  # 30 days

USER_IMPERSONATE_VARIABLE_ID = '_user_impersonate_id'
USER_IMPERSONATE_VARIABLE_DISABLE = '_user_impersonate_end'
USER_IMPERSONATE_VARIABLE_PERMANENT = '_user_impersonate_permanent'
