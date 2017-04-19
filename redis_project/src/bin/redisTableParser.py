# pylint: disable=invalid-name, anomalous-backslash-in-string
"""
    redisTableParser.py: Create a table in the Redis
    database.
"""

import argparse
import os.path
import redis

__author__ = "Stratos Gounidellis, Lamprini Koutsokera"
__copyright__ = "Copyright 2017, BDSMasters"


class RedisTableParser(object):
    """RedisTableParser: Implementation of the methods needed
        to successfuly create a table in the Redis database.
    """

    def sqlTableToRedis(self, tableFile):
        """Create a Redis Table parsing data from an SQL Table
        through a file.

        :param self: An instance of the class RedisTableParser.
        :param tableFile: A file that contains data from an SQL
            Table.
        """
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        with open(tableFile, "r") as inputFile:
            input_data = inputFile.readlines()
        try:
            flag_fields = True
            table = input_data.pop(0).replace("\n", "")
            tableId = table + "Id"
            if r.get(tableId) is None:
                r.set(tableId, 1)
            fields = []
            print

            for string in input_data:
                if not flag_fields and string.rstrip():
                    self.recordsInsertion(r, string, fields, table, tableId)
                if flag_fields and string.rstrip():
                    if string.replace("\n", "") == ";":
                        flag_fields = False
                    else:
                        fields.append(string.replace("\n", ""))

        except redis.exceptions.ConnectionError:
            print "\nRedis connection error! " + \
                "Check that redis server is on and working.\n"
            quit()
        except redis.exceptions.ResponseError:
            print "\nRedis response error! " + \
                "Check that redis' configuration!"
            quit()

    @staticmethod
    def recordsInsertion(r, string, fields, table, tableId):
        """Insert in redis database the records.

        :param r: An instance of connection to redis.
        :param string: A string delimited with ";",
            containing a record.
        :param fields: The attributes of the table.
        :param table: The name of the table to be inserted.
        :param tableId: The table counter.
        """
        counter = 1
        checkExists = False
        string = string.replace("\n", "")
        string = string.split(";")
        for field, record in zip(fields, string):
            if counter == 1:
                if record in r.smembers(table + "_PrimaryKeys"):
                    checkExists = True
                    print table + " with " + field + ": " + \
                        record + " already exists!"
                    break
                else:
                    r.sadd(table + "_PrimaryKeys", record)
                counter += 1
            record_key = table + "_" + field + "_" + r.get(tableId)
            r.set(record_key, record)
        if not checkExists:
            r.incr(tableId)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Insert relational data" +
                                     " in a redis database.",
                                     epilog="Go ahead and try it!")
    parser.add_argument("inputFile", type=str,
                        help="Input file with the sql table.")
    args = parser.parse_args()

    sqlTable = args.inputFile

    if os.path.isfile(sqlTable):
        instanceRedisTable = RedisTableParser()
        instanceRedisTable.sqlTableToRedis(sqlTable)
    else:
        raise Exception("\nInput file does not exist! \n")
    print "\nRelational data have been successfuly inserted into Redis!"
