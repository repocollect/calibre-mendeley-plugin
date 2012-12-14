#!/usr/bin/env python

__license__   = 'GPL v3'
__copyright__ = '2012, Carles Pina'


from calibre.gui2.actions import InterfaceAction
from calibre_plugins.mendeley_to_calibre.main import MendeleyDialog

class Mendeley(InterfaceAction):
    name = 'Mendeley Plugin'

    action_spec = ('This is some text', None, 'This is some other text', ())

    def genesis(self):
        print 'Genesis is called'
	icon = get_icons('images/mendeley.png')
	self.qaction.setIcon(icon)
	self.qaction.triggered.connect(self.show_dialog)
	print 'End of genesis'

    def show_dialog(self):
        base_plugin_object = self.interface_action_base_plugin
	do_user_config = base_plugin_object.do_user_config
	d = MendeleyDialog(self.gui, self.qaction.icon(), do_user_config)
	d.show()
