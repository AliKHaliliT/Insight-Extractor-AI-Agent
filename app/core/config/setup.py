from .settings import settings
from ...core.rate_limit.rate_limit_config import get_limiter
from ...core.rate_limit.rate_limiter_decorator import RateLimiterDecorator


class Setup:

    """

    Server setup.

    
    Usage
    -----
    The class instance must be used.

    """

    # Configure Limiter
    ## Global
    limiter = get_limiter(default_limits=settings.RATE_LIMITS)
    rate_limited = RateLimiterDecorator(limiter=limiter)


setup = Setup()