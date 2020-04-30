from nameko.rpc import rpc


class TaskWorker3:

    name = "task_worker"

    @rpc
    def do_job(self, task_id):
        return "worker3 -  do_job:{0}".format(task_id)


