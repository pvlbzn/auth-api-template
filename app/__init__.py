import warnings

from authlib.deprecate import AuthlibDeprecationWarning

warnings.filterwarnings("ignore", message="authlib.jose module is deprecated", category=AuthlibDeprecationWarning)
