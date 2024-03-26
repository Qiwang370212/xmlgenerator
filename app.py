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

    country_nationality = pd.read_excel(excel_file, sheet_name='Nationality codes')
    nationality_countries = country_nationality['Nationality'].tolist()
    nationality_codes = country_nationality['Code'].tolist()
    nationality_options = zip(nationality_countries, nationality_codes)

    country_birth = pd.read_excel(excel_file, sheet_name='Country codes')
    birth_countries = country_birth['Nationality'].tolist()
    birth_codes = country_birth['Code'].tolist()
    birth_options = zip(birth_countries, birth_codes)

    course_titles = pd.read_excel(excel_file, sheet_name='Course Info')
    course_title_options = course_titles['Course Title'].tolist()

    academic_level = pd.read_excel(excel_file, sheet_name='Course Level')
    academic_display_text = academic_level['Display text'].tolist()
    academic_BDT_level = academic_level['BDT Code'].tolist()
    academic_level_options = zip(academic_display_text, academic_BDT_level)

    return render_template('XMLGenerator.html', nationality_options=nationality_options, birth_options=birth_options, course_title_options=course_title_options, academic_level_options=academic_level_options)

def append_to_xml(form_data):
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

    CourseDetails = ET.SubElement(CAS, 'CourseDetails')
    element = ET.SubElement(CourseDetails, 'CourseCurriculumTitle')
    element.text = form_data['CourseCurriculumTitle']

    element = ET.SubElement(CourseDetails, 'AcademicLevel')
    element.text = form_data['AcademicLevel']

    ET.indent(root, '  ')

    tree.write("static/Testing.xml", encoding="utf-8", xml_declaration=True)


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="5000")
