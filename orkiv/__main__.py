from kivy.app import App
from kivy.uix.boxlayout import AnchorLayout
from kivy.properties import ObjectProperty

from sleekxmpp import ClientXMPP
from kivy.uix.textinput import TextInput

from kivy.uix.modalview import ModalView
from kivy.uix.label import Label

from sleekxmpp.exceptions import XMPPError

class ConnectionModel(ModelView):
	def __init__(self,jabber_id,password):
		super(ConnectionModel,self).__init__(auto_dismiss=False,anchor_y='bottom')
		self.label=Label(text = 'Connecting to %s...' % jabber_id)
		self.add_widget(self.label)
		self.jabber_id = jabber_id
		self.password = password

class AccountDetailsForm(AnchorLayout):
	server_box = ObjectProperty()
	username_box = ObjectProperty()
	password_box = ObjectProperty()

	def login(self):
		jabber_id = self.username_box.text + '@' + self.server_box.text
		model = ConnectionModel(jabber_id,self.password_box.text)
		model.open()

		password = self.password_box.text
		app = Orkiv.get_running_app()
		app.connect_to_jabber(jabber_id,password)
		print app.xmpp.client_roster.keys()
		app.xmpp.disconnect()
class AccountDetailsTextInput(TextInput):
	next=ObjectProperty()
	def _keyboard_on_key_down(self,window,keycode,text,modifiers):
		if keycode[0] == 9:
			self.next.focus = True
		elif keycode[0] == 13:
			self.parent.parent.login()
		else:
			super(AccountDetailsTextInput,self)._keyboard_on_key_down(window,keycode,text,modifiers)

class Orkiv(App):
	def connect_to_jabber(self,jabber_id,password):
		self.xmpp = ClientXMPP(jabber_id,password)
		self.xmpp.reconnect_max_attempt = 1
		connected=self.xmpp.connect()
		if not connected:
			raise XMPPError('unable to connect')

		self.xmpp.process()
		self.xmpp.send_presence()
		self.xmpp.get_roster()


Orkiv().run()

