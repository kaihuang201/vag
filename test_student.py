#! /usr/bin/env python
#################################################################################
#     File Name           :     test.py
#     Created By          :     CS438 Graders
#     Creation Date       :     [2017-02-12 21:50]
#     Last Modified       :     [2017-02-13 01:12]
#     Description         :      
#################################################################################
import os
import time
from subprocess import call

#def runtests(testcases, masternodename):
#    for testcase in testcases:
#        os.system("VBoxManage controlvm " + masternodename + " poweroff");
#        os.system("VBoxManage startvm " + masternodename + " --type headless")
#        time.sleep(10)
#        call(["ssh", "grader@"+masteraddress, "echo $PATH"])

def givecode(masteraddress, student, pathTostudentDir):
    call(["scp -r", pathTostudentDir, "grader@"+masteraddress+ ":~/cur"])

def initVM(masteraddressm, script):
    call(["ssh", "grader@"+mainDir], "killall -9 "+script)

def runtest(masteraddress, command="python3 runalltests.py"):
    call(["ssh", "grader@"+masteraddress, command])


if __name__=='__main__':
    master = "192.168.56.102"
    masternodename = "master"

    runtests(testcases, master, masternodename)
