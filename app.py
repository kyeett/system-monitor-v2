import sys
import yaml
import requests
import importlib
from flask import Flask, redirect, render_template, request, json
import logging
from collections import Counter, OrderedDict

app = Flask(__name__)
VERSION = 0.3


@app.errorhandler(NotImplementedError)
def handle_not_implemented(error):
    return "The StateGetter plugin used has not implemented get_state() method", 500


@app.errorhandler(requests.RequestException)
def handle_invalid_usage(error):
    return error.message, 404


@app.route('/state')
def state():

    current_state = state_getter.get_state()

    response = json.dumps(current_state, sort_keys=True, indent=4, separators=(',', ': '))

    # Check if ?refresh is specified for demo, used for demo purposes
    if 'refresh' in request.args:
        response = '<meta http-equiv="refresh" content="0.5">' + response.replace('\n', '<br>').replace(" ", "&nbsp;")

    return response


@app.route('/')
def home():
    return redirect("/ui", code=302)


@app.route('/ui')
def ui():
    return render_template('index.html', options=options, sections=ui_sections, version=VERSION)


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


if __name__ == '__main__':

    # Read configuration from file
    try:
        possible_states, ui_sections, options = read_configuration()
    except KeyError as e:
        logging.error(e)
        sys.exit(1)

    # Nest possible_states
    app.run(debug=True)
