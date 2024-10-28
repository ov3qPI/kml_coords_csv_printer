import os
import csv
import xml.etree.ElementTree as ET

def extract_placemarks(kml_file):
    tree = ET.parse(kml_file)
    root = tree.getroot()
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
    placemarks = root.findall('.//kml:Placemark', namespace)

    if not placemarks:
        print(".kml contains no placemarks")
        return []

    result = []
    for placemark in placemarks:
        name = placemark.find('kml:name', namespace)
        coordinates = placemark.find('.//kml:coordinates', namespace)
        if name is not None and coordinates is not None:
            result.append((name.text, coordinates.text.strip()))

    return result

def write_to_csv(placemarks, output_csv_path):
    with open(output_csv_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Name', 'Coordinates'])
        for name, coords in placemarks:
            writer.writerow([name, coords])

def main():
    kml_location = input("Enter .kml location: ")
    if not os.path.exists(kml_location):
        print(".kml file does not exist")
        return

    placemarks = extract_placemarks(kml_location)
    if placemarks:
        kml_filename = os.path.splitext(os.path.basename(kml_location))[0]
        output_csv_path = os.path.join(os.path.dirname(kml_location), f'{kml_filename}.csv')
        write_to_csv(placemarks, output_csv_path)
        print(f"Coordinates saved to {output_csv_path}")

if __name__ == "__main__":
    main()
