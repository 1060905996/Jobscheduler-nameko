from nameko.standalone.rpc import ClusterRpcProxy
from commons.logs import  get_logging_by_file
logger = get_logging_by_file(__file__)
config = {'AMQP_URI': "amqp://guest:guest@localhost"}




def job_dispatcher(task):
    with ClusterRpcProxy(config) as rpc:
        print("分发任务,id = %d, task_name = %s",task["id"],task["task_name"])
        rpc["job_worker"].job_receive.call_async(task["id"])