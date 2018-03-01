# from typing import List, Optional
#
# from config import Config, Ric
#
# import logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logger = logging.getLogger(__name__)
#
#
# class Job:
#     def __init__(self, timeout, action, periodicity):
#         self.periodicity = periodicity
#         self.action = action
#         self.timeout = timeout
#
#     def callback(self, bot, job):
#         self.action(bot, job)
#
#
# class ScheduleManager:
#     def __init__(self, config: Config):
#         self.config = config
#
#     def create_jobs(self) -> List[Job]:
#         jobs = []
#         for channel in self.config.get_channels():
#             for public in channel.get_publications():
#                 job = self.get_publisher(channel.get_address(), public.get_schedule(), public.get_rics())
#                 if job is not None:
#                     jobs.append(job)
#         return jobs
#
#     def get_once_a_minute_publiser(self, address: str, rics: List[Ric]) -> Job:
#         def once_a_minute_publisher():
#             print(address)
#             print(rics)
#
#         return Job(5, once_a_minute_publisher, 10)
#
#     def get_publisher(self, address, schedule_name: str, rics: List[Ric]) -> Optional[Job]:
#         if schedule_name == "once_a_minute":
#             return self.get_once_a_minute_publiser(address, rics)
#         else:
#             logger.warning("Unsupported schedule {}!" % schedule_name)
#             return None
