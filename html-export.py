import json
import sys
import argparse
import os.path


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
        'Room'
    ]
    for h in required_headers:
        if not h in headers:
            return False
    return True


def get_room_list(talks):
    return {x['Room']['en'] for x in talks if 'Room' in x and x['Room']}


def get_day_list(talks):
    return {x['Start (date)'] for x in talks if x['Start (date)']}


def filter_talks(talks, room, day):
    result = []
    for t in talks:
        if t['Room'] and t['Room']['en'] == room:
            if t['Start (date)'] == day:
                result.append(t)
    return result


def sorted_by_time(talks):
    return sorted(talks, key=lambda talk: talk['Start (time)'])


parser = argparse.ArgumentParser(
    prog='CalendarExporter',
    description='A quick script to convert preltax json to html')
parser.add_argument('json_file')
parser.add_argument('destination_folder')

args = parser.parse_args()
json_file = args.json_file


with open(json_file, mode='r', encoding='utf-8') as f:
    talks = json.load(f)

headers = talks[0].keys()
# remove ID, always here in json, can't be removed from the export
headers = [x for x in headers if x != 'ID']

if not verify_json(headers):
    print("Incorrect export")
    sys.exit(1)

room_list = get_room_list(talks)
day_list = get_day_list(talks)

for room in room_list:
    for day in day_list:
        filtered_talks = sorted_by_time(filter_talks(talks, room, day))

        output_file = args.destination_folder

        prefix = os.path.basename(json_file[:-len('.json')])
        output_file = f'{args.destination_folder}/{prefix}-{day}-{room}.html'

        h = headers[:]

        # remove the column we do not want to show
        h.remove("Room")
        h.remove("Start (date)")

        # merge the speaker name in the session title
        for t in filtered_talks:
            speakers = ', '.join(t['Speaker names'])
            t['Proposal title'] += ' -- ' + speakers
        h.remove('Speaker names')

        # reorder the columns
        h.remove('Start (time)')
        h.remove('End (time)')
        h2 = ['Start (time)', 'End (time)']
        h2.extend(h)

        write_html(output_file, generate_html(h2, filtered_talks))
