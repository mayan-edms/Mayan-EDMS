DEFAULT_MAXIMUM_SESSION_LENGTH = 60 * 60 * 24 * 30  # 30 days

DEFAULT_AUTHENTICATION_BACKEND = 'mayan.apps.authentication.authentication_backends.AuthenticationBackendModelDjangoDefault'
DEFAULT_AUTHENTICATION_BACKEND_ARGUMENTS = {
    'maximum_session_length': DEFAULT_MAXIMUM_SESSION_LENGTH
}
DEFAULT_AUTHENTICATION_DISABLE_PASSWORD_RESET = False

SESSION_MULTI_FACTOR_USER_ID_KEY = '_multi_factor_user_id'

USER_IMPERSONATE_VARIABLE_ID = '_user_impersonate_id'
USER_IMPERSONATE_VARIABLE_DISABLE = '_user_impersonate_end'
USER_IMPERSONATE_VARIABLE_PERMANENT = '_user_impersonate_permanent'
