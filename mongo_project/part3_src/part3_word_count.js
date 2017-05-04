/**
 * @author Stratos Gounidellis <stratos.gounidellis@gmail.com>
 * @author Lamprini Koutsokera <lkoutsokera@gmail.com>
 */

var mapWordCount = function() {
    // Declare a string with the stop words
    var stopWords = 'a, of, and, to, in, for, the';
    // Iterate over the courses in each document
    for (var idx = 0; idx < this.courses.length; idx++) {
        var course_title = this.courses[idx].course_title;
        // Convert to lowercase in order to avoid duplicates
        course_title = course_title.toLowerCase().split(' ');
        for (var i = course_title.length - 1; i >= 0; i--) {
            var regex = new RegExp('\\b' + course_title[i] + '\\b', 'i');
            // Check whether the word is a stop word or not
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
    // Sum the occureces of a word
    values.forEach(function(value) {
        count += value;
    });
    return count;
};

db.students.mapReduce(mapWordCount,
    reduceWordCount, {
        // Save the results at a collection
        out: 'count_courseTitle'
    }
);

db.count_courseTitle.find().sort({'value': -1});
