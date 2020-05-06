from nameko.rpc import rpc
from jobTraining import JobTraining
from nameko.runners import ServiceRunner
from nameko.testing.utils import get_container


from commons.logs import  get_logging_by_file
logger = get_logging_by_file(__file__)

class jobWorker:

    name = "job_worker"

    @rpc
    def job_receive(self, task_id):
        logger.info("获取调度任务,id = %s",task_id)
        print(task_id)
        JobTraining().do_job(task_id)


config = {'AMQP_URI': "amqp://guest:guest@localhost"}
if __name__ == '__main__':
    runner = ServiceRunner(config=config)
    runner.add_service(jobWorker)
    runner.start()




