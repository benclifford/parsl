import pytest

import parsl

from parsl.app.app import App
from parsl.tests.configs.local_threads import config

config.executors[0].tasks_per_block = 4
config.executors[0].init_blocks = 0
config.executors[0].min_blocks = 0
config.executors[0].max_blocks = 10
config.executors[0].parallelism = 0

parsl.clear()
parsl.load(config)


@App("python")
def python_app():
    import platform
    return "Hello from {0}".format(platform.uname())


@pytest.mark.skip('this test needs to be fixed or removed; it appears we do not expect it to complete')
def test_python(N=2):
    """No blocks provisioned if parallelism==0

    If I set init_blocks=0 and parallelism=0 I don't think any blocks will be provisioned.
    I tested and the script makes no progress. Perhaps we should catch this case and present an error to users.
    """

    results = {}
    for i in range(0, N):
        results[i] = python_app()

    print("Waiting ....")
    for i in range(0, N):
        print(results[0].result())


if __name__ == '__main__':

    parsl.set_stream_logger()
    test_python()
