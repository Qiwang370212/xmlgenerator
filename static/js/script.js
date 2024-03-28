$(document).ready(function() {

    $('#PartneredInstitution').change(function() {
        if ($(this).val() === 'yes') {
            $('#partnered_institution_fields').show();
        } else {
            $('#partnered_institution_fields').hide();
        }
    });

    // Add change event listener to CourseCurriculumTitle select element
    $('#CourseCurriculumTitle').change(function() {
        var selectedCourse = $(this).val();

        // Send an AJAX request to the server to get start date and end date based on selected course
        $.ajax({
            url: '/get_course_data',
            type: 'GET',
            data: { course: selectedCourse },
            success: function(courseData) {
                var startDate = formatDate(courseData.start_date);
                var endDate = formatDate(courseData.end_date);
                $('#CourseStartDate').val(startDate);
                $('#ExpectedCourseEndDate').val(endDate);
            },
            error: function(xhr, status, error) {
                console.error('Error occurred while fetching course dates:', error);
            }
        });
    });

    // Function to format date as yyyy-mm-dd
    function formatDate(dateString) {
        var date = new Date(dateString);
        var year = date.getFullYear();
        var month = ('0' + (date.getMonth() + 1)).slice(-2); // Adding leading zero if needed
        var day = ('0' + date.getDate()).slice(-2); // Adding leading zero if needed
        return year + '-' + month + '-' + day;
    }

    // Add change event listener to ProgramType radio buttons
    $('input[type=radio][name=ProgramType]').change(function() {
        if (this.value === 'part-time') {
            $('#hoursPerWeekField').show();
            $('input[name=CourseHoursPerWeek]').attr('required', true);
            $('input[name=CourseHoursPerWeek]').attr('placeholder', 'Enter hours per week');
            $('input[name=CourseHoursPerWeek]').val('');
            $('input[name=CourseHoursPerWeek]').focus();
        } else if (this.value === 'full-time') {
            $('#hoursPerWeekField').hide();
            $('input[name=CourseHoursPerWeek]').removeAttr('required');
            $('input[name=CourseHoursPerWeek]').attr('placeholder', '');
            $('input[name=CourseHoursPerWeek]').val('0.0');
        }
    });
});
