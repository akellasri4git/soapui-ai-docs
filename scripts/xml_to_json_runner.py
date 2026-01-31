from core.xml_to_json import XMLToJSONConverter

def main():
    converter = XMLToJSONConverter("input/Google-Maps-soapui-project.xml")
    converter.save_to_file("output/project_raw.json")
    print("✅ XML converted to JSON successfully")

if __name__ == "__main__":
    main()
