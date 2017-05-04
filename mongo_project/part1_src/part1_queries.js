/**
 * @author Stratos Gounidellis <stratos.gounidellis@gmail.com>
 * @author Lamprini Koutsokera <lkoutsokera@gmail.com>
 */

// Using the load() function inside the mongo shell, load the prep.js file
load('prep.js');

/* Q1: How many students in your database are currently taking at least 1
class (i.e. have a class with a course_status of "In Progress")?
*/

db.students.find({'courses.course_status': 'In Progress'}).count();

/* Q2: Produce a grouping of the documents that contains the name of each
home city and the number of students enrolled from that home city.
*/

db.students.aggregate(
    [
        {
            '$group': {
                _id: '$home_city',
                enrolledStudents: {
                    $sum: 1
                }
            }
        }
    ]
);

// Q3: Which hobby or hobbies are the most popular?

db.students.aggregate(
    [
        {
            $unwind: '$hobbies'
        },

        {
            '$group': {
                _id: '$hobbies',
                popularity: {
                    $sum: 1
                }
            }
        },

        {
            $sort: {
                popularity: -1
            }
        },

        {
            $limit: 1
        }
    ]
);

db.students.aggregate(
    [
        {
            $unwind: '$hobbies'
        },

        {
            '$group': {
                _id: '$hobbies',
                popularity: {
                    $sum: 1
                }
            }
        },

        {
            $sort: {
                popularity: -1
            }
        },

        {
            $limit: 5
        }
    ]
);

/* Q4: What is the GPA (ignoring dropped classes and in progress classes)
of the best student?
*/

db.students.aggregate(
    [
        {
            $match: {'courses.course_status': { $nin:
                ['In Progress', 'Dropped'] }}
        },
        {
            $unwind: '$courses'
        },
        {
            $group: {
               _id: '$_id',

               GPA: { $avg: '$courses.grade' }
            }
        },

        {$sort: {GPA: -1}},

        {$limit: 1}

   ]
);


// Q5: Which student has the largest number of grade 10's?

db.students.aggregate(
    [
        {
            $unwind: '$courses'
        },
        {
            $group: {
                _id: '$_id',
                countMaxGrade: {
                    $sum: {
                        $cond: [{
                            $eq: ['$courses.grade', 10]
                        }, 1, 0]
                    }
                }
            }
        },

        {
            $sort: {
                countMaxGrade: -1
            }
        },

        {
            $limit: 1
        }

    ]
);


// Q6: Which class has the highest average GPA?

db.students.aggregate(
    [
        {
            $unwind: '$courses'
        },
        {
            $group: {
                _id: '$courses.course_code',

                'course_title': {
                    '$first': '$courses.course_title'
                },

                avgGrade: {
                    $avg: '$courses.grade'
                }

            }
        },
        {
            $sort: {
                avgGrade: -1
            }
        },

        {
            $limit: 1
        }

    ]
).pretty();

// Q7: Which class has been dropped the most number of times?

db.students.aggregate(
    [
        {
            $unwind: '$courses'
        },
        {
            $group: {
                _id: '$courses.course_code',
                'course_name': {
                    '$first': '$courses.course_title'
                },
                numberOfDropouts: {
                    $sum: {
                        $cond: [{
                            $eq: ['$courses.course_status', 'Dropped']
                        }, 1, 0]
                    }
                }
            }
        },

        {
            $sort: {
                numberOfDropouts: -1
            }
        },

        {
            $limit: 1
        }

    ]
).pretty();


/* Q8: Produce of a count of classes that have been COMPLETED by class
type. The class type is found by taking the first letter of the course
code so that M102 has type M.
*/

db.students.aggregate(
   [
     {
         $unwind: '$courses'
     },
     {
         $group:
         {
           _id: { $substr: ['$courses.course_code', 0, 1] },
           numberOfTimesCompleted: {
               $sum: {
                   $cond: [{ $eq:
                    ['$courses.course_status', 'Complete'] }, 1, 0]
                }
            }
         }
     },

     {$sort: {numberOfTimesCompleted: -1}}

   ]
);

/* Q9: Produce a transformation of the documents so that the documents
now have an additional boolean field called "hobbyist" that is true
when the student has more than 3 hobbies and false otherwise.
*/

db.students.aggregate(
    [{
        $project: {
            home_city: 1,
            first_name: 1,
            hobbies: 1,
            hobbyist: {
                $cond: {
                    if: {
                        $gt: [{
                            $size: '$hobbies'
                        }, 3]
                    },
                    then: true,
                    else: false;
                }
            },
            favourite_os: 1,
            laptop_cost: 1,
            courses: 1
        }
    }]
);

/* Q10: Produce a transformation of the documents so that the documents
now have an additional field that contains the number of classes that
the student has completed.
*/

db.students.aggregate(
    [
        {
            $unwind: '$courses'
        },
        {
            $group: {
                _id: '$_id',
                'home_city': {
                    '$first': '$home_city'
                },
                'first_name': {
                    '$first': '$first_name'
                },
                'hobbies': {
                    '$first': '$hobbies'
                },
                'hobbyist': {
                    '$first': '$hobbyist'
                },
                'favourite_os': {
                    '$first': '$favourite_os'
                },
                'laptop_cost': {
                    '$first': '$laptop_cost'
                },
                'courses': {
                    '$push': '$courses'
                },
                completed_courses: {
                    $sum: {
                        $cond: [{
                            $eq: ['$courses.course_status', 'Complete']
                        }, 1, 0]
                    }
                }
            }
        }
    ]
).pretty();

/* Q11: Produce a transformation of the documents in the collection so that
they look like the following object.

The GPA is the average grade of all the completed classes. The other two
computed fields are the number of classes currently in progress and the
number of classes dropped. No other fields should be in there. No other
fields should be present.

{
 "_id": "ObjectId('558d08925e083d8cdd7be831')",
 "first_name": "Eirini",
 "GPA": 8.5,
 "classesInProgress": 3,
 "droppedClasses": 0
}

*/
db.students.aggregate(
    [
        {
            $unwind: '$courses'
        },
        {
            $group: {
                _id: '$_id',
                'first_name': {
                    '$first': '$first_name'
                },
                GPA: {
                    $avg: '$courses.grade'
                },
                classesInProgress: {
                    $sum: {
                        $cond: [{
                            $eq: ['$courses.course_status', 'In Progress']
                        }, 1, 0]
                    }
                },
                droppedClasses: {
                    $sum: {
                        $cond: [{
                            $eq: ['$courses.course_status', 'Dropped']
                        }, 1, 0]
                    }
                }
            }
        }

    ]
).pretty();

/* Q12: Produce a NEW collection (HINT: Use $out in the aggregation pipeline)
so that the new documents in this correspond to the classes on offer. The
structure of the documents should be like the following object.

The _id field should be the course code. The course_title is what it was before.
The numberOfDropouts is the number of students who dropped out. The
numberOfTimesCompleted is the number of students that completed this class.
The currentlyRegistered array is an array of ObjectID's corresponding to the
students who are currently taking the class. Finally, for the students that
completed the class, the maxGrade, minGrade and avgGrade are the summary
statistics for that class.

{
 "_id": "M102",

 "course_title": "Data Mining",

 "numberOfDropouts": 34,

 "numberOfTimesCompleted": 34,

 "currentlyRegistered": ["ObjectId('558d08925e083d8cdd7be831')", "..."],

 "maxGrade": 10,

 "minGrade": 2,

 "avgGrade": 7.6
}

*/

db.students.aggregate(
    [
        {
            $unwind: '$courses'
        },
        {
            $group: {
                _id: '$courses.course_code',

                course_title: {
                    '$first': '$courses.course_title'
                },
                numberOfDropouts: {
                    $sum: {
                        $cond: [{
                            $eq: ['$courses.course_status', 'Dropped']
                        }, 1, 0]
                    }
                },
                numberOfTimesCompleted: {
                    $sum: {
                        $cond: [{
                            $eq: ['$courses.course_status', 'Complete']
                        }, 1, 0]
                    }
                },
                currentlyRegistered: {
                    $push: {
                        $cond: [{
                            $eq: ['$courses.course_status', 'In Progress']
                        }, '$_id', null]
                    }
                },
                maxGrade: {
                    $max: '$courses.grade'
                },
                minGrade: {
                    $min: '$courses.grade'
                },
                avgGrade: {
                    $avg: '$courses.grade'
                },

            }
        },
        {
            $addFields: {
                'currentlyRegistered': {
                    '$setDifference': ['$currentlyRegistered', [null]]
                }
            }
        },
        {
            $out: 'classes'
        }
    ]
);
