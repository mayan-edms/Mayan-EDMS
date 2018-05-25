from .base import *  # NOQA

# Remove whitenoise from middlewares. Causes out of memory errors during test
# suit
MIDDLEWARE_CLASSES = [
    cls for cls in MIDDLEWARE_CLASSES if cls !='whitenoise.middleware.WhiteNoiseMiddleware'
]
