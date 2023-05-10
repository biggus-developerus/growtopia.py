__all__ = ("Config",)


class Config:
    """
    A class used to store configurations.

    Attributes
    ----------
    redis_namespace: str
        The namespace to use for Redis.
    """

    redis_namespace: str = "growtopia:"
