# property-service/src/models/__init__.py
"""
Property Service Models Package
Note: Since schemas are in models folder, importing them here too
"""

# Import existing models
from .models import *

# Import new models for points 6-10 (only if files exist)
try:
    from .map_models import *
except ImportError:
    pass

try:
    from .comparison_models import *
except ImportError:
    pass

try:
    from .loan_models import *
except ImportError:
    pass

try:
    from .rental_models import *
except ImportError:
    pass

# Import schemas (since they're in models folder)
try:
    from .property_schemas import *
except ImportError:
    pass