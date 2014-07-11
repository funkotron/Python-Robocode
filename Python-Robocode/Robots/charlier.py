#! /usr/bin/python
#-*- coding: utf-8 -*-

from robot import Robot #Import a base Robot
import math


class Charlier(Robot): #Create a Robot
    
    def init(self):    #To initialyse your robot
        
        
        #Set the bot color in RGB
        self.setColor(0, 200, 100)
        self.setGunColor(200, 200, 0)
        self.setRadarColor(255, 60, 0)
        self.setBulletsColor(255, 150, 150)

        self.radarVisible(True) # if True the radar field is visible
        
        #get the map size
        size = self.getMapSize()
        
        self.lockRadar("gun")
        
    
    def run(self): #main loop to command the bot
        
        #self.move(90) # for moving (negative values go back)
        #self.stop()
        self.gunTurn(90)
        self.stop()


    def onHitWall(self):
        self.reset() #To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event) 
        self.pause(100)
        self.move(-100)
        self.rPrint('ouch! a wall !')

    def sensors(self): #NECESARY FOR THE GAME
        pass
        
    def onRobotHit(self, robotId, robotName): # when My bot hit another
        self.rPrint('collision with:' + str(robotId))
        
    def onHitByRobot(self, robotId, robotName):
        self.rPrint("damn a bot collided me!")

    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower): #NECESARY FOR THE GAME
        """ When i'm hit by a bullet"""
        self.rPrint ("hit by " + str(bulletBotId) + "with power:" +str( bulletPower))
        
    def onBulletHit(self, botId, bulletId):#NECESARY FOR THE GAME
        """when my bullet hit a bot"""
        self.rPrint ("fire done on " +str( botId))
        
    def onBulletMiss(self, bulletId):#NECESARY FOR THE GAME
        """when my bullet hit a wall"""
        self.rPrint ("the bullet "+ str(bulletId) + " fail")
        
    def onRobotDeath(self):#NECESARY FOR THE GAME
        """When my bot die"""
        self.rPrint ("damn I'm Dead")

    def get_trajectory(self, botPos):

        pos = self.getPosition() #return the center of the bot
        x = pos.x() #get the x coordinate
        y = pos.y() #get the y coordinate

        dx = botPos.x() - x
        dy = botPos.y() - y
        dist = math.sqrt(dx**2 + dy**2)

        # angle = self.getGunHeading() #Returns the direction that the robot's gun is facing
        heading = self.getHeading() #Returns the direction that the robot is facing
        if dy == 0:
            dangle = 180 if dx > 0 else 0
        else:
            dangle = 180 - heading - math.degrees(math.atan(dy/dy))
        # angle = self.getRadarHeading() #Returns the direction that the robot's radar is facing
        # list = self.getEnemiesLeft() #return a list of the enemies alive in the battle
        return int(dist), int(dangle)

    def onTargetSpotted(self, botId, botName, botPos):#NECESARY FOR THE GAME
        "when the bot see another one"
        self.setRadarField("thin")
        self.rPrint("I see the bot:" + str(botId) + "on position: x:" + str(botPos.x()) + " , y:" + str(botPos.y()))
        dist, dangle = self.get_trajectory(botPos)
        self.move(dist)
        self.turn(dangle)
        self.stop()
        self.fire(5)
