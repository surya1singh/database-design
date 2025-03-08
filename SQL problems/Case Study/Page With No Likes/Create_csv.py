# 500,000,000 entries in pages and page_likes
from datetime import datetime
import random

start_time = datetime.now()
with open('pages.csv','w') as fp:
    for i in range(1, 500_000_000):
        if i%10000000 ==0:
            print(i//10000000)
        data = f'{i},"Page Name"'
        fp.write(data+'\n')


end_time = datetime.now()
print(end_time-start_time)


with open('page_likes.csv','w') as fp:
    for i in range(1, 500_000_000):
        if i%10000000 ==0:
            print(i//10000000)
        data = f'{random.randint(1,100)},{random.randint(1,500_000_000)}'
        fp.write(data+'\n')

end_time = datetime.now()
print(end_time-start_time)