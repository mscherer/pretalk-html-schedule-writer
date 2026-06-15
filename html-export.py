import json
import sys

def json_to_html(input_json, output_html):
    with open(input_json, mode='r', encoding='utf-8') as f:
        talks = json.load(f)

    headers = talks[0].keys()
    headers = [x for x in headers if x != 'ID']
    write_html(output_html, generate_html(headers, talks))

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
            html_content += f"                <th>{col}</th>\n"
    
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

#parser = argparse.ArgumentParser(
#                    prog='CalendarExporter',
#                    description='A quick script to export preltax to html')

json_file = sys.argv[1]
html_file = json_file[:-len('.json')] + '.html'
json_to_html(json_file, html_file)
