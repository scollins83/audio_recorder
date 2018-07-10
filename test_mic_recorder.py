import unittest
from mic_recorder import *


class TestRecorder(unittest.TestCase):
    def test_instantiate(self):
        rate = 4400
        chunksize = 1024
        rec = Recorder(rate=rate, chunksize=chunksize)
        self.assertIsNotNone(rec)
        self.assertEqual(rec.chunksize, chunksize)
        self.assertEqual(rec.rate, rate)
        self.assertTrue(isinstance(rec.p, pyaudio.PyAudio))

    def test_open_stream(self):
        rec = Recorder()
        self.assertIsNotNone(rec.stream)


if __name__ == '__main__':
    unittest.main()
