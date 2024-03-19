from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import datetime
import os
import xml.dom.minidom

app = Flask(__name__)

def append_to_xml(data):
    # Get today's date
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Generate filename with today's date
    filename = f"data_{today_date}.xml"
    
    # Construct the full path to the template XML file
    template_path = os.path.join("static", "template.xml")
    
    tree = ET.parse(template_path)  # XML file to append to
    root = tree.getroot()

    # Create new CAS element
    cas_element = ET.Element('CAS')  # Create CAS element

    # Iterate through data and add elements
    for category, values in data.items():
        category_element = ET.SubElement(cas_element, category)
        for key, value in values.items():
            sub_element = ET.SubElement(category_element, key)
            sub_element.text = value

    # Find the index of </ns1:CAS> in the root children
    index = None
    for i, child in enumerate(root):
        if child.tag.endswith('CAS'):
            index = i + 1
            break
    
    # Insert the new CAS element after </ns1:CAS>
    if index is not None:
        root.insert(index, cas_element)
    else:
        root.append(cas_element)  # If </ns1:CAS> not found, append at the end
    
    # Convert XML tree to a formatted string
    xml_str = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()

    # Write back to XML file
    with open(filename, "w") as f:
        f.write(xml_str)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            'ApplicantData': {
                'ApplicantID': request.form['ApplicantID'],
                'FamilyName': request.form['FamilyName'],
                'GivenName': request.form['GivenName'],
                'Nationality': request.form['Nationality'],
                'Gender': request.form['Gender'],
                'CountryOfBirth': request.form['CountryOfBirth'],
                'PlaceOfBirth': request.form['PlaceOfBirth'],
                'DateOfBirth': request.form['DateOfBirth'],
                'ApplicantPassportOrTravelDocumentNumber': request.form['ApplicantPassportOrTravelDocumentNumber']
            },
        }
        append_to_xml(data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port="8000")
