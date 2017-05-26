<img src="../logos/logoAUEB.png" width="280" height="80" align="right"></img>
<img src="../logos/dmst.png" width="200" height="80" align="left"></img><br><br>
<br><br><br>
[![BDSMasters](https://img.shields.io/badge/codedby-bdsmasters-brightgreen.svg?style=flat-square)](https://github.com/dbsmasters)
![redis database](https://img.shields.io/badge/mongo-database-blue.svg?style=flat-square)

### <a id="contents" href="#contents">Contents</a>

1. [Mongo Project: Relational databases & Document-Oriented databases](#mongo-project-intro)
1. [MongoDB installation in Windows](#installing-mongo)
1. [Queries and the Aggregation Pipeline](#queries-aggregation)
1. [Python & MongoDB](#pymongo)
1. [MapReduce](#map-reduce)
1. [Team](#team)
1. [See also](#see-also)



### <a id="mongo-project-intro" href="#mongo-project-intro">Mongo Project: Relational databases & Document-Oriented databases</a>

This assignment is a part of a project implemented in the context of the course "Big Data Management Systems" taught by Prof. Chatziantoniou in the Department of Management Science and Technology (AUEB). The aim of the project is to familiarize the students with big data management systems such as Hadoop, Redis, MongoDB and Neo4j.

In the context of this assignment on Mongo, queries will be designed and executed on a mongo collection, simple operations on mongo will be executed with python while mapreduce jobs will also be designed and executed on a mongo collection.

A detailed description of the assignment can be found [here](Proj3_MongoDB_Description.pdf).

### <a id="installing-mongo" href="#installing-mongo">MongoDB installation in Windows</a>

1. Determine which MongoDB build you need.
```shell
wmic os get caption
wmic os get osarchitecture
```
2. Download MongoDB for [Windows](https://www.mongodb.com/download-center#community).
3. Install MongoDB Community Edition.
4. Set up the MongoDB environment.
```shell
md \data\db
```
### <a id="queries-aggregation" href="#queries-aggregation">Queries and the Aggregation Pipeline</a>
Using the load() function inside the mongo shell, load the prep.js file. This will create a students collection in whatever database you are currently using. The structure of an example object is like the following:
```json
{
 "_id": "ObjectId('558d08925e083d8cdd7be831')",
 "home_city": "Kalamata",
 "first_name": "Eirini",
 "hobbies": [
  "skydiving",
  "guitar",
  "AD&D"
 ],
 "favourite_os": "OS X",
 "laptop_cost": 1506,
 "courses": [{
   "course_code": "P102",
   "course_title": "Introduction to R",
   "course_status": "Complete",
   "grade": 10
  },
  {
   "course_code": "S102",
   "course_title": "Mathematical Statistics",
   "course_status": "In Progress"
  },
  {
   "course_code": "P201",
   "course_title": "Advanced R",
   "course_status": "In Progress"
  },
  {
   "course_code": "S202",
   "course_title": "Graph Theory",
   "course_status": "Complete",
   "grade": 7
  },
  {
   "course_code": "M102",
   "course_title": "Data Mining",
   "course_status": "In Progress"
  }
 ]
}
```

The following queries are designed and expressed in mongo query language. The execution code for the queries can be found in the file queries.js.
1. How many students in your database are currently taking at least 1 class (i.e. have a class with a course_status of “In Progress”)?
2. Produce a grouping of the documents that contains the name of each home city and the number of students enrolled from that home city.
3. Which hobby or hobbies are the most popular?
4. What is the GPA (ignoring dropped classes and in progress classes) of the best student?
5. Which student has the largest number of grade 10’s?
6. Which class has the highest average GPA? 
7. Which class has been dropped the most number of times?
8. Produce of a count of classes that have been COMPLETED by class type. The class type is found by taking the first letter of the course code so that M102 has type M.
9. Produce a transformation of the documents so that the documents now have an additional boolean field called “hobbyist” that is true when the student has more than 3 hobbies and false otherwise.
10. Produce a transformation of the documents so that the documents now have an additional field that contains the number of classes that the student has completed.
11. Produce a transformation of the documents in the collection so that they look like the following output. The GPA is the average grade of all the completed classes. The other two computed fields are the number of classes currently in progress and the number of classes dropped. No other fields should be in there. No other fields should be present.
```json
{
 "_id": "ObjectId('558d08925e083d8cdd7be831')",
 "first_name": "Eirini",
 "GPA": 8.5,
 "classesInProgress": 3,
 "droppedClasses": 0
}
```
12. Produce a NEW collection (HINT: Use $out in the aggregation pipeline) so that the new documents in this correspond to the classes on offer. The structure of the documents should be like the following output. The _id field should be the course code. The course_title is what it was before. The numberOfDropouts is the number of students who dropped out. The numberOfTimesCompleted is the number of students that completed this class. The currentlyRegistered array is an array of ObjectID’s corresponding to the students who are currently taking the class. Finally, for the students that completed the class, the maxGrade, minGrade and avgGrade are the summary statistics for that class.

```json
{
 "_id": "M102",

 "course_title": "Data Mining",

 "numberOfDropouts": 34,

 "numberOfTimesCompleted": 34,

 "currentlyRegistered": ["ObjectId('558d08925e083d8cdd7be831')", "…"],

 "maxGrade": 10,

 "minGrade": 2,

 "avgGrade": 7.6
}
```


### <a id="pymongo" href="#pymongo">Python & MongoDB</a>

#### Steps

**1.** Clone this repository:
```shell
git clone https://github.com/dbsmasters/bdsmasters.git
cd /bdsmasters/mongo_project
```
**2.** Install the required python packages.
```shell
pip install -r requirements.txt
```
**3.** Run python_mongodb.py to implement basic operations (insert_one, insert_many, update, delete_one, delete_many, etc.) on mongodb.
```shell
python python_mongodb.py
```

### <a id="map-reduce" href="#map-reduce">MapReduce</a>

1. Write a map reduce job on the students collection similar to the classic word count example. More specifically, implement a word count using the course title field as the text. In addition, exclude stop words from this list. You should find/write your own list of stop words. (Stop words are the common words in the English language like “a”, “in”, “to”, “the”, etc.)
```javascript
var mapWordCount = function() {
    var stopWords = "a, of, and, to, in, for, the";
    for (var idx = 0; idx < this.courses.length; idx++) {
        var course_title = this.courses[idx].course_title;
        course_title = course_title.toLowerCase().split(" ");
        for (var i = course_title.length - 1; i >= 0; i--) {
            var regex = new RegExp("\\b" + course_title[i] + "\\b", "i");
            if (stopWords.search(regex) < 0) {
                if (course_title[i]) {
                    emit(course_title[i], 1);
                }
            }
        }
    }
};

var reduceWordCount = function(key, values) {
    var count = 0;
    values.forEach(function(value) {
        count += value;
    });
    return count;
};

db.students.mapReduce(mapWordCount,
    reduceWordCount, {
        out: {
            merge: "count_courseTitle"
        }
    }
)

db.count_courseTitle.find().sort({"value": -1})
```

2. Write a map reduce job on the students collection whose goal is to compute average GPA scores for completed courses by home city and by course type (M, B, P, etc.).
```javascript
var mapAvgGrade = function() {
    for (var idx = 0; idx < this.courses.length; idx++) {
        var course_status = this.courses[idx].course_status;
        var course_grade = this.courses[idx].grade;
        if (course_status === "Complete") {
            var course_title = this.courses[idx].course_code;
            var key = {
                home_city: this.home_city,
                course_type: course_title[0],
            };
            var value = {
                count: 1,
                sum: course_grade
            };

            emit(key, value);
        }

    }
};

var reduceAvgGrade = function(key, values) {
    var reducedVal = {
        count: 0,
        sum: 0
    };

    values.forEach(function(value) {
        reducedVal.count += value.count;
        reducedVal.sum += value.sum;
    });

    return reducedVal;
};

var finalizeAvgGrade = function(key, reducedVal) {

    reducedVal.avg = (reducedVal.sum / reducedVal.count).toFixed(4);    

    return reducedVal.avg;

};

db.students.mapReduce(mapAvgGrade,
    reduceAvgGrade, {
        out: {
            merge: "avgGrade_city"
        },
        finalize: finalizeAvgGrade
    }
)

db.avgGrade_city.find().sort({"value": -1})
```

### <a id="team" href="#team">Team</a>
|[![Lamprini Koutsokera](https://s.gravatar.com/avatar/fbf0a9ea90d21fda02132701e8082bf2?s=144)](https://github.com/lamprini-koutsokera)|[![Stratos Gounidellis](https://s.gravatar.com/avatar/761a071e4bb22145269c5b33aab8249d?s=144)](https://github.com/stratos-gounidellis)|
|---|---|
|[![Lamprini Koutsokera](https://img.shields.io/badge/Lamprini-Koutsokera-brightgreen.svg?style=flat-square)](https://github.com/lamprini-koutsokera)|[![Stratos Gounidellis](https://img.shields.io/badge/Stratos-Gounidellis-blue.svg?style=flat-square)](https://github.com/stratos-gounidellis)|

### <a id="see-also" href="#see-also">See also</a>

External resources

* [MongoDB Installation - mongodb.com](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)
