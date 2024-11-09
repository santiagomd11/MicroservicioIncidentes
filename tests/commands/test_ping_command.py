import unittest
from src.commands.ping import Ping

class TestPingCommand(unittest.TestCase):
    def test_ping(self):
        command = Ping()
        response = command.execute()
        self.assertEqual(response, 'pong')

if __name__ == '__main__':
    unittest.main()