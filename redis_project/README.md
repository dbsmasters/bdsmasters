<img src="../logos/logoAUEB.png" width="280" height="80" align="right"></img>
<img src="../logos/dmst.png" width="200" height="80" align="left"></img><br><br>
<br><br><br>
[![BDSMasters](https://img.shields.io/badge/codedby-bdsmasters-brightgreen.svg?style=flat-square)](https://github.com/dbsmasters)
![redis database](https://img.shields.io/badge/redis-database-blue.svg?style=flat-square)

### <a id="contents" href="#contents">Contents</a>

1. [Redis Project: Relational databases & Key-Value systems](#redis-project-intro)
1. [Redis installation in Linux](#installing-redis)
1. [Relational data insertion in Redis database](#relational-data-insertion)
1. [SQL query execution in Redis database](#query-execution)
1. [Testing functionality](#test-functionality)
1. [Team](#team)
1. [See also](#see-also)



### <a id="redis-project-intro" href="#redis-project-intro">Redis Project: Relational databases & Key-Value systems</a>
> > Redis & SQL

This assignment is a part of a project implemented in the context of the course "Big Data Management Systems" taught by Prof. Chatziantoniou in the Department of Management Science and Technology (AUEB). The aim of the project is to familiarize the students with big data management systems such as Hadoop, Redis, MongoDB and Neo4j.

In the context of this assignment on Redis, relational data are inserted into a redis database while sql queries are properly edited and transformed in order to retrieve information from the redis database.

A detailed description of the assignment can be found [here](Proj2_Redis_Description.pdf).

### <a id="installing-redis" href="#installing-redis">Redis installation in Linux</a>
```shell
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
```    
### <a id="relational-data-insertion" href="#relational-data-insertion">Relational data insertion in Redis database</a>

A relation's schema and its contents are given in a text file in a specific format according to the following rules:
1. the first line contains only the table's name.
2. the second line contains the primary key's name, which is only a single attribute.
3. the rest of the attributes are in a single line each.
4. one line containing the character ";" follows.
5. the following line(s), represent records and are delimited by the character ";".

It is assumed that all attributes are of type string.

For instance, the following table contains data for students.

##### Student -SQL Table
|SSN|FName|LName|Address|Age|
|---|---|---|---|---|
|12938|Nikos|Papadopoulos|Hydras 28, Athens|42|
|18298|Maria|Nikolaou|Kifisias 33, Marousi|34|
|81129|Dimitris|Panagiotou|Alamanas 44, Petralona|29|

##### Student -SQL Table in text file

``` mysql
Student
SSN
FName
LName
Address
Age
;
12938;Nikos;Papadopoulos;Hydras 28, Athens;42
18298;Maria;Nikolaou;Kifisias 33, Marousi;34
81129;Dimitris;Panagiotou;Alamanas 44, Petralona;29
```

The relational data will be inserted in the redis database using the following python script. The script is effective for the following cases:
1. The text file follows the structure described above.
2. The primary key is a single attribute.

#### Steps
**1.** Clone this repository:
```shell
git clone https://github.com/dbsmasters/bdsmasters.git
cd /bdsmasters/redis_project
```
**2.** Install the required python packages.
```shell
pip install -r requirements.txt
```
**3.** Run redisTableParser.py to insert the relational data in redis database.
```shell
python redisTableParser.py sqlTable.txt
```


### <a id="query-execution" href="#query-execution">SQL query execution in Redis database</a>

A query will be given as a text file containing two to five lines:
1. first line (SELECT): a list of table_name.attribute_name, delimited by the character ",".
2. second line (FROM): a list of table names, delimited by the character ",".
3. third line (WHERE): a simple condition, consisting only of AND, OR, NOT, =, <>, >, <, <=, >= and parentheses.
4. fourth line (ORDER BY): a simple clause, containing either an attribute name and the way of ordering (ASC or DESC) or RAND().
5. fifth line (LIMIT): a number, specifying the number of rows to be displayed.


##### SQL Query
``` mysql
SELECT Student.FName, Student.LName, Grade.Mark
FROM Student, Grade
WHERE Student.SSN=Grade.SSN
ORDER BY Student.Age ASC
LIMIT 2 
```
##### SQL Query in text file
``` mysql
Student.FName, Student.LName, Grade.Mark
Student, Grade
Student.SSN=Grade.SSN
Student.Age ASC
2 
```

The sql query is transformed into proper python code using the following script. The script is effective for the following cases:
1. The text file follows the structure described above.
2. The ORDER BY clause contains only one attribute.
3. The sql query is correct according to the sql syntax.
4. The names of the tables and the attributes are correct.
5. In case a clause is skipped then the corresponding line remains blank, like the example below.

##### SQL Query without WHERE
``` mysql
SELECT Student.FName, Student.LName, Grade.Mark
FROM Student, Grade
ORDER BY Student.Age ASC
LIMIT 2 
```

##### SQL Query without WHERE in text file

``` mysql
Student.FName, Student.LName, Grade.Mark
Student, Grade

Student.Age ASC
2 
```
#### Steps

**1.** Clone this repository:
```shell
git clone https://github.com/dbsmasters/bdsmasters.git
cd /bdsmasters/redis_project
```
**2.** Install the required python packages.
```shell
pip install -r requirements.txt
```
**3.** Run redisQueryParser.py to execute the sql query in redis database.
```shell
python redisTableParser.py sqlQuery.txt queryRunner.py
```
**4.** Run the created python file to execute the query.
```shell
python queryRunner.py
```

After executing <b>STEP 4</b> results are printed on cmd while the file redisResults.csv is created containing the retrieved data.


### <a id="test-functionality" href="#test-functionality">Testing functionality</a>

Test basic functionality of the query parser.
```shell
python testRedisQueryParser.py
```

### <a id="team" href="#team">Team</a>
|[![Lamprini Koutsokera](https://s.gravatar.com/avatar/fbf0a9ea90d21fda02132701e8082bf2?s=144)](https://github.com/lamprini-koutsokera)|[![Stratos Gounidellis](https://s.gravatar.com/avatar/761a071e4bb22145269c5b33aab8249d?s=144)](https://github.com/stratos-gounidellis)|
|---|---|
|[![Lamprini Koutsokera](https://img.shields.io/badge/Lamprini-Koutsokera-brightgreen.svg?style=flat-square)](https://github.com/lamprini-koutsokera)|[![Stratos Gounidellis](https://img.shields.io/badge/Stratos-Gounidellis-blue.svg?style=flat-square)](https://github.com/stratos-gounidellis)|

### <a id="see-also" href="#see-also">See also</a>

External resources

* [Redis Quick Start - redis.io](https://redis.io/topics/quickstart)
