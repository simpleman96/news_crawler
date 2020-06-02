from datetime import datetime
from datetime import timedelta

now = datetime.now()
print(now.strftime("%Y-%m-%d"))
print((now + timedelta(days=1)).strftime("%Y-%m-%d"))
