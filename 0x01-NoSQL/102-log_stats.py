#!/usr/bin/env python3
""" Top 10 present ip addresses in the nginx collection """


def log_stats():
    """ Improves 12-log_stats.py with top 10 ips """
    from pymongo import MongoClient

    client = MongoClient()
    db = client.logs

    print("{} logs".format(db.nginx.count_documents({})))
    print("Methods:")

    for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
        count = db.nginx.count_documents({'method': method})
        print("\tmethod {}: {}".format(method, count))

    count = db.nginx.count_documents({'method': 'GET', 'path': '/status'})
    print('{} status check'.format(count))
    print("IPs:")
    pipe = [
        {'$group': {'_id': '$ip', 'countIps': {'$sum': 1}}},
        {'$sort': {'countIps': -1}},
        {'$limit': 10}
    ]
    for ip in db.nginx.aggregate(pipe):
        print("\t{}: {}".format(ip.get('_id'), ip.get('countIps')))
    client.close()


if __name__ == '__main__':
    """ Run if not imported """
    log_stats()
