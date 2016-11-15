import os

from flask import abort, render_template, url_for, send_file, request
from flask_login import login_required

from shutterpy import app, resolve_path, get_thumbnail, get_mimetype


@app.route('/view/<path:path>')
@login_required
def view(path):
    if request.args.get('thumbnail'):
        abs_path = get_thumbnail(path).filename
    else:
        abs_path = resolve_path(path)
    return send_file(abs_path, mimetype=get_mimetype(path))


@app.route('/browse', defaults={'path': ''})
@app.route('/browse/<path:path>')
@login_required
def browse(path):
    full_path = resolve_path(path)
    if not os.path.isdir(full_path):
        abort(404)

    album_paths = {}
    thumbnail_paths = {}

    for file in os.listdir(full_path):
        rel_path = os.path.join(path, file)
        abs_path = resolve_path(rel_path)
        _, ext = os.path.splitext(file)

        if os.path.isdir(abs_path) and not file.startswith('.'):
            album_paths[url_for('browse', path=rel_path)] = file
            continue

        if ext.lstrip('.').lower() not in ('jpg', 'bmp', 'png'):
            continue

        file_path = os.path.join(full_path, file)
        thumbnail_paths[url_for('view', path=rel_path)] = file

    return render_template(
        'album.html',
        thumbnail_paths=thumbnail_paths,
        album_paths=album_paths,
    )
