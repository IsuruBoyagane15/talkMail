import sys
import threading
from builtins import super
import ctypes

if sys.version_info >= (3, 0):
    _thread_target_key = '_target'
    _thread_args_key = '_args'
    _thread_kwargs_key = '_kwargs'
else:
    _thread_target_key = '_Thread__target'
    _thread_args_key = '_Thread__args'
    _thread_kwargs_key = '_Thread__kwargs'


class ReturningThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self._return = None

    # overridden run
    def run(self):

        try:
            target = getattr(self, _thread_target_key)
            if target is not None:
                self._return = target(*getattr(self, _thread_args_key), **getattr(self, _thread_kwargs_key))
        finally:
            return None

    # overridden join
    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self._return

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    # raise a exception on thread
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

