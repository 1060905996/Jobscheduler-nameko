from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime
import time
import os
from jobDispatcher import job_dispatcher
from commons.logs import  get_logging_by_file
from commons.db.dbUtils import load_task_list

logger = get_logging_by_file(__file__)


def evt_listener(event):
    if event.exception:
        logger.error('任务出错了！！！！！！')
        logger.error(event)
    else:
        pass


def load_jobs(server_id) -> []:
    logger.info('服务器id: %s' % server_id)
    logger.info('The time is: %s' % datetime.now())
    task_list = load_task_list()
    count = len(task_list)
    logger.info("获取任务数量 : %s", count)
    if count == 0:
        time.sleep(5)
    return task_list


def tick():
    logger.info('Tick! The time is: %s' % datetime.now())


jobstores = {
    'memory': MemoryJobStore()
}

executors = {
    'default': ThreadPoolExecutor(20),
    'threadpool': ThreadPoolExecutor(20)
}

job_defaults = {
    'coalesce': True,  # 积攒的任务只跑一次
    'max_instances': 100,  # 支持100个实例并发,积攒的任务排队，超出则警告到达上限
    'misfire_grace_time': 600  # 600秒的任务超时容错
}

if __name__ == '__main__':
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
    scheduler.add_listener(evt_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler._logger = logger
    scheduler.start()
    logger.info('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        while True:
            job_list = load_jobs('localhost_is_server_id')
            for j_id in job_list:
                scheduler.add_job(job_dispatcher, args=[j_id, ], id=str(j_id["id"]))
            time.sleep(20)

    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()



