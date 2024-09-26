# Script to create CSV data file from Pascal VOC annotation files
# Based off code from GitHub user datitran: https://github.com/datitran/raccoon_dataset/blob/master/xml_to_csv.py

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(os.path.join(path, '*.xml')):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        filename = root.find('filename').text if root.find('filename') is not None else 'unknown'

        # Check if 'size' and its children exist
        size = root.find('size')
        width = int(float(size.find('width').text)) if size is not None and size.find('width') is not None else 0
        height = int(float(size.find('height').text)) if size is not None and size.find('height') is not None else 0

        for member in root.findall('object'):
            # Check if 'bndbox' and its children exist
            bndbox = member.find('bndbox')
            if bndbox is not None:
                # Convert to float and round if necessary
                xmin = round(float(bndbox.find('xmin').text)) if bndbox.find('xmin') is not None else 0
                ymin = round(float(bndbox.find('ymin').text)) if bndbox.find('ymin') is not None else 0
                xmax = round(float(bndbox.find('xmax').text)) if bndbox.find('xmax') is not None else 0
                ymax = round(float(bndbox.find('ymax').text)) if bndbox.find('ymax') is not None else 0

                value = (filename,
                         width,
                         height,
                         member.find('name').text if member.find('name') is not None else 'unknown',
                         xmin,
                         ymin,
                         xmax,
                         ymax
                         )
                xml_list.append(value)

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def main():
    for folder in ['train', 'validation']:
        image_path = os.path.join(os.getcwd(), 'images', folder)
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv(os.path.join('images', f'{folder}_labels.csv'), index=False)
        print(f'Successfully converted XML files in {folder} to CSV.')

if __name__ == "__main__":
    main()
