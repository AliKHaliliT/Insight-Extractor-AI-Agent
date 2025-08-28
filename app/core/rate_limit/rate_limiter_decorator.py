from collections.abc import Awaitable
import re
from typing import Callable

from slowapi.extension import Limiter


class RateLimiterDecorator:

    """

    Class-based custom decorator that applies rate limits to FastAPI endpoints and
    stores rate limit metadata for documentation.

    
    Usage:
    ------
    ```
    rate_limiter = RateLimiterDecorator(limiter)
    @rate_limiter("5/minute;1/hour;100/day")
    ```

    """

    def __init__(self, limiter: Limiter) -> None:

        """

        Constructor for the Rate Limiter Decorator class.
        

        Parameters
        ----------
        limiter : Limiter
            An instance of SlowAPI's Limiter used to enforce rate limits.

            
        Returns
        -------
        None.
        
        """

        if not isinstance(limiter, Limiter):
            raise TypeError(f"limiter must be a Limiter instance. Received: {limiter} with type {type(limiter)}")


        self.limiter = limiter


    def __call__(self, limit_str: str) -> Callable[[Callable], Callable[..., Awaitable]]:

        """

        Decorator interface that applies the rate limit and stores metadata.

        
        Parameters
        ----------
        limit_str : str
            Rate limit string. Use semicolon to seperate multiple limits for minute, hour, and day (e.g. "5/minute;1/hour;100/day")

            
        Returns
        -------
        rate_limiter_decorator : Callable
            A decorated route handler with rate limiting and metadata.

        """

        if not isinstance(limit_str, str) or not all(re.match(r"^\d+/(minute|hour|day)$", seg) for seg in limit_str.split(';')):
            raise TypeError(f"limit_str must be a string in the format '5/minute;1/hour;100/day'. Received: {limit_str} with type {type(limit_str)}")


        def _decorator(func: Callable) -> Callable:
            
            """

            Decorator function that applies the rate limit and stores metadata.
            
            
            Parameters
            ----------
            func : Callable
                The route handler to be decorated.

                
            Returns
            -------
            wrapped : Callable
                The decorated route handler with rate limiting and metadata.
            
            """

            if not isinstance(func, Callable):
                raise TypeError(f"func must be a callable. Received: {func} with type {type(func)}")


            wrapped = self.limiter.limit(limit_str)(func)
            setattr(wrapped, "__rate_limit__", limit_str)
            return wrapped
        

        return _decorator