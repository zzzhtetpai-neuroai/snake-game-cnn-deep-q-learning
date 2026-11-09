import numpy as np
import pygame as pg

class Environment(object):
    
    def __init__(self,waitTime):
        self.width=880
        self.height=880
        self.nRows=10
        self.nColumns=10
        self.initSnakeLen=2
        self.defReward=-0.03
        self.negReward=-1
        self.posReward=2
        self.waitTime=waitTime
        if self.initSnakeLen>self.nRows/2:  #Make sure the snake is at least half(middle) (or less) the size of screen
            self.initSnakeLen=int(self.nRows/2)
        self.screen=pg.display.set_mode((self.width,self.height))
        self.snakePos=list()   #just a list to record position
        self.screenMap=np.zeros((self.nRows,self.nColumns))   #the main scoreboard with positions for snake,apple,etc
        for i in range(self.initSnakeLen):
            self.snakePos.append((int(self.nRows/2)+i,int(self.nColumns/2)))
            self.screenMap[int(self.nRows/2)+i][int(self.nColumns/2)]=0.5

        self.applePos=self.placeApple()
        self.drawScreen()
        self.collected=False
        self.lastMove=0
    
    def placeApple(self):
        posx=np.random.randint(0,self.nColumns)
        posy=np.random.randint(0,self.nRows)
        while self.screenMap[posy][posx]==0.5:   #if the snake hits the apple
            posx=np.random.randint(0,self.nColumns)
            posy=np.random.randint(0,self.nRows)
        self.screenMap[posy][posx]=1
        return (posy,posx)   #Makes sure it returns the row and column position for apple
    
    def drawScreen(self):
        self.screen.fill("#000000",)
        cellWidth=self.width/self.nColumns
        cellHeight=self.height/self.nRows
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if self.screenMap[i][j]==0.5:
                    pg.draw.rect(self.screen,"#FFFFFF",(int(j*cellWidth+1),int(i*cellHeight+1),int(cellWidth-2),int(cellHeight-2)))
                elif self.screenMap[i][j]==1:
                    pg.draw.rect(self.screen,"#EF0808F7",(int(j*cellWidth+1),int(i*cellHeight+1),int(cellWidth-2),int(cellHeight-2)))
        
        pg.display.flip()
    
    def moveSnake(self,nextPos,col):
        self.snakePos.insert(0,nextPos)

        if not col:
            self.snakePos.pop(len(self.snakePos)-1)
        self.screenMap=np.zeros((self.nRows,self.nColumns))
            
        for i in range(len(self.snakePos)):
            self.screenMap[self.snakePos[i][0]][self.snakePos[i][1]]=0.5
            
        if col:
            self.applePos=self.placeApple()
            self.collected=True 
        self.screenMap[self.applePos[0]][self.applePos[1]]=1

    def step(self,action):
        gameOver=False
        reward=self.defReward
        self.collected=False

        for event in pg.event.get():
            if event.type==pg.QUIT:
                return
        snakeX=(self.snakePos[0][1])
        snakeY=(self.snakePos[0][0])

        if action==0 and self.lastMove==1:
            action=1
        if action==1 and self.lastMove==0:
            action=0
        if action==2 and self.lastMove==3:
            action=3
        if action==3 and self.lastMove==2:
            action=2
        
        if action==0:
            if snakeY>0:
                if self.screenMap[snakeY-1][snakeX]==0.5:
                    gameOver=True
                    reward=self.negReward
                elif self.screenMap[snakeY-1][snakeX]==1:
                    reward=self.posReward
                    self.moveSnake((snakeY-1,snakeX),True)
                elif self.screenMap[snakeY-1][snakeX]==0:
                    self.moveSnake((snakeY-1,snakeX),False)
            else:
                gameOver=True
                reward=self.negReward
            
        elif action==1:
            if snakeY<self.nRows-1:
                if self.screenMap[snakeY+1][snakeX]==0.5:
                    gameOver=True
                    reward=self.negReward
                elif self.screenMap[snakeY+1][snakeX]==1:
                    reward=self.posReward
                    self.moveSnake((snakeY+1,snakeX),True)
                elif self.screenMap[snakeY+1][snakeX]==0:
                    self.moveSnake((snakeY+1,snakeX),False)
            else:
                gameOver=True
                reward=self.negReward
        
        elif action==2:
            if snakeX<self.nColumns-1:
                if self.screenMap[snakeY][snakeX+1]==0.5:
                    gameOver=True
                    reward=self.negReward
                elif self.screenMap[snakeY][snakeX+1]==1:
                    reward=self.posReward
                    self.moveSnake((snakeY,snakeX+1),True)
                elif self.screenMap[snakeY][snakeX+1]==0:
                    self.moveSnake((snakeY,snakeX+1),False)
            else:
                gameOver=True
                reward=self.negReward
        
        elif action==3:
            if snakeX>0:
                if self.screenMap[snakeY][snakeX-1]==0.5:
                    gameOver=True
                    reward=self.negReward
                elif self.screenMap[snakeY][snakeX-1]==1:
                    reward=self.posReward
                    self.moveSnake((snakeY,snakeX-1),True)
                elif self.screenMap[snakeY][snakeX-1]==0:
                    self.moveSnake((snakeY,snakeX-1),False)
            else:
                gameOver=True
                reward=self.negReward
        
        self.drawScreen()
        self.lastMove=action
        pg.time.wait(self.waitTime)
        return self.screenMap,reward,gameOver
    
    def reset(self):
        self.screenMap=np.zeros((self.nRows,self.nColumns))
        self.snakePos=list()
        for i in range(self.initSnakeLen):
            self.snakePos.append((int(self.nRows/2)+i,int(self.nColumns/2)))
            self.screenMap[int(self.nRows/2)+i][int(self.nColumns/2)]=0.5
        self.screenMap[self.applePos[0]][self.applePos[1]]=1
        self.lastMove=0




            