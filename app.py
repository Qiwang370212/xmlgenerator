from flask import Flask, render_template, request, jsonify, redirect, url_for
import xml.etree.ElementTree as ET
import pandas as pd
import os
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_form():
    if request.method == 'POST':
        try:
            append_to_xml(request.form)
            return "Form submitted successfully!"
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return index()

# Function to load templates from JSON file
def load_templates():
    # Get the root directory
    root_directory = os.path.abspath("templates/templates.json")
    
    # Load and return the JSON data
    with open(root_directory, 'r') as json_file:
        return json.load(json_file)
    

@app.route('/edit_template')
def edit_template():
    templates = load_templates()
    qualification_template = templates['qualification_template']
    english_qualification_template = templates['english_qualification_template']
    english_speaking_template = templates['english_speaking_template']  # Add this line
    return render_template('edit_template.html', 
                           qualification_template=qualification_template, 
                           english_qualification_template=english_qualification_template,
                           english_speaking_template=english_speaking_template)  # Update context

@app.route('/save_templates', methods=['POST'])
def save_templates():
    qualification_placeholder = request.form['qualificationPlaceholder']
    english_qualification_placeholder = request.form['englishQualificationPlaceholder']
    english_speaking_placeholder = request.form['englishSpeakingPlaceholder']  # New line
    templates = load_templates()
    templates['qualification_template']['placeholder'] = qualification_placeholder
    templates['english_qualification_template']['placeholder'] = english_qualification_placeholder
    templates['english_speaking_template']['placeholder'] = english_speaking_placeholder  # New line
    # Additional processing or saving of templates may be required here

    # Construct the absolute path to the JSON file
    json_file_path = os.path.join('templates', 'templates.json')

    # Save the updated templates to templates/templates.json
    with open(json_file_path, 'w') as json_file:
        json.dump(templates, json_file, indent=4)

    return redirect(url_for('index'))


excel_file = os.path.join(app.root_path, 'static', 'data_base.xlsx')

@app.route('/get_course_data')
def get_course_dates():
    selected_course = request.args.get('course')

    # Read the Excel file and extract start date and end date based on the selected course
    course_data = pd.read_excel(excel_file, sheet_name='Course Info')
    course_row = course_data.loc[course_data['Course Title'] == selected_course]
    start_date = course_row['Start Date'].values[0]
    end_date = course_row['End Date'].values[0]

    return jsonify({'start_date': str(start_date), 'end_date': str(end_date)})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            append_to_xml(request.form)
            return "Form submitted successfully!"
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        templates = load_templates()
        qualification_template = templates['qualification_template']
        english_qualification_template = templates['english_qualification_template']
        english_speaking_template = templates['english_speaking_template']  # Add this line

        # Read nationality data
        nationality_data = pd.read_excel(excel_file, sheet_name='Nationality codes')
        nationality_options = zip(nationality_data['Nationality'].tolist(), nationality_data['Code'].tolist())

        # Read birth country data
        birth_country_data = pd.read_excel(excel_file, sheet_name='Country codes')
        birth_options = zip(birth_country_data['Nationality'].tolist(), birth_country_data['Code'].tolist())

        # Read course title data
        course_data = pd.read_excel(excel_file, sheet_name='Course Info')
        course_title_options = course_data['Course Title'].tolist()
        
        # Read academic level data
        academic_level_data = pd.read_excel(excel_file, sheet_name='Course Level')
        academic_level_options = zip(academic_level_data['Display text'].tolist(), academic_level_data['BDT Code'].tolist())

        # Read country data
        country_data = pd.read_excel(excel_file, sheet_name='Country codes')
        country_options = zip(country_data['Nationality'].tolist(), country_data['Code'].tolist())

        return render_template('CAS Generator.html', 
                               qualification_template=qualification_template,
                               english_qualification_template=english_qualification_template,
                               english_speaking_template=english_speaking_template,
                               nationality_options=nationality_options, 
                               birth_options=birth_options, 
                               course_title_options=course_title_options, 
                               academic_level_options=academic_level_options, 
                               country_options=country_options)

def append_to_xml(form_data):
    try:
        # Check if Testing.xml exists in uploads/xml folder
        if os.path.exists('uploads/xml/Testing.xml'):
            xml_path = 'uploads/xml/Testing.xml'
        else:
            xml_path = 'static/Testing.xml'

        tree = ET.parse(xml_path)
        root = tree.getroot()

        CAS = ET.Element('CAS')
        root.append(CAS)

        ApplicantData = ET.SubElement(CAS, 'ApplicantData')
        for field in ['ApplicantID', 'FamilyName', 'GivenName', 'Nationality', 'Gender', 'CountryOfBirth', 'DateOfBirth', 'ApplicantPassportOrTravelDocumentNumber']:
            element = ET.SubElement(ApplicantData, field)
            if field == 'DateOfBirth':  
                FullDate_element = ET.SubElement(element, 'FullDate')
                FullDate_element.text = form_data.get(field, '')  # Default to empty string if not provided
            elif field == 'GivenName':
                given_name = form_data.get('FirstName', '') + ' ' + form_data.get('MiddleName', '')
                element.text = given_name.strip()
            else:
                element.text = form_data.get(field, '')  # Default to empty string if not provided

        if form_data.get('PartneredInstitution') == 'yes':
            NonSponsorEducationInstitutionData = ET.SubElement(CAS, 'NonSponsorEducationInstitutionData')
            PartnerInstitutionDetails = ET.SubElement(NonSponsorEducationInstitutionData, 'PartnerInstitutionDetails')
            Name = ET.SubElement(PartnerInstitutionDetails, 'Name')
            Name.text = form_data.get('PartneredInstitutionName', '')
            AddressDetails = ET.SubElement(PartnerInstitutionDetails, 'AddressDetails')
            for field in ['AddressLine', 'City', 'CountyAreaDistrict', 'PostCode', 'Country']:
                element = ET.SubElement(AddressDetails, field)
                if field == 'Country':
                    # Access the country field directly without concatenating
                    element.text = form_data.get(field, '')  # Default to empty string if not provided
                else:
                    element.text = form_data.get('PartneredInstitution' + field, '')  # Default to empty string if not provided
        else:
            NonSponsorEducationInstitutionData = ET.SubElement(CAS, 'NonSponsorEducationInstitutionData')

        CourseDetails = ET.SubElement(CAS, 'CourseDetails')
        
        element = ET.SubElement(CourseDetails, 'CourseCurriculumTitle')
        element.text = form_data.get('CourseCurriculumTitle', '')  # Default to empty string if not provided

        element = ET.SubElement(CourseDetails, 'AcademicLevel')
        element.text = form_data.get('AcademicLevel', '')  # Default to empty string if not provided

        element = ET.SubElement(CourseDetails, 'CourseStartDate')
        element.text = form_data.get('CourseStartDate', '')  # Default to empty string if not provided

        latest_date = form_data.get('LatestDateForAcceptanceOnCourse')
        if latest_date:
            element = ET.SubElement(CourseDetails, 'LatestDateForAcceptanceOnCourse')
            element.text = latest_date

        element = ET.SubElement(CourseDetails, 'ExpectedCourseEndDate')
        element.text = form_data.get('ExpectedCourseEndDate', '')  # Default to empty string if not provided

        program_type = form_data.get('ProgramType')
        if program_type == 'full-time':
            full_time_element = ET.SubElement(CourseDetails, 'CourseIsFullTime')
            full_time_element.text = 'true'
            hours_per_week_element = ET.SubElement(CourseDetails, 'CourseHoursPerWeek')
            hours_per_week_element.text = '0.0'
        elif program_type == 'part-time':
            full_time_element = ET.SubElement(CourseDetails, 'CourseIsFullTime')
            full_time_element.text = 'false'
            hours_per_week_element = ET.SubElement(CourseDetails, 'CourseHoursPerWeek')
            hours_per_week = form_data.get('CourseHoursPerWeek', '')  # Default to empty string if not provided
            if hours_per_week:
                hours_per_week_element.text = hours_per_week

        selected_site = form_data.get('MainSiteOfStudy')

        address_sets = {
            'site1': {
                'AddressLine': '4-22 Arch Buildings',
                'City': 'Croydon',
                'CountyAreaDistrict': 'Surrey',
                'PostCode': 'CR0 2DY'
            },
            'site2': {
                'AddressLine': 'Another Address',
                'City': 'Another City',
                'CountyAreaDistrict': 'Another District',
                'PostCode': 'Another Postcode'
            }
            # Add more address sets as needed
        }

        main_site_element = ET.SubElement(CourseDetails, 'MainSiteOfStudy')
        address_set = address_sets.get(selected_site, {})
        for field, value in address_set.items():
            element = ET.SubElement(main_site_element, field)
            element.text = value

        applicant_work_placement = ET.SubElement(CAS, 'ApplicantHasWorkPlacement')
        applicant_work_placement.text = 'false'

        Documentation = ET.Element('Documentation')
        CAS.append(Documentation)

        DocumentsUsedToObtainOffer = ET.SubElement(Documentation, 'DocumentsUsedToObtainOffer')
        qualification_value = form_data.get('qualification', '')
        english_qualification_value = form_data.get('englishQualification', '')
        DocumentsUsedToObtainOffer.text = f'{qualification_value}\n{english_qualification_value}'

        CourseRequiresATAS = ET.SubElement(Documentation, 'CourseRequiresATAS')
        CourseRequiresATAS.text = 'false'

        PostgraduateDeanCertificateRequired = ET.SubElement(Documentation, 'PostgraduateDeanCertificateRequired')
        PostgraduateDeanCertificateRequired.text = 'false'

        ET.indent(root, '  ')

        tree.write("uploads/xml/Testing.xml", encoding="utf-8", xml_declaration=True)
        return True, "Form submitted successfully!"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="8000")
