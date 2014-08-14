from __future__ import absolute_import

from celery import shared_task


import MySQLdb


@shared_task
def remote_query(host, user, passwd, query, params=None):
    con = MySQLdb.connect(host=host, user=user, passwd=passwd)
    cur = con.cursor()
    cur.execute(query)
    output = cur.fetchall()
    cur.close()
    con.close()
    return output

