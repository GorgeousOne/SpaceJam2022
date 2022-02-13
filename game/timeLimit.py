import datetime
import multiprocessing
from typing import List, Tuple


class TimeoutException(Exception):
	def __init__(self, msg=''):
		self.msg = msg


def worker(func, args: Tuple, result: List):
	"""
	Executes a function and adds it's return value to the given result list
	:param func:
	:param args:
	:param result:
	:return:
	"""
	result.append(func(*args))


def execute_limited(func, seconds: float, interval: float, args=()):
	"""
	Executes a function in a parallel process with a time limit for execution time.
	Throws :class:`TimeoutException` if time limit is exceeded
	:param func: function to execute
	:param args: function arguments
	:param seconds: approximately max time to wait for function to terminate
	:param interval: interval of seconds to check in for function to terminate
	:return: the functions return value
	"""
	return_val = []
	process = multiprocessing.Process(target=worker, args=(func, args, return_val))
	process.start()
	start_time = datetime.datetime.now()

	while datetime.datetime.now() - start_time < datetime.timedelta(seconds=seconds):
		process.join(interval)
		if not process.is_alive():
			return return_val[0] if len(return_val) > 0 else None
	process.terminate()
	raise TimeoutException('Function \'' + func.__name__ + '\' took longer than ' + str(seconds) + 's to execute.')


def infinite_loop():
	while True:
		pass


if __name__ == '__main__':
	execute_limited(infinite_loop, 1.0, 0.1)
