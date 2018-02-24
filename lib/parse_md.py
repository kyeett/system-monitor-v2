from pprint import pprint
import os

print(os.getcwd())


def new_slide():
    return {
        'index': 0,
        'content': '',
    }


def new_section(name, title=''):
    return {
        'section': name,
        'slides': [new_slide()],
        'title': title
    }


def parse_markdown():

    with open(os.getcwd() + '/lib/EXAMPLE.md') as f:

        # Start with an empty section in case document doesn't start with a title
        ui_sections = []
        #new_section(name='empty', title='')]

        for line in f.readlines():

            # New section and new slide
            if "## " in line or "# " in line:

                if line.startswith('## ') or line.startswith('# '):
                    section_name = line.replace('## ', '').replace('# ', '').replace('\n', '')

                    ui_sections.append(
                        new_section(name=section_name, title=section_name.title()))

                elif line.startswith('### '):
                    pass

            ui_sections[-1]['slides'][-1]['content'] += line

            print('s:%s i:%i - %s' % (ui_sections[-1]['section'], len(ui_sections[-1]['slides']), line))
    pprint(ui_sections)
    return ui_sections


if __name__ == '__main__':
    parse_markdown()

