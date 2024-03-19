from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import datetime

app = Flask(__name__)

def append_to_xml(first_name, last_name):
    # Get today's date
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Generate filename with today's date
    filename = f"data_{today_date}.xml"
    
    tree = ET.parse('data.xml')  # XML file to append to
    root = tree.getroot()
    
    # Create new entry
    new_entry = ET.Element('person')
    first_name_element = ET.SubElement(new_entry, 'first_name')
    first_name_element.text = first_name
    last_name_element = ET.SubElement(new_entry, 'last_name')
    last_name_element.text = last_name
    
    # Append new entry to root
    root.append(new_entry)
    
    # Write back to XML file with pretty printing and today's date as filename
    tree.write(filename, xml_declaration=True, pretty_print=True)
if __name__ == '__main__':
    app.run(debug=True)
