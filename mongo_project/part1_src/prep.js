home_cities = ["Athina", "Kalamata", "Larissa", "Katerini", "Thessaloniki", "Pyrgos", 
"Patra", "Messolongi", "Agrinio", "Ioannina", "Arta", "Florina", "Preveza", "Irakleio", 
"Halkida", "Kavala", "Mytilini", "Chania", "Rethymno", "Thyra"];

first_names = ["Despoina", "Eleni", "Giorgos", "Giannis", "Kostas", "Pavlos", 
"Maria", "Anna", "Georgia", "Myrto", "Alexandra", "Nikos",
"Thanos", "Sokratis", "Clio", "Vangelis", "Iris", "Eirini", "Danae", "Miltos"];

hobbies = ["gardening", "skydiving", "ventriloquism", "skiing", "swimming", "watercolour painting",
"guitar", "poetry", "archaeology", "snooker", "board games", "model cars", "AD&D",
"paintball", "hiking", "philately", "coin collecting", "piano", "cinema", "World of Warcraft"];

osystems = ["windows", "linux", "OS X"];

course_codes = ["S201", "D101", "D102", "D103", "B101", "M102", "M101", 
"S102", "P102", "P201", "S101", "M201", "P101", "P201", "M201", "S202", "V101", "V102", "P101", "P103"];

course_titles = ["Predictive Modeling", "Essentials of MongoDB", "MongoDB Operations", 
"Introduction to HBase", "Hadoop and MapReduce", "Data Mining", "Machine Learning", "Mathematical Statistics", 
"Introduction to R", "Advanced R", "Fundamentals of Probability", "Natural Language Porcessing", 
"Algorithms and Data Structures", "Graph Algorithms", "Neural Networks", "Graph Theory", "Information Visualization", 
"Tableau for Data Scientists", "Object Oriented Programming in Java", "Node.js in Action"];

for (i=0; i<10000; i++) {

	// Compute helper variables for student properties
	core_ability = Math.floor((Math.random()*6)+5);
	number_of_courses = Math.floor((Math.random()*3)+Math.floor(core_ability/2));
	number_of_hobbies = Math.floor((Math.random()*4)+1);

	// Build student object
	student = new Object();
	student.home_city = home_cities[Math.floor((Math.random()*20))];
	student.first_name = first_names[Math.floor((Math.random()*20))];

	student_hobbies = new Array();
	for (j=0; j<number_of_hobbies; j++) {
		hobby = hobbies[Math.floor((Math.random()*20))];
		// We don't want duplicates
		while (student_hobbies.indexOf(hobby)>-1) {
			hobby = hobbies[Math.floor((Math.random()*20))];
		}
		student_hobbies[j] = hobby;
	}
	student.hobbies = student_hobbies;
	student.favourite_os = osystems[Math.floor((Math.random()*3))];
	student.laptop_cost = 800 + Math.floor((Math.random()*1000));

	student_courses = new Array();
	course_code_temps = new Array();
	for (j=0; j<number_of_courses; j++) {
		course_rnd = Math.floor((Math.random()*20));
		course_code = course_codes[course_rnd];
		// We don't want duplicates
		while (course_code_temps.indexOf(course_code)>-1) {
			course_rnd = Math.floor((Math.random()*20));
			course_code = course_codes[course_rnd];
		}
		course = new Object();
		course.course_code = course_code;
		course.course_title = course_titles[course_rnd];
		status_rnd = Math.floor((Math.random()*10)+1);
		if (status_rnd>5) {
			course.course_status = "Complete";
			course.grade = Math.max(Math.min(core_ability + Math.floor((Math.random()*5)-2),10),1);
		} else if (status_rnd>1) {
			course.course_status = "In Progress";
		} else {
			course.course_status = "Dropped";
		}
		student_courses[j] = course;
	}
	student.courses = student_courses;
	db.students.insert(student);

}