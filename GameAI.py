#!/usr/bin/env python

"""GameAI.py: INF1771 GameAI File - Where Decisions are made."""
#############################################################
#Copyright 2020 Augusto Baffa
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#############################################################
__author__      = "Augusto Baffa"
__copyright__   = "Copyright 2020, Rio de janeiro, Brazil"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "abaffa@inf.puc-rio.br"
#############################################################

import random
from Map.Position import Position

# <summary>
# Game AI Example
# </summary>
class GameAI():

    player = Position()
    state = "ready"
    dir = "north"
    score = 0
    energy = 0
    command = []
    scoreDelta = 0
    stateMachine = "hunt"
    previousStateMachine = ""
    observations = []
    cmdCount = 0
    

    # <summary>
    # Refresh player status
    # </summary>
    # <param name="x">player position x</param>
    # <param name="y">player position y</param>
    # <param name="dir">player direction</param>
    # <param name="state">player state</param>
    # <param name="score">player score</param>
    # <param name="energy">player energy</param>
    def SetStatus(self, x, y, dir, state, score, energy):
    
        self.player.x = x
        self.player.y = y
        self.dir = dir.lower()

        self.state = state
        self.score = score
        self.energy = energy


    # <summary>
    # Get list of observable adjacent positions
    # </summary>
    # <returns>List of observable adjacent positions</returns>
    def GetObservableAdjacentPositions(self):
        ret = []

        ret.append(Position(self.player.x - 1, self.player.y))
        ret.append(Position(self.player.x + 1, self.player.y))
        ret.append(Position(self.player.x, self.player.y - 1))
        ret.append(Position(self.player.x, self.player.y + 1))

        return ret


    # <summary>
    # Get list of all adjacent positions (including diagonal)
    # </summary>
    # <returns>List of all adjacent positions (including diagonal)</returns>
    def GetAllAdjacentPositions(self):
    
        ret = []

        ret.Add(Position(self.player.x - 1, self.player.y - 1))
        ret.Add(Position(self.player.x, self.player.y - 1))
        ret.Add(Position(self.player.x + 1, self.player.y - 1))

        ret.Add(Position(self.player.x - 1, self.player.y))
        ret.Add(Position(self.player.x + 1, self.player.y))

        ret.Add(Position(self.player.x - 1, self.player.y + 1))
        ret.Add(Position(self.player.x, self.player.y + 1))
        ret.Add(Position(self.player.x + 1, self.player.y + 1))

        return ret
    

    # <summary>
    # Get next forward position
    # </summary>
    # <returns>next forward position</returns>
    def NextPosition(self):
    
        ret = None
        
        if self.dir == "north":
            ret = Position(self.player.x, self.player.y - 1)
                
        elif self.dir == "east":
                ret = Position(self.player.x + 1, self.player.y)
                
        elif self.dir == "south":
                ret = Position(self.player.x, self.player.y + 1)
                
        elif self.dir == "west":
                ret = Position(self.player.x - 1, self.player.y)

        return ret
    

    # <summary>
    # Player position
    # </summary>
    # <returns>player position</returns>
    def GetPlayerPosition(self):
        return self.player


    # <summary>
    # Set player position
    # </summary>
    # <param name="x">x position</param>
    # <param name="y">y position</param>
    def SetPlayerPosition(self, x, y):
        self.player.x = x
        self.player.y = y

    

    # <summary>
    # Observations received
    # </summary>
    # <param name="o">list of observations</param>
    def GetObservations(self, o):
        self.observations = o

    # <summary>
    # No observations received
    # </summary>
    def GetObservationsClean(self):
        pass
    

    # <summary>
    # Get Decision
    # </summary>
    # <returns>command string to new decision</returns>
    def GetDecision(self):
        print ("---\nObservations: " + str(self.observations) + "\nEnergia: " + str(self.energy) + "\nState: " + self.stateMachine + "\nCommand Buffer: " + str(self.command))
        return self.StateMachineEngine(self.observations)
    
    def StateMachineEngine (self, observations):
        #retornos possiveis: virar_direita, virar_esquerda, andar, atacar, pegar_ouro, pegar_anel, pegar_powerup, andar_re
        
        #definição do novo estado a partir das informações do estado atual e das observações
        if not observations: #não há observações
            if (self.stateMachine == "gather_ouro"
               or self.stateMachine == "gather_anel"
               or self.stateMachine == "gather_powerup"
               or self.stateMachine == "seek"
               or self.stateMachine == "destroy"):
                self.stateMachine = "hunt"
            elif (self.stateMachine == "bonk" or self.stateMachine == "its_a_trap"):
                self.stateMachine = self.previousStateMachine
            
        elif any(substring in "breeze" for substring in observations):
            if self.stateMachine == "hunt" or self.stateMachine == "fly_you_fool":
                self.previousStateMachine = self.stateMachine
                self.stateMachine = "its_a_trap"
                
        elif any(substring in "damage, steps" for substring in observations):
            if self.energy > 25:
                self.stateMachine = "seek"
                
            else:
                self.stateMachine = "fly_you_fool"
                    
        elif any(substring in "bluelight" for substring in observations):
            if self.stateMachine == "hunt":
                self.stateMachine = "gather_powerup"
                
        elif any(substring in "redlight" for substring in observations):
            if self.stateMachine == "hunt":
                self.stateMachine = "gather_ouro"
            elif self.stateMachine == "gather_ouro":
                self.stateMachine = "gather_anel"
                
        elif any(substring in "blocked" for substring in observations):
            if self.stateMachine == "hunt" or self.stateMachine == "fly_you_fool":
                self.previousStateMachine = self.stateMachine
                self.stateMachine = "bonk"
            
        elif any(substring in "hit" for substring in observations):
            if self.energy > 25:
                self.stateMachine = "destroy"
                self.cmdCount = 0
            else:
                self.stateMachine = "fly_you_fool"
        
        #ação do novo estado
        if not self.command: #lista de comandos vazia
            if self.stateMachine == "hunt":
                n = random.randint(0, 99)
                if n < 10:
                    self.command.append("virar_direita")
                elif n < 20:
                    self.command.append("virar_esquerda")
                else:
                    self.command.append("andar") 
                
            elif self.stateMachine == "its_a_trap":
                self.command.append("andar_re")
                self.command.append("virar_direita") #MUDANÇA: mudar pra random?
                
            elif self.stateMachine == "fly_you_fool":
                pass #FALTA: função de fuga, precisa eventualmente mudar o estado para "hunt"
                
            elif self.stateMachine == "seek":
                self.command.append("atacar")
                self.command.append("virar_direita")
                self.command.append("atacar")
                self.command.append("virar_direita")
                self.command.append("atacar")
                self.command.append("virar_direita")
                self.command.append("atacar")
            
            elif self.stateMachine == "destroy":
                self.command.append("atacar")
            
            elif self.stateMachine == "bonk":
                self.command.append("virar_direita")  #MUDANÇA: mudar pra random?
            
            elif self.stateMachine == "gather_powerup":
                self.command.append("pegar_powerup")
            
            elif self.stateMachine == "gather_ouro":
                self.command.append("pegar_ouro")
            
            elif self.stateMachine == "gather_anel":
                self.command.append("pegar_anel")

        ret = self.command[0]
        print("ret = " + ret)
        self.command.remove(ret)
        return ret