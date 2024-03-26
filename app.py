from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import pandas as pd
import os

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

def index():
    excel_file = os.path.join(app.root_path, 'static', 'countrycode.xlsx')

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

    return render_template('XMLGenerator.html', nationality_options=nationality_options, 
                           birth_options=birth_options, course_title_options=course_title_options, 
                           academic_level_options=academic_level_options, country_options=country_options)

def append_to_xml(form_data):
    try:
        tree = ET.parse('static/Testing.xml')
        root = tree.getroot()

        CAS = ET.Element('CAS')
        root.append(CAS)

        ApplicantData = ET.SubElement(CAS, 'ApplicantData')
        for field in ['ApplicantID', 'FamilyName', 'GivenName', 'Nationality', 'Gender', 'CountryOfBirth', 'DateOfBirth', 'ApplicantPassportOrTravelDocumentNumber']:
            element = ET.SubElement(ApplicantData, field)
            if field == 'DateOfBirth':  
                FullDate_element = ET.SubElement(element, 'FullDate')
                FullDate_element.text = form_data[field]
            elif field == 'GivenName':
                given_name = form_data.get('FirstName', '') + ' ' + form_data.get('MiddleName', '')
                element.text = given_name.strip()
            else:
                element.text = form_data[field]

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
                    element.text = form_data.get(field, '')
                else:
                    element.text = form_data.get('PartneredInstitution' + field, '')
        else:
            NonSponsorEducationInstitutionData = ET.SubElement(CAS, 'NonSponsorEducationInstitutionData')

        CourseDetails = ET.SubElement(CAS, 'CourseDetails')
        element = ET.SubElement(CourseDetails, 'CourseCurriculumTitle')
        element.text = form_data.get('CourseCurriculumTitle', '')

        element = ET.SubElement(CourseDetails, 'AcademicLevel')
        element.text = form_data.get('AcademicLevel', '')

        element = ET.SubElement(CourseDetails, 'CourstStartDate')
        element.text = form_data.get('CourstStartDate', '')

        latest_date = form_data.get('LatestDateForAcceptanceOnCourse')
        if latest_date:
            element = ET.SubElement(CourseDetails, 'LatestDateForAcceptanceOnCourse')
            element.text = latest_date

        element = ET.SubElement(CourseDetails, 'ExpectedCourseEndDate')
        element.text = form_data.get('ExpectedCourseEndDate', '')

        ET.indent(root, '  ')

        tree.write("static/Testing.xml", encoding="utf-8", xml_declaration=True)
        return True, "Form submitted successfully!"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="5000")
