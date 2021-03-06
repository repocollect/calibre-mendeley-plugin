#!/usr/bin/env python

# "THE CHOCOLATE-WARE LICENSE" (Revision 1):
# <carles@pina.cat> wrote this file. As long as you retain
# this notice you can do whatever you want with this stuff. If we meet some
# day, and you think this stuff is worth it, you can buy me a chocolate in
# return. - Carles Pina Estany
# (license based in Beer-ware, see
#           https://fedoraproject.org/wiki/Licensing/Beerware )


from __future__ import (division, absolute_import, print_function)

__license__   = 'Chocolate-ware r1'
__copyright__ = '2012, 2013, Carles Pina Estany'

from PyQt4.Qt import (Qt, QWidget, QDialog, QVBoxLayout, QCheckBox, QPushButton, QLineEdit, QLabel, QFormLayout, QDialogButtonBox, QSizePolicy, QLayout)

from calibre.gui2 import dynamic, info_dialog
from calibre.utils.config import JSONConfig

plugin_prefs = JSONConfig('plugins/Mendeley')

class OapiConfig:
    def __init__(self):

        # Consumey Key
        setattr(self,'api_key', 'c168ce62964a4900e66d9361bda9cb3a04cf98732')

        #Consumey Secret
        setattr(self,'api_secret', '7d4294168e43807651faf051510c707b')
        #See
        # http://stackoverflow.com/questions/5681223/oauth-security-against-sharing-consumer-key-secret-and-list-of-access-tokens
        # to see why the consumer secret is here :-( (OAuth 1 is the problem).
        # Please, create your one consumer secret if you want Mendeley OAPI
        # access (just go to http://dev.mendeley.com and you can generate your
        # one. Easy! Thanks!!).

        setattr(self,'host', 'api.mendeley.com')

class ConfigWidget(QDialog):
    def __init__(self, plugin_action):
        from calibre_plugins.mendeley_to_calibre.mendeley_oapi import fetch
        from calibre_plugins.mendeley_to_calibre.mendeley_oapi import mendeley_client

        self.information_label = None

        QWidget.__init__(self)
        self.plugin_action = plugin_action

        self.layout = QFormLayout()
        self.label = QLabel()
        self.label.setOpenExternalLinks(True)

        oapiConfig = OapiConfig()
        tokens_store = mendeley_client.MendeleyTokensStore()
        # tokens_store.loads(plugin_prefs['account'])

        self.oapi = fetch.calibreMendeleyOapi(oapiConfig, tokens_store)
        self.oapi.isValid()
        url = self.oapi.getVerificationUrl()
        link = '<a href="%s">Press Here</a>' % (url)

        self.label.setText("""<ol>
<li>%s</li>
<li>Authenticate and authorize the applicatoin</li>
<li>Copy-paste the Verification Token</li>
<li>Press 'Ok'</li>
</ol>
""" % (link))

        self.setLayout(self.layout)

        self.api_key = QLineEdit(self)

        self.layout.addRow(self.label)
        self.layout.addRow('Verification Code',self.api_key)

        self.api_key.textChanged.connect(self.clean_information)

        self.api_key.setText(plugin_prefs.get('api_key',''))

        self.setWindowTitle('Customise Mendeley Plugin Importer')

        self.layout.setSizeConstraint(QLayout.SetFixedSize)

    def add_ok_cancel_buttons(self):
        """ This QDialog is shown by Calibre -then it adds the Ok/Cancel
            buttons- but also by the plugin itself.
        """
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout.addRow(button_box)

        button_box.accepted.connect(self.ok_pressed)
        button_box.rejected.connect(self.reject)

    def ok_pressed(self):
        if self.save_settings():
            self.accept()
        else:
            if self.information_label == None:
                self.information_label = QLabel()
                self.layout.addRow(self.information_label)

            self.information_label.setText('<font color="red">Invalid verification code</font>')

    def clean_information(self):
        if self.information_label:
            self.information_label.setText('')

    def save_settings(self):
        ok_api_key = True
        from calibre_plugins.mendeley_to_calibre.mendeley_oapi import mendeley_client
        plugin_prefs['verification'] = str(self.api_key.text())
        try:
            self.oapi.setVerificationCode(str(self.api_key.text()))
        except ValueError:
            ok_api_key = False

        if ok_api_key:
            tokens_store = mendeley_client.MendeleyTokensStore()
            tokens_store.add_account('test_account',self.oapi.mendeley.get_access_token())
            plugin_prefs['account'] = tokens_store.dumps()

        return ok_api_key
