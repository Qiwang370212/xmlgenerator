from flask import Flask, render_template, request
from lxml import etree

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate_xml():
    xml_file = request.files['xml_file']
    xsd_file = request.files['xsd_file']

    xml_data = xml_file.read().decode('utf-8')
    xsd_data = xsd_file.read().decode('utf-8')

    try:
        xmlschema_doc = etree.parse(etree.fromstring(xsd_data))
        xmlschema = etree.XMLSchema(xmlschema_doc)
        xml_doc = etree.fromstring(xml_data)

        if xmlschema.validate(xml_doc):
            return 'XML is valid according to XSD.'
        else:
            return 'XML is not valid according to XSD.'
    except etree.XMLSyntaxError as e:
        return f'Error parsing XSD file: {e}'

if __name__ == '__main__':
    app.run(debug=True)
