#! /usr/bin/env python
#################################################################################
#     File Name           :     ag.py
#     Created By          :     CS438 Graders
#     Creation Date       :     [2017-02-12 21:46]
#     Last Modified       :     [2017-02-25 20:52]
#     Description         :      
#################################################################################

import traceback
import subprocess
from subprocess import call, check_output, check_call
import os
from os import listdir
from os.path import isfile, isdir, join
from pprint import pprint
import json

from dateutil import parser
from grade_info import *
import datetime

DEVNULL = open(os.devnull, 'wb')

#SVN_ROOT = '/home/grader/sp17-cs438/'
SVN_ROOT = '/home/grader/khuang/'
MP_PATH = 'MP2/'

MASTER_IP = '192.168.56.101'
GRADING_SCRIPT = 'runalltests.py'

NETID_EXCLUDE = ['khuang29', 'rhk', 'azhang41']

def list_students(exclude=[]):
    res = []
    for f in listdir(SVN_ROOT):
        if isdir(join(SVN_ROOT, f)) and str.isalnum(f) and f not in exclude:
            res.append(f)

    return sorted(res)


def svn_last_changed(dirpath):
    svninfo = check_output(['svn', 'info', dirpath])
    timestamp = None
    rev = None
    try:
        for l in svninfo.split('\n'):
            if 'Last Changed Date' in l:
                segs = l.split()
                timestr = ' '.join(segs[3:6])
                timestamp = parser.parse(timestr)
            elif 'Last Changed Rev' in l:
                segs = l.split()
                rev = int(segs[3])
    except:
        pass
    return timestamp, rev


def grade(nid, masteraddress, command='python3 ~/'+GRADING_SCRIPT):
    mppath =  join(SVN_ROOT, nid, MP_PATH)
    try:
        check_call(['ssh', 'grader@'+masteraddress, 'rm -rf ~/cur'], stdout=DEVNULL, stderr=subprocess.STDOUT)
        check_call(['scp', GRADING_SCRIPT, 'grader@'+masteraddress+':~'], stdout=DEVNULL, stderr=subprocess.STDOUT)
        check_call(['scp', '-r', mppath, 'grader@'+masteraddress+':~/cur'], stdout=DEVNULL, stderr=subprocess.STDOUT)
        check_call(['ssh', 'grader@'+masteraddress, command], stdout=DEVNULL, stderr=subprocess.STDOUT)
        call(['scp', 'grader@'+masteraddress+join(':~/cur/', 'results.txt'), mppath], stdout=DEVNULL, stderr=subprocess.STDOUT)
    except:
        traceback.print_exc()



def get_cur_version_num(nid, mp_path):
    version_file_path = join(SVN_ROOT, nid, mp_path, 'version.txt')
    try:
        with open(version_file_path) as f:
            return int(f.read())
    except:
        return -1


def auto_grade(nids, mp_path):
    gi = GradeInfo()
    for nid in nids:
        print('* Processing ' + nid)

        current_version = get_cur_version_num(nid, mp_path)
        if current_version <= gi.get_last_version_num(nid):
            print('    current_version = %d, last_version = %d. Skipping' % (current_version, gi.get_last_version_num(nid)))
            #continue #TODO: UNCOMMENT!

        curgrade = grade(nid, MASTER_IP)

        gi.update(nid, current_version, curgrade)
        gi.dump()


if __name__=='__main__':
    auto_grade(list_students(NETID_EXCLUDE), MP_PATH)
    #print svn_last_changed('/home/grader/sp17-cs438/khuang29')
