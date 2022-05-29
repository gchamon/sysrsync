import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
import sysrsync


class TestE2E(unittest.TestCase):
    def test_send_file(self):
        sysrsync.run(source="end-to-end-tests/test-cases/test_file",
                     destination="/tmp/target_test_file",
                     destination_ssh="test@openssh-server",
                     private_key="end-to-end-tests/keys/test-key",
                     rsh_port=2222,
                     strict_host_key_checking=False)

    def test_send_file_with_spaces(self):
        sysrsync.run(source="end-to-end-tests/test-cases/file with spaces",
                     destination="/tmp/target_test_file",
                     destination_ssh="test@openssh-server",
                     private_key="end-to-end-tests/keys/test-key",
                     rsh_port=2222,
                     strict_host_key_checking=False)


if __name__ == '__main__':
    unittest.main()
