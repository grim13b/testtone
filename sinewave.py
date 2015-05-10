# -*- coding: utf-8 -*-
__author__ = 'grim3lt'
import numpy
import struct


class SineWaveCreator:
    def offset_header(self, fp):
        for i in range(44):
            fp.write(b'0')

    def write(self, fp, a, f0, fs, depth, sec):
        """
        a = amplitude
        f0 = frequency
        fs = sampling frequency
        depth = bit depth
        sec = seconds
        """
        if a > 1.0:
            return None

        dr = 2 ** depth / 2 - 1

        for n in range(sec * fs):
            y = a * numpy.sin(2 * numpy.pi * f0 * n / fs)
            s = int(y * dr)
            fp.write(struct.pack('h', s))
            fp.write(struct.pack('h', s))

    def write_header(self, fp, fs, depth):
        data_chunk_size = fp.tell()

        fp.seek(0, 0)
        fp.write(b'RIFF')
        fp.write(struct.pack('I', data_chunk_size + 44))  # data size + format header size
        fp.write(b'WAVE')  # WAVE format chunk Header
        fp.write(b'fmt ')  # fmt chunk header
        fp.write(struct.pack('I', 16))  # size of chunk
        fp.write(struct.pack('H', 0x0001))  # liner pcm
        fp.write(struct.pack('H', 0x0002))  # channel
        fp.write(struct.pack('I', fs))  # sampling frequency(unit Hz)
        fp.write(struct.pack('I', fs * 2 * 2))  # data transfer speed
        fp.write(struct.pack('H', 2 * 2))  # data block size
        fp.write(struct.pack('H', depth))  # bit depth
        fp.write(b'data')
        fp.write(struct.pack('I', data_chunk_size))


def main():
    album = [
        [10, 200, 10],
        [200, 2000, 100],
        [2100, 5000, 100],
        [5100, 8000, 100],
        [8100, 10000, 100],
        [10100, 12000, 100],
        [12100, 15000, 100],
        [15100, 18000, 100],
        [18100, 20000, 100]
    ]

    for track in album:
        filename = '{0}-{1}Hz-{2}Hz.wav'.format(track[0], track[1], track[2])
        with open(filename, 'w+b') as fp:
            sw = SineWaveCreator()
            sw.offset_header(fp)

            for freq in range(track[0], track[1], track[2]):
                sw.write(fp, 0.7, freq, 96000, 16, 3)

            sw.write_header(fp, 96000, 16)

if __name__ == "__main__":
    main()
