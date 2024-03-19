import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from lxml import etree


class XMLValidatorApp:
    def __init__(self, master):
        self.master = master
        master.title("XML Validator")

        self.label = tk.Label(master, text="Select XML and XSD files to validate:")
        self.label.pack()

        self.xml_button = tk.Button(master, text="Select XML File", command=self.select_xml_file)
        self.xml_button.pack()

        self.xsd_button = tk.Button(master, text="Select XSD File", command=self.select_xsd_file)
        self.xsd_button.pack()

        self.validate_button = tk.Button(master, text="Validate", command=self.validate)
        self.validate_button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        self.xml_file_path = ""
        self.xsd_file_path = ""

    def select_xml_file(self):
        self.xml_file_path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
        if self.xml_file_path:
            self.label.config(text=f"Selected XML File: {self.xml_file_path}")

    def select_xsd_file(self):
        self.xsd_file_path = filedialog.askopenfilename(filetypes=[("XSD Files", "*.xsd")])
        if self.xsd_file_path:
            self.label.config(text=f"Selected XSD File: {self.xsd_file_path}")

    def validate(self):
        if not self.xml_file_path or not self.xsd_file_path:
            messagebox.showerror("Error", "Please select both XML and XSD files.")
            return

        try:
            xml_tree = etree.parse(self.xml_file_path)
            xsd_schema = etree.parse(self.xsd_file_path)
            xml_schema = etree.XMLSchema(xsd_schema)
            xml_schema.assertValid(xml_tree)
            messagebox.showinfo("Validation Result", "XML is valid according to XSD.")
        except etree.XMLSyntaxError as e:
            messagebox.showerror("Error", f"XML Syntax Error: {e}")
        except etree.DocumentInvalid as e:
            messagebox.showerror("Error", f"XML Validation Error: {e}")


def main():
    root = tk.Tk()
    app = XMLValidatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
