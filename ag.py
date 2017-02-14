#! /usr/bin/env python
#################################################################################
#     File Name           :     ag.py
#     Created By          :     CS438 Graders
#     Creation Date       :     [2017-02-12 21:46]
#     Last Modified       :     [2017-02-13 01:28]
#     Description         :      
#################################################################################

import traceback
from subprocess import call, check_output, check_call
from os import listdir
from os.path import isfile, isdir, join
from pprint import pprint
import json

from dateutil import parser
from grade_info import *
import datetime


SVN_ROOT = '/home/grader/sp17-cs438/'
MP_PATH = 'MP2/'

NETID_EXCLUDE = ['khuang29', 'rhk', 'azhang41']

def list_students(exclude=[]):
    res = []
    for f in listdir(SVN_ROOT):
        if isdir(join(SVN_ROOT, f)) and str.isalnum(f) and f not in exclude:
            res.append(f)

    return sorted(res)


def svn_last_changed(dirpath):
    svninfo = check_output(['svn', 'info', dirpath])
    for l in svninfo.split('\n'):
        if 'Last Changed Date' in l:
            segs = l.split()
            timestr = ' '.join(segs[3:6])
            return parser.parse(timestr)
    return None


def grade(nid, masteraddress, command):
    mppath =  join(SVN_ROOT, nid, MP_PATH)
    try:
        check_call(["scp -r", mppath, "grader@"+masteraddress+ ":~/cur"])
        check_call(["ssh", "grader@"+masteraddress, command])
    except:
        traceback.print_exc()

    call(["scp", "grader@"+masteraddress+ join(":~/cur", 'results.txt')], mppath)

    return parse_result(mppath)


def parse_result(mppath):
    with open(join(mppath, 'results.txt') as f:
        

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
            continue

        curgrade = grade(nid)

        gi.update(nid, current_version, curgrade)
        gi.dump()


if __name__=='__main__':
    auto_grade(list_students(NETID_EXCLUDE), 'MP1')
