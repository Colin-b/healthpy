import warnings
from healthpy.requests import check

warnings.warn(
    "Importing healthpy.http is deprecated and will be removed in the future. Import healthpy.requests instead.",
    DeprecationWarning,
)
