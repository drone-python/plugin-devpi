import os
import time
import unittest

import run_devpi
import plugin_input

BASE_PATH = os.path.dirname(os.path.abspath(__name__))
# We use testpkg as a sample Python module to publish.
TEST_PACKAGE_PATH = os.path.join(BASE_PATH, "testpkg")


class DevpiTestCase(unittest.TestCase):
    # We'll override the default clientdir while creating our index below.
    default_clientdir = "/tmp/devpi-testclientdir"
    default_env = {
        "PLUGIN_SERVER": "http://localhost:3141/",
        "PLUGIN_INDEX": "root/devpitest",
        "PLUGIN_USERNAME": "root",
        "PLUGIN_PASSWORD": "",
        "PLUGIN_PACKAGE_PATH": TEST_PACKAGE_PATH
    }

    def setUp(self):
        os.environ.update(self.default_env)
        plugin_input.values.load_values()

    @classmethod
    def setUpClass(cls):
        # TODO: This should probably go away once load_values() accepts
        # an optional override kwarg.
        os.environ.update(cls.default_env)
        plugin_input.values.load_values()
        # We'll only do this once so we're not hammering the server if we
        # grow this test suite.
        cls._wait_for_devpi_to_start(cls.default_clientdir)

    @classmethod
    def _wait_for_devpi_to_start(cls, clientdir):
        """
        devpi is a bit... pokey while starting. We'll just harass it until
        it responds before doing the rest of the tests.
        """
        retries_left = 30
        while retries_left > 0:
            try:
                run_devpi.select_server(
                    plugin_input.values['SERVER'], clientdir=clientdir)
            except SystemExit:
                retries_left -= 1
                time.sleep(1)
                continue
            return

    def _ensure_test_index_exists(self, clientdir):
        """
        Since Drone fires up a new devpi server for each test run, we'll
        need to create an index before we can upload.
        """
        run_devpi.select_server(
            plugin_input.values['SERVER'], clientdir=clientdir)
        run_devpi.login(
            plugin_input.values['USERNAME'], plugin_input.values['PASSWORD'],
            clientdir=self.default_clientdir)
        try:
            run_devpi.create_index(
                plugin_input.values['INDEX'], clientdir=clientdir)
        except SystemExit:
            pass

    def test_upload(self):
        """
        Tests a simple package upload to an existing DevPi server.
        """
        self._ensure_test_index_exists(self.default_clientdir)
        run_devpi.main()


if __name__ == '__main__':
    unittest.main()
