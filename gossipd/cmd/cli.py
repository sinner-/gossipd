""" gossipd
"""
from multiprocessing import Process
from gossipd.process.daemon import Daemon
from gossipd.process.worker import Worker

def worker_process():
    """ worker
    """

    worker = Worker()
    worker.start()
    return

def main():
    """ main
    """

    Process(target=worker_process).start()
    gossipd = Daemon()
    gossipd.start()
