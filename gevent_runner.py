from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
from nornir.core.task import AggregatedResult, Task
from nornir.core.inventory import Host
from typing import List


#simple gevent runner. nothing fancy just using threading from gevent instead of concurrent.futures.
#
#see https://raw.githubusercontent.com/no-such-anthony/nornir3_play/master/gevent-runner-test.py
#for example usage, due to monkey patch likely best to have before any other imports/code.

class GeventRunner:

    def __init__(self, num_workers: int = 20) -> None:
        self.num_workers = num_workers

    def run(self, task: Task, hosts: List[Host]) -> AggregatedResult:

        result = AggregatedResult(task.name)
        greenlets = []

        pool = Pool(self.num_workers)
        for host in hosts:
            greenlet = pool.spawn(task.copy().start, host)
            greenlets.append(greenlet)        
        pool.join()

        for greenlet in greenlets:
            worker_result = greenlet.get()
            result[worker_result.host.name] = worker_result

        return result
