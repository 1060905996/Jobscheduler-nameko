from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime
import time

from nameko.standalone.rpc import ClusterRpcProxy
config = {'AMQP_URI': "amqp://guest:guest@localhost"}


def evt_listener(event):
    if event.exception:
        print('error---------------')
    else:
        pass


def load_jobs():
    task_list=[]
    task_list.append({'id': datetime.now().strftime("%H_%M_%S")})
    time.sleep(1)
    task_list.append({'id': datetime.now().strftime("%H_%M_%S")})
    time.sleep(1)
    task_list.append({'id': datetime.now().strftime("%H_%M_%S")})
    time.sleep(1)
    task_list.append({'id': datetime.now().strftime("%H_%M_%S")})

    count = len(task_list)
    if count == 0:
        time.sleep(5)
    return task_list


def to_do_job(task_id):
    with ClusterRpcProxy(config) as rpc:
        result = rpc.task_worker.do_job.call_async(task_id)
        print(result)

jobstores = {
    'memory': MemoryJobStore()
}

executors = {
    'default': ThreadPoolExecutor(20),
    'threadpool': ThreadPoolExecutor(20)
}


if __name__ == '__main__':
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, timezone=utc)
    scheduler.add_listener(evt_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()
    try:
        while True:
            job_list = load_jobs()
            for j_id in job_list:
                print(j_id)
                scheduler.add_job(to_do_job, args=[j_id['id'], ], id=str(j_id['id']))
            time.sleep(10)
            print('scheduler--------------time sleep')

    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


