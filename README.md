Quick script to generate a printable table for pretalk

How to use it
=============

Go to the admin interface of the pretalx instance. Select your event, and go to the
menu on the left side, in "Schedule", "Export".

On the first tab (CSV/JSON exports), select:
* "Json export" as export format
* "Confirmed" as Target group"
* Check the following
- Proposal title
- Speakers names
- Start (date)
- Start (time)
- End (time)

You can also select "Tracks" or "Session type".

Then you can hit "Save" and get a json file.

On the command line, create a directory where the script will write the html file (let's call it directory-where-output-will-be-generated)

Run `python html-export.py path-to-the-json-file directory-where-output-will-be-generated`

And voila, you can print
