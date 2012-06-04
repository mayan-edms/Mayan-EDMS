import os

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


def _lazy_load(fn):
    _cached = []

    def _decorated():
        if not _cached:
            _cached.append(fn())
        return _cached[0]
    return _decorated


@_lazy_load
def load_backend():
    from converter.conf.settings import GRAPHICS_BACKEND as backend_name

    try:
        module = import_module('.base', 'converter.backends.%s' % backend_name)
        import warnings
        warnings.warn(
            "Short names for CONVERTER_BACKEND are deprecated; prepend with 'converter.backends.'",
            PendingDeprecationWarning
        )
        return module
    except ImportError, e:
        # Look for a fully qualified converter backend name
        try:
            return import_module('.base', backend_name)
        except ImportError, e_user:
            # The converter backend wasn't found. Display a helpful error message
            # listing all possible (built-in) converter backends.
            backend_dir = os.path.join(os.path.dirname(__file__), 'backends')
            try:
                available_backends = [f for f in os.listdir(backend_dir)
                        if os.path.isdir(os.path.join(backend_dir, f))
                        and not f.startswith('.')]
            except EnvironmentError:
                available_backends = []
            available_backends.sort()
            if backend_name not in available_backends:
                error_msg = ("%r isn't an available converter backend. \n" +
                    "Try using converter.backends.XXX, where XXX is one of:\n    %s\n" +
                    "Error was: %s") % \
                    (backend_name, ", ".join(map(repr, available_backends)), e_user)
                raise ImproperlyConfigured(error_msg)
            else:
                # If there's some other error, this must be an error in Mayan itself.
                raise


def cleanup(filename):
    """
    Tries to remove the given filename. Ignores non-existent files
    """
    try:
        os.remove(filename)
    except OSError:
        pass
