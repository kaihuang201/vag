#! /usr/bin/env python
#################################################################################
#     File Name           :     runalltests.py
#     Created By          :     CS438 Graders
#     Creation Date       :     [2017-02-19 12:34]
#     Last Modified       :     [2017-02-28 12:53]
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
    test_timeout = [30, 30, 30, 30, 30, 30, 30, 60]
    num_of_testcases = 8
    testcases = []
    prefix = testcase_prefix[index]
    for i in range(num_of_testcases):
        testfile = prefix + str(i+1) + ".pl"
        testcases.append((testfile, test_weight[i], test_timeout[i]))
    return testcases

def compile_and_check(cur_dir):
    os.chdir(cur_dir)
    os.system("rm results.txt >/dev/null 2>&1")
    os.system("rm ls_router >/dev/null 2>&1")
    os.system("rm vec_router >/dev/null 2>&1")
    os.system("make clean >/dev/null 2>&1")
    os.system("make >/dev/null 2>&1")
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
    total_score = 20
    for testname, weight, timeout in testcases:
        print (testname, weight, timeout)
        try:
            message = subprocess.check_output(
                ["perl", testname], timeout=timeout).decode()
            segs = message.strip().split()
            item_score = int(segs[0])
            if item_score > 0:
                segs[0] = '0'
            else:
                total_score += weight 
                segs[0] = str(weight)
            f.write(' '.join(segs) + '\n')
        except:
            message = "0 " + testname + " timed out.\n"
            f.write(message)
    f.write('----------------\n')
    f.write('Total score: %d' % total_score + '\n')
    f.close()

if __name__ == "__main__":
    cur_dir = '/home/grader/cur/'
    test_dir = '/home/grader/mp2_tests/'
    index = compile_and_check(cur_dir)
    if index is None:
        f = open(cur_dir+'results.txt', 'w+')
        f.write('Compile error!\n')
        f.write('----------------\n')
        f.write('Total score: 0\n')
        f.close()
    else:
        testcases = make_testcases(index)
        print (testcases)
        runtests(test_dir, testcases)

