from random import *


class GameField:
    def __init__(self, botMapSave=None, userMapSave=None, botMapForUserSave=None, shipCountUserSave=20, shipCountBotSave=20,
                 hodi=[], drctForShot=[[0, -1], [0, 1], [-1, 0], [1, 0]],  lst=[-1, -1], drctx=[-1, -1], drctx2=[-1, -1],
                 whoIsTurn=randint(0, 1)):
        self.botMapForUser = [[0 for i in range(10)] for j in range(10)]
        self.botMap = [[0 for i in range(10)] for j in range(10)]
        self.userMap = [[0 for i in range(10)] for j in range(10)]
        if botMapSave != None:
            self.botMap = botMapSave
        if userMapSave != None:
            self.userMap = userMapSave
        if botMapForUserSave != None:
            self.botMapForUser = botMapForUserSave
        self.shipCountUser = shipCountUserSave
        self.shipCountBot = shipCountBotSave
        self.whoIsTurn = whoIsTurn
        self.ShipsCnt = [0, 0, 0, 0]
        self.bot = Bot(self.botMap, self, hodi, drctForShot, lst, drctx, drctx2)

    def placeShip(self, field, shipSize, rotate, startPointX, startPointY):
        try:
            keys = {'А': 0, 'Б': 1, 'В': 2, 'Г': 3, 'Д': 4, 'Е': 5, 'Ж': 6, 'З': 7, 'И': 8, 'К': 9}
            startPointX -= 1
            tst = startPointX
            rotate = rotate.lower()
            startPointY = keys[startPointY.upper()]
            startPointX = startPointY
            startPointY = tst
            if 10 > startPointX >= 0 and 10 > startPointY >= 0:
                if rotate == "вправо":
                    if startPointX + shipSize <= 10:
                        if startPointX - 1 >= 0:
                            if field[startPointX - 1][startPointY] == 1:
                                return False
                        if field[startPointX][startPointY] == 1:
                            return False
                        for i in range(startPointX, startPointX + shipSize):
                            if i + 1 < 10:
                                if field[i + 1][startPointY] == 1:
                                    return False
                            if startPointY + 1 < 10:
                                if field[i][startPointY + 1] == 1:
                                    return False
                            if startPointY - 1 >= 0:
                                if field[i][startPointY - 1] == 1:
                                    return False
                        for i in range(startPointX, startPointX + shipSize):
                            field[i][startPointY] = 1
                        self.ShipsCnt[shipSize - 1] += 1
                        return True
                    return False
                elif rotate == "влево":
                    if 0 <= startPointX - shipSize + 1:
                        if startPointX - shipSize + 1 >= 0:
                            if startPointX - shipSize >= 0:
                                if field[startPointX - shipSize][startPointY] == 1:
                                    return False
                            if field[startPointX][startPointY] == 1:
                                return False
                            for i in range(startPointX - shipSize + 1, startPointX + 1):
                                if i + 1 < 10:
                                    if field[i + 1][startPointY] == 1:
                                        return False
                                if startPointY + 1 < 10:
                                    if field[i][startPointY + 1] == 1:
                                        return False
                                if startPointY - 1 >= 0:
                                    if field[i][startPointY - 1] == 1:
                                        return False
                            for i in range(startPointX - shipSize + 1, startPointX + 1):
                                field[i][startPointY] = 1
                            self.ShipsCnt[shipSize - 1] += 1
                            return True
                    return False
                elif rotate == "вниз":
                    if startPointY + shipSize <= 10:
                        if startPointY - 1 >= 0:
                            if field[startPointX][startPointY - 1] == 1:
                                return False
                        if field[startPointX][startPointY] == 1:
                            return False
                        for i in range(startPointY, startPointY + shipSize):
                            if i + 1 < 10:
                                if field[startPointX][i + 1] == 1:
                                    return False
                            if startPointX + 1 < 10:
                                if field[startPointX + 1][i] == 1:
                                    return False
                            if startPointX - 1 >= 0:
                                if field[startPointX - 1][i] == 1:
                                    return False
                        for i in range(startPointY, startPointY + shipSize):
                            field[startPointX][i] = 1
                        self.ShipsCnt[shipSize - 1] += 1
                        return True
                    return False
                elif rotate == "вверх":
                    if startPointY - shipSize + 1 >= 0:
                        if startPointY - shipSize >= 0:
                            if field[startPointX][startPointY - shipSize] == 1:
                                return False
                        if field[startPointX][startPointY] == 1:
                            return False
                        for i in range(startPointY - shipSize + 1, startPointY + 1):
                            if i + 1 < 10:
                                if field[startPointX][i + 1] == 1:
                                    return False
                            if startPointX + 1 < 10:
                                if field[startPointX + 1][i] == 1:
                                    return False
                            if startPointX - 1 >= 0:
                                if field[startPointX - 1][i] == 1:
                                    return False
                        for i in range(startPointY - shipSize + 1, startPointY + 1):
                            field[startPointX][i] = 1
                        self.ShipsCnt[shipSize - 1] += 1
                        return True
                    return False
                else:
                    return False
            else:
                return False
        except BaseException:
            return False

    def shotBot(self, x, y):
        tst = x
        x = y
        y = tst
        tst = self.userMap[x][y]
        if tst == 1:
            self.userMap[x][y] = 3
            self.shipCountUser -= 1
        elif tst == 0:
            self.userMap[x][y] = 2
        return tst

    def shotUser(self, x, y):
        keys = {'А': 0, 'Б': 1, 'В': 2, 'Г': 3, 'Д': 4, 'Е': 5, 'Ж': 6, 'З': 7, 'И': 8, 'К': 9}
        x -= 1
        tst = x
        y = keys[y.upper()]
        x = y
        y = tst
        tst = self.botMap[x][y]
        if tst == 1:
            self.botMapForUser[x][y] = 3
            self.shipCountBot -= 1
        elif tst == 0:
            self.swapTrurn()
            self.botMapForUser[x][y] = 2
        else:
            self.swapTrurn()
        return tst

    def swapTrurn(self):
        if self.whoIsTurn == 0:
            self.whoIsTurn = 1
        else:
            self.whoIsTurn = 0

    def autoCreate(self):
        rotate = ["влево", "вправо", "вверх", "вниз"]
        posY = "АБВГДЕЖЗИК"
        for i in range(4):
            for j in range(i + 1):
                x, y = randint(1, 10), posY[randint(0, 9)]
                while not self.placeShip(self.userMap, 4 - i, choice(rotate), x, y):
                    x, y = randint(1, 10), posY[randint(0, 9)]

    def restart(self):
        self.botMapForUser = [[0 for i in range(10)] for j in range(10)]
        self.botMap = [[0 for i in range(10)] for j in range(10)]
        self.userMap = [[0 for i in range(10)] for j in range(10)]
        self.shipCountUser = 20
        self.shipCountBot = 20
        self.whoIsTurn = randint(0, 1)
        self.bot.restart()


class Bot:
    def __init__(self, map, GameField, hodi=[], drctForShot=[[0, -1], [0, 1], [-1, 0], [1, 0]], lst=[-1, -1], drctx=[-1, -1], drctx2=[-1, -1]):
        self.map = map
        self.hodi = hodi
        self.x = -1
        self.y = -1
        self.lst = lst
        self.drctx = drctx
        self.drctx2 =drctx2
        self.drctForShot = drctForShot
        self.enemyShipsShotten = []
        self.GameField = GameField
        rotate = ["влево", "вправо", "вверх", "вниз"]
        posY = "АБВГДЕЖЗИК"
        if self.map == [[0 for i in range(10)] for j in range(10)]:
            for i in range(4):
                for j in range(i + 1):
                    x, y = randint(1, 10), posY[randint(0, 9)]
                    while not GameField.placeShip(self.map, 4 - i, choice(rotate), x, y):
                        x, y = randint(1, 10), posY[randint(0, 9)]

    def hod(self):
        if self.lst == [-1, -1] and self.GameField.shipCountUser > 0:
            for i in self.enemyShipsShotten:
                self.hodi.append([i[0] + 1, i[1]])
                self.hodi.append([i[0] - 1, i[1]])
                self.hodi.append([i[0], i[1] + 1])
                self.hodi.append([i[0], i[1] - 1])
            self.drctForShot = [[0, -1], [0, 1], [-1, 0], [1, 0]]
            x, y = randint(0, 9), randint(0, 9)
            while [x, y] in self.hodi:
                x, y = randint(0, 9), randint(0, 9)
            result = self.GameField.shotBot(x, y)
            if result == 1:
                self.lst = [x, y]
                self.enemyShipsShotten.append([x, y])
            else:
                self.GameField.swapTrurn()
            self.hodi.append([x, y])
        elif self.GameField.shipCountUser > 0:
            if self.drctx2 == [-1, -1] and len(self.drctForShot) > 0:
                self.drctx = choice(self.drctForShot)
                self.drctForShot.remove(self.drctx)
                self.x, self.y = self.lst
                if 10 > self.y + self.drctx[1] >= 0 and 10 > self.x + self.drctx[0] >= 0 and \
                        [self.x + self.drctx[0], self.y + self.drctx[1]] not in self.hodi:
                    self.y += self.drctx[1]
                    self.x += self.drctx[0]
                    rslt = self.GameField.shotBot(self.x, self.y)
                    self.hodi.append([self.x, self.y])
                    if rslt == 1:
                        self.drctx2 = self.drctx
                        self.enemyShipsShotten.append([self.x, self.y])
                    else:
                        self.GameField.swapTrurn()
                        self.drctx2 = [-1, -1]
                else:
                    self.drctx2 = [-1, -1]
                    self.hod()
            elif self.drctx2 != [-1, -1]:
                if 10 > self.y + self.drctx2[1] >= 0 and 10 > self.x + self.drctx2[0] >= 0 and \
                        [self.x + self.drctx2[0], self.y + self.drctx2[1]] not in self.hodi:
                    self.y += self.drctx2[1]
                    self.x += self.drctx2[0]
                    rslt = self.GameField.shotBot(self.x, self.y)
                    self.hodi.append([self.x, self.y])
                    if rslt == 1:
                        self.drctx2 = self.drctx
                        self.enemyShipsShotten.append([self.x, self.y])
                    else:
                        self.GameField.swapTrurn()
                        self.drctx2 = [-1, -1]
                else:
                    self.drctx2 = [-1, -1]
                    self.hod()
            else:
                self.lst = [-1, -1]
                self.drctx = [-1, -1]
                self.drctx2 = [-1, -1]
                self.GameField.swapTrurn()
        if self.GameField.shipCountUser <= 0:
            return True
        return False

    def restart(self):
        self.hodi = []
        self.x = -1
        self.y = -1
        self.lst = [-1, -1]
        self.drctx = [-1, -1]
        self.drctx2 = [-1, -1]
        self.drctForShot = [-1, -1]
        self.enemyShipsShotten = []
        self.GameField = GameField
        rotate = ["влево", "вправо", "вверх", "вниз"]
        posY = "АБВГДЕЖЗИК"
        if self.map == [[0 for i in range(10)] for j in range(10)]:
            for i in range(4):
                for j in range(i + 1):
                    x, y = randint(1, 10), posY[randint(0, 9)]
                    while not GameField.placeShip(self.map, 4 - i, choice(rotate), x, y):
                        x, y = randint(1, 10), posY[randint(0, 9)]