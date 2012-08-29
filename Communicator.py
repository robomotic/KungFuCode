# Communicator: this is the part that does the dialog with the server
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

import time
import logging
from rest import restful_lib
import ConfigParser

class Client(object):
    
    __version=1.0
    __conn=None
    def __init__(self):
        Config = ConfigParser.ConfigParser()
        Config.read("config/parser.ini")
        self.user=Config.get("Authentication", "Username")
        self.password=Config.get("Authentication", "Password")
        self.server=Config.get("Params","SERVERNAME")
        self.__conn = restful_lib.Connection("http://codefactor.phpfogapp.com/", username=self.user, password=self.password)
    def postStats(self, data):
        response =self.__conn.request_post("/upload.php", args=data)
        #print response

    def getStats(self, data):
        response =self.__conn.request_get("/get.php", args=data)
        #print response
