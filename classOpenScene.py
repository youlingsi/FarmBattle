class OpenScene(object):
    def __init__(self, width,height):
        self.width = width
        self.height = height
        # backgroung color
        self.BGcolor = (20,50,20)
        # game title text properties
        self.gameTitle = "Farm Battle"
        self.titleSize = height // 10
        self.titleFont = 'Comic Sans MS'
        self.titleColor = (255,231,53)
        # selection texts properties
        self.fontSize = self.titleSize//2
        self.fontName = 'Comic Sans MS'
        self.fontColor = (255,231,53)
        self.selectionStage = 0 #0=slect playerrol, 1 select mAI, 2 select fAI
        # selection 1:
        self.opt1 = "Select Players Role"
        self.playerRole = 0 #0-farmer, 1 = Mole
        # selection 2:
        self.opt2 = "Turn AI on/off"
        self.sMAIOn = "Mole AI On"
        self.sMAIOff = "Mole AI Off"
<<<<<<< HEAD
=======
        # Selection 3
>>>>>>> 5039ed1261ecaad475738703d0384ace26f87944
        self.sFAIOn = "Farmer AI On"
        self.sFAIOff = "Farmer AI Off"
        self.mAIon = False # mole AI switch
        self.fAIon = False # farmer AI switch
<<<<<<< HEAD
=======
        # Selection 4: Loading
        self.loading = "LOADING"
>>>>>>> 5039ed1261ecaad475738703d0384ace26f87944
        # properties of all the elements
        self.allElement = {}


    #pass the players selection to game map
    def selectionTogm(self,gm):
        gm.playerRole = self.playerRole
        gm.mAIon = self.mAIon
        gm.fAIon = self.fAIon
