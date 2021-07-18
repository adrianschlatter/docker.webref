# -*- coding: utf-8
"""
Web-Interface for JabRef library.

It lists the entries in a given JabRef library. It provides a simple
search bar to filter for those entries your looking for. Currently, it
provides read-only access to the library without any possibility to modify
existing entries or to add new ones.
"""

from flask import Flask, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import sqlalchemy as sa
from ppf.jabref import Entry, Field, split_by_unescaped_sep
from pathlib import Path

# Credential management
#
# This application is meant to run inside a docker container.
# Docker provides a mechanism to manage secrets. The user
# creates a container, adds a (named) secret, and runs the
# container.
# Inside the container, the named secret is available in the text file
# /run/secrets/<secret-name>.

sqlusername = open('/run/secrets/sqlusername').readline().strip()
sqlpassword = open('/run/secrets/sqlpassword').readline().strip()
sqlserver = open('/run/secrets/sqlserver').readline().strip()
sqldatabasename = open('/run/secrets/sqldatabasename').readline().strip()

app = Flask(__name__,
            static_url_path='',
            static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+pymysql://'
                                         f'{sqlusername}:{sqlpassword}'
                                         f'@{sqlserver}/{sqldatabasename}')
db = SQLAlchemy(app)


@app.route('/')
def root():
    """Show WebApp."""
    return app.send_static_file('index.html')


@app.route('/references/<path:path>')
def send_reference(path):
    """Send reference."""
    return send_from_directory('references', path)


@app.route('/loadEntries.php', methods=['POST'])
def loadEntries():
    """Return entries from library matching search expression."""
    searchexpr = request.form.get('searchexpr')

    patternmatchingQ = (sa.select(Field.entry_shared_id)
                        .where(Field.value.op('rlike')(searchexpr))
                        .distinct())
    entryQ = (sa.select(Entry)
              .where(Entry.shared_id.in_(patternmatchingQ)))

    entries = [{f: entry[0].fields.get(f, None)
               for f in ['author', 'title', 'year', 'file']}
               for entry in db.session.execute(entryQ)]

    basepath = Path('references')
    for entry in entries:
        if entry['file'] is not None:
            filepath = Path(split_by_unescaped_sep(entry['file'])[1])
            entry['file'] = basepath / filepath
            if not entry['file'].exists() or filepath.is_absolute():
                entry['file'] = None

    return render_template('entry_table.tmpl', entries=entries)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
