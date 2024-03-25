from flask import Flask, render_template, request, redirect, url_for
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Function to append first name and last name to XML file
def append_to_xml(first_name, last_name):
    tree = ET.parse('data.xml')
    root = tree.getroot()

    person = ET.SubElement(root, 'person')
    first = ET.SubElement(person, 'first')
    first.text = first_name
    last = ET.SubElement(person, 'last')
    last.text = last_name

    tree.write('data.xml')

# Route for the entry form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        append_to_xml(first_name, last_name)
        return redirect(url_for('index'))
    return render_template('templates/XMLGenerator.html')

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="8000")
