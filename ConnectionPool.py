class ConnectionPool:

    connectionPool = None

    def __new__(cls, *args, **kwargs):
        if cls.connectionPool is None:
            cls.connectionPool = super().__new__(cls, *args, **kwargs)
        return cls.connectionPool
