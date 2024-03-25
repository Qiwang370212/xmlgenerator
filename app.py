from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import pandas as pd
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_form():
    if request.method == 'POST':
        append_to_xml(request.form)
        return "Form submitted successfully!"
    # Call index function to render the template with nationality options
    return index()

def index():
    # Define the path to the Excel file
    excel_file = os.path.join(app.root_path, 'static', 'countrycode.xlsx')

    country_nationality = pd.read_excel(excel_file, sheet_name='Nationality codes')
    nationality_countries = country_nationality['Nationality'].tolist()
    nationality_codes = country_nationality['Code'].tolist()
    nationality_options = zip(nationality_countries, nationality_codes)

    country_birth = pd.read_excel(excel_file, sheet_name='Country codes')
    birth_countries = country_birth['Nationality'].tolist()
    birth_codes = country_birth['Code'].tolist()
    birth_options = zip(birth_countries, birth_codes)

    return render_template('XMLGenerator.html', nationality_options=nationality_options, birth_options=birth_options)

def append_to_xml(form_data):
    tree = ET.parse('static/Testing.xml')
    root = tree.getroot()

    CAS = ET.Element('CAS')
    root.append(CAS)

    # Append data to ApplicantData
    ApplicantData = ET.SubElement(CAS, 'ApplicantData')
    for field in ['ApplicantID', 'FamilyName', 'GivenName', 'Nationality', 'Gender', 'CountryOfBirth', 'DateOfBirth', 'ApplicantPassportOrTravelDocumentNumber']:
        element = ET.SubElement(ApplicantData, field)
        # Special handling for DateOfBirth field
        if field == 'DateOfBirth':  
            FullDate_element = ET.SubElement(element, 'FullDate')
            FullDate_element.text = form_data[field]
        elif field == 'Nationality':
            element.text = form_data.get(field, '')  # Get the value from the form data
        else:
            element.text = form_data[field]

    # Append data to CourseDetails
    CourseDetails = ET.SubElement(CAS, 'CourseDetails')
    element = ET.SubElement(CourseDetails, 'CourseCurriculumTitle')
    element.text = form_data['CourseCurriculumTitle']

    ET.indent(root, '  ')

    tree.write("static/Testing.xml", encoding="utf-8", xml_declaration=True)


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="5000")
