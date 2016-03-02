# -*- coding: utf-8 -*-
from datetime import datetime
import pytz
import tzlocal

tz = str(tzlocal.get_localzone())
t = datetime.utcnow()
print(t)
t.replace(tzinfo=pytz.timezone(str(tzlocal.get_localzone())))
print(t.strftime('%Y-%m-%dT%H:%M'))