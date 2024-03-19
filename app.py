from flask import Flask, render_template, request, jsonify
from xml.etree.ElementTree import ElementTree, Element, SubElement, tostring, parse
import pandas as pd


app = Flask(__name__)

# Read the Excel file
df = pd.read_excel('static/countrycode.xlsx', sheet_name='Nationality codes')

# Create a dictionary from the DataFrame
countries_dict = dict(zip(df['Nationality'], df['Code']))

# Read the initial XML data from the file
initial_xml_file = 'static/template.xml'
tree = parse(initial_xml_file)
root = tree.getroot()

@app.route('/')
def index():
    return render_template('index.html', countries=countries_dict)

@app.route('/add_cas', methods=['POST'])
def add_cas():
    # Find the last CAS element
    last_cas_element = root.find('.//CAS[last()]')

    # Create a new CAS element
    cas_element = SubElement(root, 'CAS')

    # Extract data from the form
    applicant_id = request.form['applicant_id']
    family_name = request.form['family_name']
    given_name = request.form['given_name']
    nationality = request.form['nationality']
    gender = request.form['gender']  # Retrieve the selected value from the dropdown menu
    country_of_birth = request.form['country_of_birth']
    year_of_birth = request.form['year_of_birth']
    passport_number = request.form['passport_number']

    # Convert gender to the required numeric value
    if gender == 'Male':
        gender_value = '1'
    else:  # Assume Female
        gender_value = '2'

    # Add form data as child elements
    applicant_data_element = SubElement(cas_element, 'ApplicantData')
    SubElement(applicant_data_element, 'ApplicantID').text = applicant_id
    SubElement(applicant_data_element, 'FamilyName').text = family_name
    SubElement(applicant_data_element, 'GivenName').text = given_name
    SubElement(applicant_data_element, 'Nationality').text = nationality
    SubElement(applicant_data_element, 'Gender').text = gender_value  # Use the converted value
    SubElement(applicant_data_element, 'CountryOfBirth').text = country_of_birth
    date_of_birth_element = SubElement(applicant_data_element, 'DateOfBirth')
    SubElement(date_of_birth_element, 'Year').text = year_of_birth
    SubElement(applicant_data_element, 'ApplicantPassportOrTravelDocumentNumber').text = passport_number

    # Move the new CAS element after the last CAS element
    if last_cas_element is not None:
        root.insert(root.index(last_cas_element) + 1, cas_element)
    else:
        root.append(cas_element)

    # Save the updated XML document back to the file
    tree.write(initial_xml_file)

    # Return the updated XML document
    return tostring(root)

@app.route('/print_data')
def print_data():
    data = []

    for cas_element in root.findall('.//CAS'):
        cas_data = {}
        applicant_data = cas_element.find('ApplicantData')
        cas_data['ApplicantID'] = applicant_data.findtext('ApplicantID')
        cas_data['FamilyName'] = applicant_data.findtext('FamilyName')
        cas_data['GivenName'] = applicant_data.findtext('GivenName')
        cas_data['Nationality'] = applicant_data.findtext('Nationality')
        cas_data['Gender'] = applicant_data.findtext('Gender')
        cas_data['CountryOfBirth'] = applicant_data.findtext('CountryOfBirth')
        cas_data['DateOfBirth'] = applicant_data.findtext('DateOfBirth/Year')
        cas_data['PassportOrTravelDocumentNumber'] = applicant_data.findtext('ApplicantPassportOrTravelDocumentNumber')

        data.append(cas_data)

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
