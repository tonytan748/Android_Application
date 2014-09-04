from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NemericProperty,ReferenceListProperty,ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

class PongPaddle(Widget):
	score=NumericPropety(0)

	def bounce_ball(self,ball):
		if self.collide_widget(ball):
			vx,vy=ball.velocity
			offset = (ball.center_y - self.center_y) / (self.height / 2)
			bounced = Vector(-1 * vx,vy)
			vel = bounced * 1.1
			ball.velocity = vel.x,vel.y + offset

class PongBall(Widget):
	velocity_x=NumericPropety(0)
	velocity_y=NumericPropety(0)
	velocity=ReferenceListProperty(velocity_x,velocity_y)

	def move(self):
		self.pos=Vector(*self.velocity) + self.pos

class PongGame(Widget):
	ball = ObjectProperty(None)
	player1=ObjectProperty(None)

	def serve_ball(self,vel=(4,0)):
		self.ball.center=self.center
		self.ball.velocity=vel

	def update(self,dt):
		self.ball.move()
		self.player1.bounce_ball(self.ball)

		if (self.ball.y<self.y) or (self.ball.top > self.top):
			self.ball.velocity_y *= -1

		if self.ball.x < 0:
			self.ball.velocity_y *= -1
		if self.ball.x > self.width:
			self.player1.score += 1
			self.serve_ball(vel=(-4,0))

	def on_touch_move(self,touch):
		if touch.x < self.width / 3:
			self.player1.center_y = touch.y

class PongApp(App):
	def build(self):
		game = PongGame()
		game.serve_ball()
		Clock.schedule_interval(game.update,1.0/60.0)
		return game

if __name__=="__main__":
	PongApp().run()

