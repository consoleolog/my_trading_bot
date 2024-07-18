import datetime
import logging
from traceback import format_exc
from _logging import set_loglevel

from schedule import Job, Scheduler


class SafeScheduler(Scheduler):
    set_loglevel("I")

    def __init__(self, logger: logging.Logger, rerun_immediately=True):
        self.logger = logger
        self.rerun_immediately = rerun_immediately
        super().__init__()

    def _run_job(self, job: Job):
        try:
            super()._run_job(job)

        except Exception as e:

            self.logger.error(f"Error : {e} , while {next(iter(job.tags))}...\n{format_exc()}")
            job.last_run = datetime.datetime.now()

            if not self.rerun_immediately:
                # Reschedule the job for the next time it was meant to run, instead of
                # letting it run
                # next tick
                job._schedule_next_run()
