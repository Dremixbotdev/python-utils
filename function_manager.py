"""Uses python decorators to execute function before and / or after a function has finished running.

Example:

  Code block: Python 3.6+  ## Hopefully If not, open an issue referencing this line
    
    from function_manager import function manager
    
    def a_random_function_to_run_before_foo():
      print('foo is going to get executed!')
     
    def a_random_function_to_run_after_foo():
      print('foo has executed!')
    
    @function_manager(before=a_random_function_to_run_before_foo, after=a_random_function_to_run_after_foo)
    def foo():
      print('Executing foo!')
      
"""


import functools


def function_manager(before=None,                # A function to run before executing func: If this is not a function, then it is ignored silently.
                     before_wait_for: int = 0,   # The time to delay running func after running before. 
                     after=None,                 # A function to run after executing func: If this is not a function, then it is ignored silently.
                     after_wait_for: int = 0):   # The time to delay running after after running func. # Sorry for understandable comments
  
  def inner(func):
    @functools.wraps
    def wrapper(*args, **kwargs):
      if before is not None and callable(before):
        before()
        time.sleep(before_wait_for)

      func(*args, **kwargs)

      if after is not None and callable(after):
        time.sleep(after_wait_for)
        after()
