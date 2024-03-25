from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_form():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        append_to_xml(first_name, last_name)
        return "Form submitted successfully!"
    return render_template('XMLGenerator.html')

def append_to_xml(first_name, last_name):
    tree = ET.parse('static/Testing.xml')
    root = tree.getroot()

    person = ET.SubElement(root, 'person')
    first = ET.SubElement(person, 'first')
    first.text = first_name
    last = ET.SubElement(person, 'last')
    last.text = last_name

    # Serialize the XML element tree to a string
    xml_str = ET.tostring(root, encoding='utf-8')
    
    # Parse the XML string to an XML document
    xml_doc = minidom.parseString(xml_str)
    
    # Get the XML as a string without extra newlines
    pretty_xml_str = xml_doc.toxml(encoding='utf-8')
    ET.indent(tree, '  ')
    # Write the XML string to a file
    tree.write("modifyed.xml", encoding="utf-8", xml_declaration=True)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="8000")
