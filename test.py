import re
from mongoctl import MongoCtl

if __name__ == '__main__':
    mongoctl = MongoCtl()

    uids_1 = set()
    uids_2 = set()
    print(0, '-----')
    data = mongoctl.users.find()
    for record in data:
        uid = record['uid']
        if uid in uids_1:
            print(uid)
        else:
            uids_1.add(uid)

