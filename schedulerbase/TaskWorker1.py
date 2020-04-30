from nameko.rpc import rpc


class TaskWorker1:

    name = "task_worker"

    @rpc
    def do_job(self, task_id):
        msg = "worker1 -  do_job:{0}".format(task_id)
        print(msg)
        return msg





