class ConsistencyException(Exception):
    def __init__(self, message="ConsistencyException"):
        self.message = message
        super().__init__(self.message)