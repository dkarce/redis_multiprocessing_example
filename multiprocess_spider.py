import redis
import time
import random
from multiprocessing import Process

'''Example of creating and catching urls for spider'''


class XiaomiSpider(object):

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    # creating list of urls
    def product(self):
        for pagenum in range(67):
            url = 'http://app.mi.com/category/2#page={}'.format(pagenum)
            self.r.lpush('xiaomi:spider', url)
            time.sleep(random.randint(1, 3))

    # collecting urls from redis server
    def consumer(self):
        while True:
            urls = self.r.brpop('xiaomi:spider', 4)
            if urls:
                print('scanning: ', urls)
            else:
                break

    # create multiprocessing
    def run(self):
        p1 = Process(target=self.product)
        p2 = Process(target=self.product)
        p1.start()
        p2.start()
        p1.join()
        p2.join()


if __name__ == '__main__':
    spider = XiaomiSpider()
    spider.run()
