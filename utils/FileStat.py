# FileStat: a simple class to make file analysis
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

"""@package FolderStat
This package contains a class for listing files in folders and traversing the file system

"""

#########################################################################
__author__="Paolo Di Prodi"
__version__ = "1.0"
#########################################################################


import time
import mmap
import random
from collections import defaultdict
import unittest

class FileReader:
    """
    FileReader is an utility class to build analytics for files
    """
    ## the filename we are analysing
    __filename=None;
    def __init__(self, filename):
        """The constructor.
        @param filename: filename of the file
        """
        self.__filename=filename
    
    def GetLines(self):
        """Return the number of lines in the buffer """
        return self.bufcount()
        
    def mapcount(self):
        """Load the buffer via memory map and count the lines """
        f = open(self.__filename, "r+")
        buf = mmap.mmap(f.fileno(), 0)
        lines = 0
        readline = buf.readline
        while readline():
            lines += 1
        return lines

    def simplecount(self):
        """Open the file and read the line one by one """
        lines = 0
        try: 
            for line in open(self.__filename):
                lines += 1
            return lines
        except IOError:
            return None
            
    def bufcount(self):
        """Open the file, read it in page buffer and count the lines"""
        try:
            f = open(self.__filename)          
        except IOError:
            return None
        else:
            with f:
                lines = 0
                ## buffer size is 1 Kb * 1 Kb
                buf_size = 1024 * 1024
                read_f = f.read
                buf = read_f(buf_size)
                while buf:
                    lines += buf.count('\n')
                    buf = read_f(buf_size)
                return lines

    def opcount(self):
        """Open the file and read the number of operations """
        with open(self.__filename) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

class Benchmark(unittest.TestCase):
    """
    Unit test to measure correctness in measuring number of lines
    """
    __file_lines=68
    def setUp(self):
        self.reader =FileReader("tests/main.c")
    def testRead(self):
        self.failIf(self.reader.bufcount() is None)
        
    def testSpeed(self):
        """Compare and measure the best method to count the number of lines """    
        counts = defaultdict(list)
        for i in range(5):
            for func in [self.reader.mapcount,self.reader.simplecount, self.reader.bufcount, self.reader.opcount]:
                start_time = time.time()
                self.assertEqual(func() ,  self.__file_lines )
                counts[func].append(time.time() - start_time)
        print "File read comparison"
        for key, vals in counts.items():
            print key.__name__, ":", sum(vals) / float(len(vals))

def main():
    unittest.main()
    
if __name__ == "__main__":
    """ This should be called only for unit testing """
    main()


