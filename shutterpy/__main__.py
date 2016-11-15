import click
import os
import sys

os.environ['FLASK_APP'] = __file__

if __package__ is None:
    sys.path.insert(0, '')
    import shutterpy
    __package__ = 'shutterpy'

from . import app


@app.cli.command()
@click.option('--debug', is_flag=True)
@click.option('--port', default=5000)
@click.option('--host', default='127.0.0.1')
@click.argument('album_root')
def run(debug, port, host, album_root):
    app.config['SHUTTERPY_ROOT'] = os.path.abspath(album_root)
    print("Serving pictures from %s" % app.config['SHUTTERPY_ROOT'])
    import shutterpy.views
    app.run(debug=debug, port=port, host=host)


if __name__ == '__main__':
    run()
