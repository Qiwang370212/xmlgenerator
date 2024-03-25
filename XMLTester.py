from flask import Flask, render_template, request
from lxml import etree

app = Flask(__name__)

# HTML form to upload XML and XSD files
@app.route('/')
def upload_form():
    return render_template('upload_form.html')

# Validation route
@app.route('/validate', methods=['POST'])
def validate():
    try:
        # Get uploaded files
        xml_file = request.files['xml']
        xsd_file = request.files['xsd']

        # Parse XML and XSD
        xml_doc = etree.parse(xml_file)
        xsd_doc = etree.parse(xsd_file)

        # Create XML Schema
        schema = etree.XMLSchema(xsd_doc)

        # Validate XML against XSD
        is_valid = schema.validate(xml_doc)

        if is_valid:
            result = "Validation successful: XML is valid against XSD."
        else:
            result = "Validation failed: XML is not valid against XSD."

    except Exception as e:
        result = f"An error occurred: {str(e)}"

    return result

if __name__ == '__main__':
    app.run(debug=True)
