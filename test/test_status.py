import unittest

import healthpy


class StatusTest(unittest.TestCase):
    def test_status_aggregation_with_failure(self):
        self.assertEqual("fail", healthpy.status("pass", "fail", "warn"))

    def test_status_aggregation_with_warning(self):
        self.assertEqual("warn", healthpy.status("pass", "warn", "pass"))

    def test_status_aggregation_with_pass(self):
        self.assertEqual("pass", healthpy.status("pass", "pass", "pass"))
