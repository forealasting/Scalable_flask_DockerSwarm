import os
import threading

cmd1 = "sudo docker run --rm --cpus 0.3  --cpuset-cpus 12 --name service_1 flask"
cmd2 = "sudo docker run --rm --cpus 1  --cpuset-cpus 13 --name service_2 flask"
cmd3 = "sudo docker run --rm --cpus 1  --cpuset-cpus 14 --name service_3 flask"
cmd4 = "sudo docker run --rm --cpus 1  --cpuset-cpus 15 --name service_4 flask"


def thread_job(cmd):
    os.system(cmd)


thread1 = threading.Thread(target=thread_job, args=(cmd1, ))
thread2 = threading.Thread(target=thread_job, args=(cmd2, ))
thread3 = threading.Thread(target=thread_job, args=(cmd3, ))
thread4 = threading.Thread(target=thread_job, args=(cmd4, ))
thread1.start()
thread2.start()
thread3.start()
thread4.start()
