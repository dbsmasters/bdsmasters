# pylint: disable=invalid-name, anomalous-backslash-in-string
"""
    testRedisQueryParser.py: Test the results' validity of the SQL
    Query Parsing.
"""

import unittest
from redisQueryParser import RedisQueryParser

__author__ = "Stratos Gounidellis, Lamprini Koutsokera"
__copyright__ = "Copyright 2017, BDSMasters"


class TestRredisQueryParser(unittest.TestCase):
    """TestRredisQueryParser: Implementation of the methods needed
        to successfuly test the expected results from the
        SQL Query Parsing.
    """

    def test_readSqlQuery(self):
        """Test whether a given query is read correctly or not.
        """
        instanceQueryParser = RedisQueryParser()
        fname = "redisQuery1.txt"
        clauses = instanceQueryParser.parseSqlQuery(fname)

        expectedClauses = ["Student_FName, Student_LName, Grade_Mark"]
        expectedClauses.append("Student, Grade")
        expectedClauses.append("Student_SSN=Grade_SSN")
        expectedClauses.append("")
        expectedClauses.append(None)

        self.assertEqual(clauses, tuple(expectedClauses))

    def test_selectFromToRedis(self):
        """Test whether the SELECT clause is converted correctly or not.
        """
        instanceQueryParser = RedisQueryParser()
        fname = "redisQuery1.txt"
        clauses = instanceQueryParser.parseSqlQuery(fname)
        selectQuery = clauses[0]
        fromQuery = clauses[1]
        fromQuery = fromQuery.split(",")
        fromQuery = map(str.strip, fromQuery)
        fromQuery = [s + "_" for s in fromQuery]
        whereQuery = clauses[2]
        selectQuerySplitOrder = []

        results = instanceQueryParser.selectFromToRedis(
            selectQuery, fromQuery, whereQuery, selectQuerySplitOrder)
        expectedClauses = "Student_FName_List, Student_LName_List," + \
            " Grade_Mark_List, Student_SSN_List, Grade_SSN_List"
        self.assertEqual(results[2], expectedClauses)

    def test_orderQueryToRedis(self):
        """Test whether the ORDER BY clause is converted correctly or not.
        """
        instanceQueryParser = RedisQueryParser()
        fname = "redisQuery.txt"
        clauses = instanceQueryParser.parseSqlQuery(fname)
        selectQuery = clauses[0]
        fromQuery = clauses[1]
        fromQuery = fromQuery.split(",")
        fromQuery = map(str.strip, fromQuery)
        fromQuery = [s + "_" for s in fromQuery]
        orderQuery = clauses[3]

        results = instanceQueryParser.orderQueryToRedis(
            orderQuery, selectQuery)
        results = results[:2]
        expectedClauses = ['Student_FName', 1]
        self.assertEqual(results, tuple(expectedClauses))

    def test_whereQueryToRedis(self):
        """Test whether the WHERE clause is converted correctly or not.
        """
        instanceQueryParser = RedisQueryParser()
        fname = "redisQuery.txt"
        clauses = instanceQueryParser.parseSqlQuery(fname)
        fromQuery = clauses[1]
        fromQuery = fromQuery.split(",")
        fromQuery = map(str.strip, fromQuery)
        fromQuery = [s + "_" for s in fromQuery]
        whereQuery = clauses[2]

        results = instanceQueryParser.whereToRedis(fromQuery, whereQuery)
        expectedClause = 'if r.get(Student_FName) < "Nikos1":\n\t\t'
        self.assertEqual(results, expectedClause)

    def test_exceptionSyntaxError(self):
        """Test whether the syntax of the created python file is correct.
        """
        instanceQueryParser = RedisQueryParser()
        fname = "redisQuery6.txt"

        sqlClauses = instanceQueryParser.parseSqlQuery(fname)
        pythonFileContent = instanceQueryParser.sqlQueryToRedis(
            sqlClauses[0], sqlClauses[1], sqlClauses[2], sqlClauses[3],
            sqlClauses[4])
        outputFile = "test.py"
        instanceQueryParser.writePythonFile(outputFile, pythonFileContent)

        with self.assertRaises(Exception) as context:
            instanceQueryParser.checkSyntax(outputFile)
        self.assertIn('\nERROR! Please check the syntax of the ' +
                      'query. Output python file is not created! :(',
                      "".join(context.exception))


if __name__ == "__main__":
    unittest.main()
