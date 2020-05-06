# -*- coding:utf8 -*-
from datetime import  datetime
from commons.logs import  get_logging_by_file
logger = get_logging_by_file(__file__)


class JobTraining:

    def __init__(self):
        self.task = None
        self.detail_task = None

    def do_job(self, task_id: int):
        logger.info("id: %s 任务开始",task_id )
        self.run_job()

    def run_job(self):
        pass


