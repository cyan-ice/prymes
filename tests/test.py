from functools import wraps
from asyncio import run, timeout
from prymes import *

class test:
    n = 0
    tests = []

    def __init__(self, times=1, timeout=1):
        test.n += 1
        self._id, self.times, self.timeout = test.n, times, timeout

    def __call__(self, f):
        @wraps(f)
        async def wrapper():
            print(end=f'Test #{self._id}: {f.__name__}... ')
            try:
                for _ in range(self.times):
                    async with timeout(self.timeout):
                        await f()
                print('Passed')
                return 0
            except TimeoutError:
                print('Failed: Timed Out')
                return 1
            except Exception as e:
                print(f'Failed: {e}')
                return 1
        test.tests.append(wrapper)
        return wrapper
    
    @classmethod
    async def execute_all(cls):
        s = cls.n
        for t in cls.tests:
            s -= await t()
        print(f'Passed {s}/{cls.n}')

@test()
async def primality_test_fixed():
    assert 480_194_653 in P
    assert 20_074_069 not in P
    assert 871_87753_77449 in P
    assert 865_17769_13431 not in P
    assert 3315_29345_21928_21991 in P
    assert 1152_96599_65919_97761 not in P

run(test.execute_all())