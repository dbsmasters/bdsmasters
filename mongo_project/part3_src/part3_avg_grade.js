/**
 * @author Stratos Gounidellis <stratos.gounidellis@gmail.com>
 * @author Lamprini Koutsokera <lkoutsokera@gmail.com>
 */

var mapAvgGrade = function() {
    // Iterate over the courses in each document
    for (var idx = 0; idx < this.courses.length; idx++) {
        var course_status = this.courses[idx].course_status;
        var course_grade = this.courses[idx].grade;
        // Check that the course status is complete
        if (course_status === 'Complete') {
            var course_title = this.courses[idx].course_code;
            // Set as key the home city and the course type
            var key = {
                home_city: this.home_city,
                course_type: course_title[0]
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
    // Calculate the average grade
    reducedVal.avg = (reducedVal.sum / reducedVal.count).toFixed(4);

    return reducedVal.avg;

};

db.students.mapReduce(mapAvgGrade,
    reduceAvgGrade, {
        // Save the results at a collection
        out: {
            merge: 'avgGrade_city'
        },
        finalize: finalizeAvgGrade
    }
);

db.avgGrade_city.find().sort({'value': -1});
