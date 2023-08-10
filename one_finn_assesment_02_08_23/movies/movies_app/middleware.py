from threading import Lock

class RequestCounterMiddleware:
    _counter = 0
    _lock = Lock()
    
    @classmethod
    def increment_counter(cls):
        with cls._lock:
            cls._counter += 1
    
    @classmethod
    def get_request_count(cls):
        with cls._lock:
            return cls._counter
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        self.increment_counter()
        response = self.get_response(request)
        return response
                        
    