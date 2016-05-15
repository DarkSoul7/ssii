# -*- coding: utf-8 -*-
import datetime
import psi5.functions.auxiliary as a
from dateutil.relativedelta import relativedelta

nextsync = datetime.datetime.today() + relativedelta(months=1, day=1, hour=0, minute=0, second=0, microsecond=0)

while True:
    if datetime.datetime.today() == nextsync:
        file = a.updatefiles(nextsync)
        a.sendemail(file)
        nextsync += relativedelta(months=1)
