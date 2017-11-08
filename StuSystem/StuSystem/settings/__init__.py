try:
    from StuSystem.settings.prod import *
except ImportError:
    try:
        from StuSystem.settings.test import *
    except ImportError:
        from StuSystem.settings.dev import *