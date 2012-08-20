# FileReader: a simple class to count the number of line codes in a file
# Author: Paolo Di Prodi
# Copyright 2012 Robomotic ltd
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import with_statement
import time
import mmap
import random
from collections import defaultdict

class FileReader:
    __filename=None;
    def __init__(self, filename):
        self.__filename=filename
    
    def GetLines(self):
        return self.bufcount(self.__filename)
    def mapcount(self, filename):
        f = open(filename, "r+")
        buf = mmap.mmap(f.fileno(), 0)
        lines = 0
        readline = buf.readline
        while readline():
            lines += 1
        return lines

    def simplecount(self, filename):
        lines = 0
        for line in open(filename):
            lines += 1
        return lines

    def bufcount(self, filename):
        f = open(filename)                  
        lines = 0
        buf_size = 1024 * 1024
        read_f = f.read # loop optimization

        buf = read_f(buf_size)
        while buf:
            lines += buf.count('\n')
            buf = read_f(buf_size)
        return lines

    def opcount(fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def benchmark(self):
        counts = defaultdict(list)
        for i in range(5):
            for func in [mapcount, simplecount, bufcount, opcount]:
                start_time = time.time()
                assert func("tests/main.c")==65 
                counts[func].append(time.time() - start_time)

        for key, vals in counts.items():
            print key.__name__, ":", sum(vals) / float(len(vals))

if __name__ == "__main__":
    reader=FileReader("tests/main.c")
    print reader.GetLines()
