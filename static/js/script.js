$(document).ready(function() {
    $('#PartneredInstitution').change(function() {
        if ($(this).val() === 'yes') {
            $('#partnered_institution_fields').show();
        } else {
            $('#partnered_institution_fields').hide();
        }
    });

    document.getElementById('CourseCurriculumTitle').addEventListener('change', function() {
        var selectedCourse = this.value;

        // Send an AJAX request to the server to get start date and end date based on selected course
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/get_course_dates?course=' + encodeURIComponent(selectedCourse), true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var courseDates = JSON.parse(xhr.responseText);
                var startDate = formatDate(courseDates.start_date);
                var endDate = formatDate(courseDates.end_date);
                document.getElementById('CourseStartDate').value = startDate;
                document.getElementById('ExpectedCourseEndDate').value = endDate;
            }
        };
        xhr.send();
    });

    // Function to format date as yyyy-mm-dd
    function formatDate(dateString) {
        var date = new Date(dateString);
        var year = date.getFullYear();
        var month = ('0' + (date.getMonth() + 1)).slice(-2); // Adding leading zero if needed
        var day = ('0' + date.getDate()).slice(-2); // Adding leading zero if needed
        return year + '-' + month + '-' + day;
    }
});
