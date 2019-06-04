import subprocess
import sys
from datetime import datetime

import click
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Box, Frame, TextArea


class CLI:
    def __init__(self, command, refresh_interval=2):
        self.setup_layout()
        self._command = command
        self._app = Application(layout=self._layout,
                                key_bindings=self.generate_keybindings(),
                                full_screen=False,
                                erase_when_done=True,
                                before_render=self.refresh,
                                min_redraw_interval=refresh_interval)

    def setup_layout(self):
        self._text_area = TextArea(
            text=f'Loading...\nPress control-c to quit.',
            read_only=True
        )
        self._frame = Frame(self._text_area)
        self._layout = Layout(container=self._frame)

    def generate_keybindings(self):
        kb = KeyBindings()
        kb.add('c-c')(self._exit_keybinding_listener)
        return kb

    def _exit_keybinding_listener(self, event):
        event.app.exit()

    def refresh(self, event):
        output = subprocess.check_output(self._command, shell=True,
                                         encoding=sys.stdout.encoding).strip()
        try:
            datum = int(output)
        except ValueError:
            raise ValueError('Command output needs to be a number')

        self._text_area.text = (f'Last run: {datetime.now()}\n\n'
                                f'{datum}\n\n'
                                f'Press control-c to quit.')

    def run(self):
        self._app.run()

@click.command()
def main():
    CLI(command='ls -l | wc -l').run()
