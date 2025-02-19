import threading

# Thread-local storage to store the current user
_thread_locals = threading.local()

def set_current_user(user):
    """Store the current user in thread-local storage"""
    _thread_locals.user = user

def get_current_user():
    """Retrieve the current user from thread-local storage"""
    return getattr(_thread_locals, 'user', None)
