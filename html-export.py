import json
import sys
import argparse

def get_printable_title(header):
    replace_names = {
        'Start (date)': 'Date',
        'Start (time)': 'Start',
        'End (time)': 'End',
    }
    if header in replace_names:
        return replace_names[header]
    return header

def generate_html(headers, talks):

    # Begin the HTML document with basic CSS and print configurations
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sessions</title>
    <style>
        /* Base styles for screen viewing */
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            color: #333;
        }
        h1 {
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f4f4f4;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        /* Styles applied specifically when printing */
        @media print {
            body {
                margin: 0;
            }
            table {
                page-break-inside: auto; /* Ensures table behaves well across pages */
            }
            tr {
                page-break-inside: avoid; /* Prevents a row from being split in half */
                page-break-after: auto;
            }
            th {
                background-color: #e0e0e0 !important;
                -webkit-print-color-adjust: exact; /* Ensures background prints on Chrome/Safari */
                color-adjust: exact;               /* Ensures background prints on Firefox */
            }
        }
    </style>
</head>
<body>
    <h1>Sessions</h1>
    <table>
        <thead>
            <tr>
"""
    # Dynamically generate the table headers
    for col in headers:
            html_content += f"                <th>{get_printable_title(col)}</th>\n"
    
    html_content += """            </tr>
        </thead>
        <tbody>
"""
    
    # Dynamically generate the table rows and cells
    for row in talks:
        if row['Start (date)']: 
            html_content += "            <tr>\n"
            for col in headers:
                    c = row[col]
                    if type(c) == type({}):
                        c = c['en']
                    html_content += f"                <td>{c}</td>\n"
            html_content += "            </tr>\n"

    html_content += """        </tbody>
    </table>
</body>
</html>
"""
    return html_content

def write_html(output_html, html_content):
    # Write the completed string out to the HTML file
    with open(output_html, mode='w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully created {output_html}")

def verify_json(headers):
    required_headers = [
        'Start (date)',
        'Start (time)',
        'End (time)',
        'Proposal title',
    ]
    for h in required_headers:
        if not h in headers:
            return False
    return True

parser = argparse.ArgumentParser(
                    prog='CalendarExporter',
                    description='A quick script to convert preltax json to html')
parser.add_argument('json_file')


args = parser.parse_args()
json_file = args.json_file
html_file = json_file[:-len('.json')] + '.html'

with open(json_file, mode='r', encoding='utf-8') as f:
    talks = json.load(f)

headers = talks[0].keys()
# remove ID, always here in json, can't be removed from the export
headers = [x for x in headers if x != 'ID']

if not verify_json(headers):
    print("Incorrect export")
    sys.exit(1)

write_html(html_file, generate_html(headers, talks))
