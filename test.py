import time
from enum import Enum
import os
import psutil
from logger import log


class ResultTest(Enum):
    Passed = 1
    Failed = 2
    Interrupted = 3


class TestCase:
    def __init__(self, tc_id, name):
        self.tc_id = tc_id
        self.name = name

    def get_name(self):
        return self.name

    def get_tc_id(self):
        return self.tc_id

    def prep(self):
        log.debug("Prep started")

    def run(self):
        log.debug("Run started")

    def clean_up(self):
        log.debug("Clean_up started")

    def execute(self):
        """Test passed if run is True, failed if run is False, interupted due to an Exeption"""
        try:
            log.debug("Test case {}: {}".format(self.tc_id, self.name))
            self.prep()
            result_run = self.run()
            self.clean_up()

            log.info("Test result: {}\n".format("PASSED" if result_run else "FAILED"))

            return ResultTest.Passed if result_run else ResultTest.Failed

        except Exception as e:
            log.exception(e)
            log.info("Test result: INTERRUPTED\n")
            return ResultTest.Interrupted


class FileListTestCase(TestCase):
    def __init__(self, base_dir):
        self.base_dir = base_dir
        super().__init__(tc_id="01", name="file_list")

    def prep(self):
        """If current system time taken as an integer since the Unix Epoch is divisible by 2, return True."""
        super().prep()

        current_system_time = time.time()
        log.debug("Seconds since epoch (int) = {}".format(int(current_system_time)))
        if int(current_system_time) % 2 == 0:
            log.debug("Divisibility by 2: True")
        else:
            raise Exception("Divisibility by 2: False")

    def run(self):
        """List all files from directory."""
        super().run()

        list_files = []

        if not os.path.isdir(self.base_dir):
            log.error("Directory '{}' does not exist".format(self.base_dir))
            return False

        with os.scandir(self.base_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    list_files.append(entry.name)
            log.debug("List of files in the '{}' directory:\n{}".format(self.base_dir, list_files))
        return True

    def clean_up(self):
        pass


class RandomFileTestCase(TestCase):
    def __init__(self):
        self.file_name = 'random_data'
        self.required_memory = (1024.0 ** 3)
        self.required_file_size = int(1024.0 ** 2)
        super().__init__(tc_id="02", name="random_file")

    def prep(self):
        """Get RAM available for the process (2nd field). If memory > 1 GB, return True"""
        super().prep()

        available_memory = psutil.virtual_memory()[1]
        available_memory_gb = available_memory / (1024.0 ** 3)
        log.debug("RAM available for the process: {} GB, OK".format(available_memory_gb))
        if available_memory < self.required_memory:
            raise Exception("Not enough memory, requiered min. 1 GB")

    def run(self):
        """Create a binary file test of size 1024 KB with random content and close."""
        super().run()

        with open(self.file_name, 'wb') as f:
            f.write(os.urandom(self.required_file_size))
            log.debug("Random data written to the file")
            f.close()
            log.debug("File closed")

        file = os.path.exists(self.file_name)
        log.debug("File check: {}".format("file found" if file else "file not found"))
        if not file:
            return False

        file_size = os.path.getsize(self.file_name)
        log.debug("File size check: {}".format("OK" if self.required_file_size == file_size else "NOK"))
        return file_size == self.required_file_size

    def clean_up(self):
        """Remove the file."""
        super().clean_up()

        if os.path.exists(self.file_name):
            os.remove(self.file_name)
            log.debug("File removed")
            if os.path.exists(self.file_name):
                raise Exception("File was not removed")
