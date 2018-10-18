# -*- coding: utf-8 -*-

'''
@author: wujun
'''


# CURRENT_CONFIG = 'local'
CURRENT_CONFIG = 'line'
# CURRENT_CONFIG = 'local'
DB = {
      'local':
        {
            'MYSQL_HOST':'127.0.0.1',
            'MYSQL_DBNAME':'ecms72',
            'MYSQL_PORT':3306,
            'MYSQL_USER':'py',
            'MYSQL_PASSWD':'py'
        },
      'line':
        {
            'MYSQL_HOST':'10.2.2.103',
            'MYSQL_DBNAME':'whois_python',
            'MYSQL_PORT':3306,
            'MYSQL_USER':'whois_pythonuser',
            'MYSQL_PASSWD':'p6l6agW5FSu9FYzq'
        },
    'localline':
        {
            'MYSQL_HOST':'127.0.0.1',
            'MYSQL_DBNAME':'ecms72',
            'MYSQL_PORT':3306,
            'MYSQL_USER':'py',
            'MYSQL_PASSWD':'py'
        }
}

REDIS = {
      'local':
        {
            'host':'119.10.116.237',
            'port':6379,
            'db':8,
            'password':'xinnet'
        },
      'line':
        {
            'host':'10.2.2.87',
            'port':6379,
            'db':4,
            'password':'xinnet123'
        },

    'localline':
        {
            'host':'10.2.2.87',
            'port':6379,
            'db':4,
            'password':'xinnet123'
        }
}





