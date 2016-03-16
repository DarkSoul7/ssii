# -*- coding: utf-8 -*-
import random
import string
from os.path import isfile


def generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def writelog(log_dir, operation, error=False):
    if not isfile(log_dir):
        log = open(log_dir, mode='w+')
        log.close()

    with open(log_dir, mode='r') as log:
        lines = log.readlines()
    with open(log_dir, mode='w+') as log:
        if lines:
            lines.pop(-1)
            sucop = lines.pop(-1).split('\t\t')[1]
            op = lines.pop(-1).split('\t\t')[1]
            lines.append(operation + '\n')

            if error:
                op = int(op) + 1
                sucop = int(sucop)
                kpi = float(sucop/op)
            else:
                op = int(op) + 1
                sucop = int(sucop) + 1
                kpi = float(sucop/op)

            lines.append('Total number of operations\t\t' + str(op) + '\n')
            lines.append('Total number of successful operations\t\t' + str(sucop) + '\n')
            lines.append('Kpi\t\t' + str(kpi) + '\n')
        else:
            lines.append(operation + '\n')
            if error:
                lines.append('Total number of operations\t\t1\n')
                lines.append('Total number of successful operations\t\t0\n')
                lines.append('Kpi\t\t0\n')
            else:
                lines.append('Total number of operations\t\t1\n')
                lines.append('Total number of successful operations\t\t1\n')
                lines.append('Kpi\t\t1\n')
        log.writelines(lines)
