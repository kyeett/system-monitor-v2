import sys
import yaml
import requests
import importlib
from flask import Flask, redirect, render_template, request, json
import logging
from collections import Counter, OrderedDict
from flask_socketio import SocketIO, emit
from pprint import pprint

app = Flask(__name__)
app.config['SECRET'] = "mysecret!"
app.config['DEBUG'] = True
socketio = SocketIO(app)

VERSION = 0.2


@app.errorhandler(requests.RequestException)
def handle_invalid_usage(error):
    return error.message, 404


@app.route('/')
def home():
    is_master = bool(request.args.get('master', ''))
    print(is_master)
    return render_template('index.html', options=options, sections=ui_sections, is_master=is_master, version=VERSION)


# Add metadata to states that only has basic configuration
def add_metadata(state_info, section_counter):

    metadata = {}

    # Some metadata is defined
    if isinstance(state_info, dict):
        basename = state_info.keys()[0]
        default_text = basename.title().replace("_", " ")

        metadata['title'] = state_info.values()[0].get('title', '')
        metadata['content'] = state_info.values()[0].get('content', '<h1>' + default_text +'</h1>')

        # Use section if specified, otherwise basename
        section = state_info.values()[0].get('section', basename)

    else:
        basename = state_info
        default_text = basename.title().replace("_", " ")
        metadata['content'] = '<h1>' + default_text + '</h1>'
        section = basename
    print(metadata)
    metadata['index'] = section_counter[section]
    metadata['section'] = section
    section_counter[section] += 1
    return metadata


def read_configuration():

    with open('config.yaml', 'r') as f:
        configuration = yaml.load(f)

        options = configuration['options']

        section_counter = Counter()
        possible_states = [add_metadata(state, section_counter) for state in configuration['states']]

        ui_sections = []
        # Get unique sections
        for section in OrderedDict.fromkeys([state['section'] for state in possible_states]):

            # Get slides in section
            ui_sections.append({
                'section': section,
                'title': section.title(),
                'slides': [slide_metadata for slide_metadata in possible_states if slide_metadata['section'] == section]
            })

        pprint(ui_sections)
        # Verify mandatory fields exist in options
        if 'stateGetter' not in options:
            raise KeyError(""" Mandatory option 'stateGetter' missing in 'config.yaml'.

Example:

options:
  stateGetter: plugins.builtin_stategetters.RandomStateGetter
""")

        return possible_states, ui_sections, options


def load_getter_class(options):
    state_getter_class = options['stateGetter']
    mod_name, class_name = state_getter_class.rsplit('.', 1)
    mod = importlib.import_module(mod_name)
    getter_class = getattr(mod, class_name)
    return getter_class


@socketio.on('message')
def handle_message(msg):
    print(msg)

@socketio.on('position master')
def handle_position(msg):
    print(msg)
    emit('position broadcast', msg, broadcast=True)


if __name__ == '__main__':

    # Read configuration from file
    try:
        possible_states, ui_sections, options = read_configuration()
    except KeyError as e:
        logging.error(e)
        sys.exit(1)

    import lib.parse_md as parse_md
    ui_sections = parse_md.parse_markdown()

    # Nest possible_states
    socketio.run(app)
