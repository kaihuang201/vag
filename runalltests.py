#! /usr/bin/env python
#################################################################################
#     File Name           :     runalltests.py
#     Created By          :     CS438 Graders
#     Creation Date       :     [2017-02-19 12:34]
#     Last Modified       :     [2017-02-21 22:26]
#     Description         :     run all tests for MP 
#################################################################################

#credits azhang41
import os
import subprocess
import os.path
import pdb

def make_testcases(index):
    testcase_prefix = ["lstest", "vectest"]
    test_weight = [10, 10, 10, 10, 10, 10, 10, 10]
    test_timeout = [30, 30, 30, 30, 30, 30, 30, 30]
    num_of_testcases = 8
    testcases = []
    prefix = testcase_prefix[index]
    for i in range(num_of_testcases):
        testfile = prefix + str(i+1) + ".pl"
        testcases.append((testfile, test_weight[i], test_timeout[i]))
    return testcases

def compile_and_check(cur_dir):
    os.chdir(cur_dir)
    os.system("rm compile_error.txt")
    os.system("rm results.txt")
    os.system("make clean")
    os.system("make")
    #pdb.set_trace()
    if os.path.isfile(cur_dir+'ls_router'):
        return 0
    elif os.path.isfile(cur_dir+'vec_router'):
        return 1
    else:
        return None

def runtests(test_dir, testcases):
    os.chdir(test_dir)
    f = open(cur_dir+'results.txt', 'w+')
    for testname, weight, timeout in testcases:
        try:
            message = subprocess.check_output(
                ["perl", testname], timeout=timeout).decode()
        except:
            message = str(weight) + " " + testname + " timed out.\n"
        f.write(message)
    f.close()

if __name__ == "__main__":
    cur_dir = '/home/grader/cur/'
    test_dir = '/home/grader/mp2_tests/'
    index = compile_and_check(cur_dir)
    if index is None:
        f = open(cur_dir+'compile_error.txt', 'w+')
        f.write('compile error!')
        f.close()
    else:
        testcases = make_testcases(index)
        print (testcases)
        runtests(test_dir, testcases)

