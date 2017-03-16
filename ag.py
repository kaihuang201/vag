#! /usr/bin/env python
#################################################################################
#     File Name           :     ag.py
#     Created By          :     CS438 Graders
#     Creation Date       :     [2017-02-12 21:46]
#     Last Modified       :     [2017-03-16 11:24]
#     Description         :      
#################################################################################

import traceback
import subprocess
from subprocess import call, check_output, check_call
import os
import sys
from os import listdir
from os.path import isfile, isdir, join
from pprint import pprint
import json

from dateutil import parser
from grade_info import *
import datetime

DEVNULL = open(os.devnull, 'wb')

#SVN_ROOT = '/home/grader/sp17-cs438/'
#Ailing: test on sp16
SVN_ROOT = '/home/grader/sp17-cs438/'
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


def svn_last_changed(nid, mp_path=MP_PATH):
    dirpath =  join(SVN_ROOT, nid, mp_path)
    timestamp = None
    rev = -1
    try:
        svninfo = check_output(['svn', 'info', dirpath])
        for l in svninfo.split('\n'):
            if 'Last Changed Date' in l:
                segs = l.split()
                timestr = ' '.join(segs[3:6])
                timestamp = parser.parse(timestr)
            elif 'Last Changed Rev' in l:
                segs = l.split()
                rev = int(segs[3])
    except:
        traceback.print_exc()

    return timestamp, rev


def grade(nid, masteraddress, command='python3 ~/'+GRADING_SCRIPT, mp_path=MP_PATH):
    #TODO: use score as a return value
    mppath =  join(SVN_ROOT, nid, mp_path)
    try:
        check_call(['ssh', 'grader@'+masteraddress, 'rm -rf ~/cur'], stdout=DEVNULL, stderr=subprocess.STDOUT)
    except:
        traceback.print_exc()

    try:
        check_call(['scp', GRADING_SCRIPT, 'grader@'+masteraddress+':~'], stdout=DEVNULL, stderr=subprocess.STDOUT)
    except:
        traceback.print_exc()

    try:
        check_call(['scp', '-r', mppath, 'grader@'+masteraddress+':~/cur'], stdout=DEVNULL, stderr=subprocess.STDOUT)
    except:
        traceback.print_exc()

    try:
        check_call(['ssh', 'grader@'+masteraddress, command], stdout=DEVNULL, stderr=subprocess.STDOUT)
    except:
        traceback.print_exc()

    try:
        call(['scp', 'grader@'+masteraddress+join(':~/cur/', 'results.txt'), mppath], stdout=DEVNULL, stderr=subprocess.STDOUT)
    except:
        traceback.print_exc()



def get_cur_version_num(nid, mp_path):
    version_file_path = join(SVN_ROOT, nid, mp_path, 'version.txt')
    try:
        with open(version_file_path) as f:
            return int(f.read())
    except:
        traceback.print_exc()
        return -1 

def append_result(nid, rev, mp_path=MP_PATH):
    result_file_path = join(SVN_ROOT, nid, mp_path, 'results.txt')
    try:
        with open(result_file_path, 'a') as f:
            currtime = datetime.datetime.now().strftime("%I:%M %p on %B %d, %Y")
            f.write('\nsvn rev: %d\n\n%s' % (rev, currtime))
    except:
        traceback.print_exc()
        return -1


def auto_grade(nids, mp_path, ignore_version=False):
    gi = GradeInfo()
    for nid in nids:
        print('* Processing ' + nid)

        current_version = get_cur_version_num(nid, mp_path)
        if current_version <= gi.get_last_version_num(nid):
            if ignore_version:
                print('    current_version = %d, last_version = %d. ignore_version = True' % (current_version, gi.get_last_version_num(nid)))
            else:
                print('    current_version = %d, last_version = %d. Skipping' % (current_version, gi.get_last_version_num(nid)))
                continue

        curgrade = grade(nid, MASTER_IP)

        timestamp, rev = svn_last_changed(nid)
        append_result(nid, rev)

        gi.update(nid, current_version, curgrade)
        gi.dump()


if __name__=='__main__':
    if len(sys.argv) == 1:
        auto_grade(list_students(NETID_EXCLUDE), MP_PATH)
    else:
        auto_grade(sys.argv[1:], MP_PATH, True)
    #ts, rev = svn_last_changed('fkdlaj')
    #append_result('khuang29', rev)
