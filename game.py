
from Tkinter import *

import random
import time
import string

#from playsound import playsound


class ModelCenter:
    def __init__(self,canvas):
        #all objects to draw
        self.to_draw = []

        #Other attribute
        #self.yolo = 11

        
        #Alive
        self.game_over = False
        self.active_ball = 0
        self.score = 0

        #canvas
        self.canvas = canvas
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

        #bricks
        self.bricks = []
        num_col = 20
        num_row = 5
        self.num_B = num_col*num_row
        
        
        #Init Bricks
        func = ["bullet","ball_size", "none", "none", "none", "none", "none", "none", "clone", "long", "none","none", "none","none",'none' "none","none","clone","none","none","magic"]#,"long","clone"]
        for j in range(num_row):
            for i in range(num_col):
                a = Brick([5+25*i,10+j*15,25+25*i,20+15*j,'white',random.choice(func)],self)
                self.bricks.append(a)
                self.to_draw.append(a)

        #ball
        #attribute = [x, y, vx,vy, size, color, alive]
        self.balls = []
        num_of_balls = 1
        for i in range(num_of_balls):
            b = Ball([200+random.randint(1,2), 300+random.randint(10,20), (random.random()+1), (random.random()-3),10,'white', True],self)
            self.balls.append(b)
            self.to_draw.append(b)
            self.active_ball += 1


        #paddle
        self.paddle = Paddle([250,570,400,585,'white','none'],self)
        self.to_draw.append(self.paddle)

        #bullet
        self.bullets = []
        #self.bullet = Bullet([self.paddle.att[0],self.paddle.att[1],self.paddle.att[2],self.paddle.att[3],10,'yellow'],self)

    ##############BULLET FUNCTION#####################
    def create_bullet(self,bullet):
        bullet_id = self.canvas.create_oval(bullet.att[0],
                                            bullet.att[1],
                                            bullet.att[0]+2*bullet.att[4],
                                            bullet.att[1]+2*bullet.att[4],
                                            fill=bullet.att[5])
        return bullet_id

    def shoot_bullet(self,bullet):
        self.canvas.move(bullet.id,bullet.att[2],bullet.att[3])
        bullet.att[0] = bullet.att[0]+bullet.att[2]
        bullet.att[1] = bullet.att[1]+bullet.att[3]


    ##############BALL FUNCTION#######################
    def create_ball(self,ball):
        ball_id = self.canvas.create_oval(ball.att[0],
                                          ball.att[1],
                                          ball.att[0]+2*ball.att[4],
                                          ball.att[1]+2*ball.att[4],
                                          fill=ball.att[5])
        return ball_id

    def move_ball_by(self,ball,direction):
        self.canvas.move(ball.id, direction[0],direction[1])
        ball.att[0] = ball.att[0] + direction[0]
        ball.att[1] = ball.att[1] + direction[1]
        return


    def move_ball(self,ball):
        '''
        move the ball to next position
        call move on canvas: canvas.move()
        '''
        self.canvas.move(ball.id,ball.att[2],ball.att[3])
        ball.att[0] = ball.att[0]+ball.att[2]
        ball.att[1] = ball.att[1]+ball.att[3]

        pos = [ball.att[0],ball.att[1]]

        #hit wall
        if pos[1] <=0:
            self.move_ball_by(ball, [0, -1*pos[1]])
            ball.att[3] = ball.att[3]*-1

        if pos[0] <=0:
            self.move_ball_by(ball, [-1*pos[0],0])
            ball.att[2] = ball.att[2]*-1

        if pos[0]+2*ball.att[4] >= self.canvas_width:
            self.move_ball_by(ball, [self.canvas_width-pos[0]-2*ball.att[4], 0])
            ball.att[2] = ball.att[2]*-1

        if pos[1]+2*ball.att[4] >= self.canvas_height:
            if ball.att[6] ==True:
                ball.att[6] = False
                self.to_draw.remove(ball)
                self.balls.remove(ball)
                self.canvas.delete(ball.id)
                
                self.active_ball = self.active_ball - 1

                print "Balls Left: ", self.active_ball
                
                if self.active_ball == 0:
                    self.game_over = True
        #brick
            '''
        if self.hit_brick(pos) == True:
            self.y = self.y*-1

        #bottom
        if pos[3] >= self.canvas_height:
            if (not self.hit_bottom): self.paddle.hp -= 1
            self.hit_bottom = True
            '''



    ################PADDLE FUNCTION#########################
    def create_paddle(self,paddle):
        paddle_id = self.canvas.create_rectangle(paddle.att[0], paddle.att[1], paddle.att[2], paddle.att[3], fill=paddle.att[4])
        return paddle_id

    def bind_all(self,key,function):
        self.canvas.bind_all(key,function)
        return

    def move_paddle(self,paddle):
        pos = paddle.att[0:4]
        if pos[0] <= 0:
            paddle.x= 4
        elif pos[2] >= self.canvas_width:
            paddle.x= -4
        self.canvas.move(paddle.id,paddle.x,0)
        return

    ################BRICK FUNCTION#################################
    def create_brick(self,brick):
        brick_id = self.canvas.create_rectangle(brick.att[0], brick.att[1], brick.att[2], brick.att[3], fill=brick.att[4])
        return brick_id


    ##############INTERACTION FUNCTION#############################
    def ball_paddle(self,ball,paddle):
        ball.att[3] = ball.att[3]*-1 - 0.35
        x_correction = (ball.att[0]-0.5*(paddle.att[0]+paddle.att[2]))*0.05
        ball.att[2] = ball.att[2]+x_correction
        return

    def ball_brick(self,ball,brick):
        if brick.reaction() == "delete_me":
            self.canvas.delete(brick.id)
            self.to_draw.remove(brick)
            self.bricks.remove(brick)
            
            self.num_B = self.num_B-1

            print "Bricks left: ", self.num_B
            
        if self.num_B == 0:
            self.canvas.delete("all")
            self.game_over = True
            print ""
            print "######################"
            print "#                    #"
            print "# You beat the game! #"
            print "#                    #"
            print "######################"
            print ""
            print ""
            print "###########################"
            print "#                         #"
            print "# How did you do that???? #"
            print "#                         #"
            print "###########################"
            print ""
            playsound('file:///Users/xujiang/Desktop/GG.mp3')
            
            
        
        cx  = ball.att[0]+ball.att[4]
        cy = ball.att[1] +ball.att[4]
        bcx = 0.5*(brick.att[0]+brick.att[2])
        bcy = 0.5*(brick.att[1]+brick.att[3])
        if (cx > brick.att[0] and cx < brick.att[2]):
            ball.att[3] = ball.att[3]*-1

            if cy-bcy == 0:
                y_correction = (0.5*(brick.att[3]-brick.att[1])+ball.att[4]-(cy - bcy))*abs(cy-bcy)/(cy-bcy+0.0001)
            
            y_correction = (0.5*(brick.att[3]-brick.att[1])+ball.att[4]-(cy - bcy))*abs(cy-bcy)/(cy-bcy+0.0001)
            self.move_ball_by(ball,[0,y_correction])
        elif (cy > brick.att[1] and cy < brick.att[3]):

            if cx-bcx == 0:
                x_correction = (0.5*(brick.att[2]-brick.att[0])+ball.att[4]-(cx - bcx))*abs(cx-bcx)/(cx-bcx+0.0001)
            
            x_correction = (0.5*(brick.att[2]-brick.att[0])+ball.att[4]-(cx - bcx))*abs(cx-bcx)/(cx-bcx+0.0001)
            self.move_ball_by(ball,[x_correction,0])
            ball.att[2] = ball.att[2]*-1
        else:
            y_correction = (0.5*(brick.att[3]-brick.att[1])+ball.att[4]-(cy - bcy))*abs(cy-bcy)/(cy-bcy+0.0001)
            x_correction = (0.5*(brick.att[2]-brick.att[0])+ball.att[4]-(cx - bcx))*abs(cx-bcx)/(cx-bcx+0.0001)
            self.move_ball_by(ball,[x_correction,y_correction])
            ball.att[2] = ball.att[2]*-1
            ball.att[3] = ball.att[3]*-1
        brick.effect(ball)
        return

    def ball_ball(self,ball,ball2):
        cx1 = ball.att[0]+ball.att[4]
        cy1 = ball.att[1]+ball.att[4]
        cx2 = ball2.att[0] + ball2.att[4]
        cy2 = ball2.att[1] + ball2.att[4]
        r1  = ball.att[4]
        r2 = ball2.att[4]
        dis = ((cx2-cx1)**2 + (cy2-cy1)**2)**0.5
        r_correction = r1 + r2 - dis
        x_correction = (cx2-cx1)*r_correction/dis
        y_correction = (cy2-cy1)*r_correction/dis
        self.move_ball_by(ball2,[x_correction,y_correction])
        #change velocity
        tempvx = ball.att[2]
        tempvy = ball.att[3]
        ball.att[2] = ball2.att[2]
        ball.att[3] = ball2.att[3]
        ball2.att[2] = tempvx
        ball2.att[3] = tempvy
        return

    def bullet_brick(self,bullet,brick):
        if brick.reaction() == "delete_me":
            self.canvas.delete(brick.id)
            self.to_draw.remove(brick)
            self.bricks.remove(brick)
            
            self.num_B = self.num_B-1
            print "Bricks left: ", self.num_B
            
        if self.num_B == 0:
            self.game_over = True
            print ""
            print "######################"
            print "#                    #"
            print "# You beat the game! #"
            print "#                    #"
            print "######################"
            print ""
            playsound('file:///Users/xujiang/Desktop/GG.mp3')
            
        self.to_draw.remove(bullet)
        self.bullets.remove(bullet)
        self.canvas.delete(bullet.id)
        bullet.att[6] = False
        return


    ##############Collision Check###################################
    def check_collision(self):
        for ball in self.balls:
            #balls hit paddle
            if (ball.att[1]+2*ball.att[4]>= self.paddle.att[1]) and (ball.att[0]+2*ball.att[4]>=self.paddle.att[0]) and (ball.att[0]<= self.paddle.att[2]):
                self.ball_paddle(ball,self.paddle)

            #balls hit balls
            for ball2 in self.balls:
                if ball != ball2:
                    cx1 = ball.att[0]+ball.att[4]
                    cy1 = ball.att[1]+ball.att[4]
                    cx2 = ball2.att[0] + ball2.att[4]
                    cy2 = ball2.att[1] + ball2.att[4]
                    r1  = ball.att[4]
                    r2 = ball2.att[4]
                    if ((cx2-cx1)**2 + (cy2-cy1)**2 <= (r1+r2)**2):
                        #print (cx2-cx1)**2 + (cy2-cy1)**2
                        self.ball_ball(ball,ball2)

            #balls hit bricks
            for brick in self.bricks:
                cx = ball.att[0] + ball.att[4]
                cy = ball.att[1] + ball.att[4]
                r = ball.att[4]
                if ( (cx + r > brick.att[0]) and (cx - r < brick.att[2]) and (cy + r > brick.att[1]) and (cy - r < brick.att[3])):
                    if ball.att[6]: self.ball_brick(ball,brick)

        ##bullets interaction with bricks            
        for bullet in self.bullets:
            for brick in self.bricks:
                cx = bullet.att[0] + bullet.att[4]
                cy = bullet.att[1] + bullet.att[4]
                r = bullet.att[4]
                if ((cx + r > brick.att[0]) and (cx - r < brick.att[2]) and (cy + r > brick.att[1]) and (cy - r < brick.att[3])):
                    if bullet.att[6]: self.bullet_brick(bullet,brick)

                    

    ###############Effect function######################################
    def clone_me(self,ball):
        self.score += 2
        b2 = ball.clone()
        b2.att[2] = b2.att[2]*-1
        self.move_ball_by(b2,[b2.att[4],b2.att[4]])
        self.balls.append(b2)
        self.to_draw.append(b2)
        self.active_ball += 1
        return
    
    def none(self, ball):
        self.score += 1
    
    def size_ball(self,ball):
        self.score += 5
        x = ball.att[0]
        y = ball.att[1]
        vx = ball.att[2]
        vy = ball.att[3]
        size = 0.2*random.randint(30,100)
        color = ball.att[5]
        alive = ball.att[6]
        new_b = Ball([x,y,vx,vy,size,color,alive],ball.mc)
        if ball.att[6] == True:
            ball.att[6] = False
            self.to_draw.remove(ball)
            self.balls.remove(ball)
            self.canvas.delete(ball.id)

            self.to_draw.append(new_b)
            self.balls.append(new_b)
        return

    def long_paddle(self):
        x = self.paddle.att[0]
        y = self.paddle.att[1]
        x1 = self.paddle.att[2]
        y1 = self.paddle.att[3]
        color = self.paddle.att[4]
        func = self.paddle.att[5]
        newpaddle = Paddle([x,y,x1+random.randint(10,30),y1,color,func],self)
        self.to_draw.remove(self.paddle)
        self.canvas.delete(self.paddle.id)
        self.paddle = newpaddle
        self.to_draw.append(self.paddle)

    def fire_func(self):
        self.paddle.add_func("fire")
        return

    def magic(self,ball):
        self.score += 100
        x = ball.att[0]
        y = ball.att[1]
        vx = ball.att[2]
        vy = ball.att[3]
        size = 0.1
        color = ball.att[5]
        alive = ball.att[6]
        new_b = Ball([x,y,vx,vy,size,color,alive],ball.mc)
        if ball.att[6] == True:
            ball.att[6] = False
            self.to_draw.remove(ball)
            self.balls.remove(ball)
            self.canvas.delete(ball.id)

            self.to_draw.append(new_b)
            self.balls.append(new_b)
        return
    
    def fire_bullet(self):
        bullet = Bullet([0.5*(self.paddle.att[0]+self.paddle.att[2]),0.5*(self.paddle.att[1]+self.paddle.att[3]),0,-3,3,'yellow',True],self)
        self.score+= 10
        self.bullets.append(bullet)
        self.to_draw.append(bullet)
        return




class Controller:

    def __init__(self):
        self.view = View()
        self.tk = self.view.tk
        self.canvas = self.view.canvas
        self.mc = ModelCenter(self.view.get_canvas())


    def game_start(self):
        print ''
        print '#########################'
        print '#                       #'
        print '# Welcome to the Game ! #'
        print '#                       #'
        print '#########################'
        print ''
        print 'Blue brick = clone ball'
        print ''
        print 'Red brick = bullets (press space to fire)'
        print ''
        print 'Pink brick = LOL brick :D'
        print ''
        print 'Yellow brick = size of ball changes'
        print ''
        print 'White brick = nothing'
        print ''
        print 'Green brick = longer paddle'
        print ''

        name = raw_input('Please enter your name: ')
        
        
        
        while 1:
                if not (self.mc.game_over):
                    for draw_me in self.mc.to_draw:
                        draw_me.draw()
                    self.mc.check_collision()
                    self.tk.update_idletasks()
                    self.tk.update()
                    time.sleep(0.005)
                    
                else:
                    print ''
                    print name, ' Your score: ', self.mc.score
                    print ''
                    break
        print ''
        print ''
        print '################'
        print "#              #"
        print "# Game is over #"
        print "#              #"
        print "################"
        print ''
        print ''
        
        return



class View:
    def __init__(self):
        self.tk=Tk()
        self.tk.title("$$$$$$$$$$$$$$$$$$  Game  $$$$$$$$$$$$$$$$$$")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)

        self.canvas = Canvas(self.tk, width=505, height=600, bd=0, highlightthickness=0)
        self.canvas.config(background='black')
        self.canvas.pack()
        self.tk.update()
    def get_canvas(self):
        return self.canvas






#---------------------------------------
class Ball:
    def __init__(self,att,mc):
        #attribute = [x, y, vx,vy, size, color, alive]
        # position x  : att[0]
        # position y  : att[1]
        # velocity vx : att[2]
        # velocity vy : att[3]
        # size:         att[4]
        # color:        att[5]
        # alive:        att[6]
        self.mc = mc
        self.att = att

        #create the ball figure on the canvas
        self.id = mc.create_ball(self)

    def move(self):
        return

    def draw(self):
        self.move()
        self.mc.move_ball(self)

    def clone(self):
        x = self.att[0]
        y = self.att[1]
        vx = self.att[2]
        vy = self.att[3]
        size = self.att[4]
        color = self.att[5]
        alive = self.att[6]
        b = Ball([x,y,vx,vy,size,color,alive],self.mc)
        return b

class Bullet:
    def __init__(self,att,mc):
        #attribute = [x, y, vx,vy, size, color, alive]
        # position x  : att[0]
        # position y  : att[1]
        # velocity vx : att[2]
        # velocity vy : att[3]
        # size:         att[4]
        # color:        att[5]
        # alive:        att[6]
        self.mc = mc
        self.att = att
        self.id = mc.create_bullet(self)
        
        return

    def shoot(self):
        return

    def draw(self):
        self.shoot()
        self.mc.shoot_bullet(self)
        return
    
    

class Brick:
    def __init__(self,att,mc):
        #att =  [x0,y0,x1,y1,color,effect]
        '''
        position x : att[0]
        position y : att[1]
        position x1 : att[2]
        position x2 :  att[3]
        color: att[4]
        effect : att[5]
        '''
        self.mc = mc
        self.att = att
        if self.att[5] == "clone":
            self.att[4] = "blue"
        elif self.att[5] == "long":
            self.att[4] = "green"
        elif self.att[5] == "ball_size":
            self.att[4] = "yellow"
        elif self.att[5] == "bullet":
            self.att[4] = "red"
        elif self.att[5] == "none":
            self.att[4] = "white"
        elif self.att[5] == "magic":
            self.att[4] = "pink"
        #create the brick on the canvas
        self.id = mc.create_brick(self)
        
    def draw(self):
        return

    def effect(self,ball):
        if self.att[5] == "clone":
            self.mc.clone_me(ball)
            print "A new ball is cloned"
            print ""
        if self.att[5] == "none":
            self.mc.none(ball)
            print "nothing happened"
            print ""
        if self.att[5] == "long":
            self.mc.long_paddle()
            print "Longer paddle"
            print ""
        if self.att[5] == "ball_size":
            self.mc.size_ball(ball)
            print "ball size is changed"
            print ""
        if self.att[5] == "magic":
            self.mc.magic(ball)
            print "LOL Looks like your ball disappeared"
            print ""
        if self.att[5] == 'bullet':
            self.mc.fire_func()
            print 'you fired bullets'
            print ""
        return

    def reaction(self):
        return "delete_me"

class Paddle:
    def __init__(self,att,mc):
        #att =  [x0,y0,x1,y1,color,func]
        '''
        position x : att[0]
        position y : att[1]
        position x1 : att[2]
        position x2 : att[3]
        color : att[4]
        func : att[5]
        '''
        self.mc = mc
        self.att =att

        #create a paddle on the canvas
        self.id = mc.create_paddle(self)

        #bind the paddle with keyboard
        self.mc.bind_all('<KeyPress-Left>', self.turn_left)
        self.mc.bind_all('<KeyPress-Right>', self.turn_right)
        #paddle velocity
        self.x = 0

        #ammo
        self.ammo = 0
        return

    def draw(self):
        self.mc.move_paddle(self)
        self.att[0] += self.x
        self.att[2] += self.x
        return

    def turn_left(self,evt):
        self.x = -8
        return

    def turn_right(self,evt):
        self.x = 8
        return

    def change_id(self, new_id):
        self.id = new_id
        return

    def change_att(self, new_att):
        self.att = new_att
        return

    
    def add_func(self,func):
        if func == "fire":
            self.att[5] = "fire"
            self.mc.bind_all('<KeyPress-space>', self.fire)
            self.ammo += 5
            print "your ammo now is: ", self.ammo
            return
            
    def fire(self,evt):
        if self.ammo>0:
            self.ammo = self.ammo-1
            self.mc.fire_bullet()
            print "your ammo now is: ", self.ammo
        return
    

class Effect:
    def __init__(self,eff, mc):
        self.controller = mc
        self.eff = eff
    def get_effect(self):
        return self.eff

c = Controller()
c.game_start()
