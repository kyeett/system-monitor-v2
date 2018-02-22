import sys
import yaml
import requests
import importlib
from flask import Flask, redirect, render_template, request, json
import logging
from collections import Counter, OrderedDict
from flask_socketio import SocketIO, emit

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
def add_metadata(state_info, group_counter):

    metadata = {}

    # Some metadata is defined
    if isinstance(state_info, dict):
        basename = state_info.keys()[0]
        default_text = basename.title().replace("_", " ")

        metadata['basename'] = basename
        metadata['title'] = state_info.values()[0].get('title', default_text)
        metadata['text'] = state_info.values()[0].get('text', default_text)

        # Use group if specified, otherwise basename
        group = state_info.values()[0].get('group', basename)

    else:
        basename = state_info
        default_text = basename.title().replace("_", " ")
        metadata['basename'] = basename
        metadata['title'] = default_text
        metadata['text'] = default_text
        group = basename

    metadata['index'] = group_counter[group]
    metadata['group'] = group
    group_counter[group] += 1
    return metadata


def read_configuration():

    with open('config.yaml', 'r') as f:
        configuration = yaml.load(f)

        options = configuration['options']

        group_counter = Counter()
        possible_states = [add_metadata(state, group_counter) for state in configuration['states']]

        ui_sections = []
        # Get unique groups
        for group in OrderedDict.fromkeys([state['group'] for state in possible_states]):

            # Get slides in section
            ui_sections.append({
                'group': group,
                'title': group.title(),
                'slides': [slide_metadata for slide_metadata in possible_states if slide_metadata['group'] == group]
            })

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

    # Nest possible_states
    socketio.run(app)
