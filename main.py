import curses

from map import map
from player import player


class screen():

    def __init__(self):
        self.newwidth = 100000000000
        self.activeGame = True
        self.activeMenu = False
        self.MenuSelect = 1
        self.origin_x = 0
        self.origin_y = 0
        self.InfoLine = ["first", "second", "third", "fourth", "fifth"]
        self.Textmenu = ["", "historic", "second", "third", "fourth", "fifth"]
        self.BlockingBiome = ["OCEAN"]
        self.map = map()
        self.player = player()
        curses.wrapper(self.main)

    def ShowHistoric(self, screen):
        k = 0
        height, width = screen.getmaxyx()
        try:
            self.wMenu.erase()

        except:
            pass

        try:
            self.wInfo.erase()
            self.wTimeInd.erase()
            self.wBoard.erase()
        except:
            pass
        self.wHistoric = curses.newwin(int(height * 0.8), int(width * 0.8), int(height * 0.1), int(width * 0.1))
        self.wHistoric.box()
        height, width = self.wHistoric.getmaxyx()

        if ((height - 2) > len(self.InfoLine)):
            a = 0
        else:
            a = len(self.InfoLine) - height + 2

        for i in range(a, len(self.InfoLine)):
            self.wHistoric.addstr(i - a + 1, 1, self.InfoLine[i])

        self.wHistoric.refresh()

        while (k != ord('q')):
            if (k == curses.KEY_RESIZE):
                self.iniateWin(screen)
                self.RefreshWin(k)
                self.ShowHistoric(screen)
                break

            k = screen.getch()
        self.wHistoric.erase()

    ## create or recrate window after resize
    def iniateWin(self, screen):
        height, width = screen.getmaxyx()
        width += 1
        while (self.newwidth > width):
            width -= 1
            self.newwidth = int((height * 16) / 9)
        a = int(16 / 18 * height)
        b = int(12 / 32 * self.newwidth)
        c = width - b
        d = height - a

        self.player.bundary_x_plus = int(0.3 * width)
        self.player.bundary_x_less = int(0.7 * width)
        self.player.bundary_y_plus = int(0.3 * a)
        self.player.bundary_y_less = int(0.7 * a)

        try:
            self.wMenu.erase()

        except:
            pass

        try:
            self.wInfo.erase()
            self.wTimeInd.erase()
            self.wBoard.erase()
        except:
            pass

        if (self.activeMenu):
            self.wMenu = curses.newwin(a, b, 0, c)
            self.wBoard = curses.newwin(a, c + 1)
        else:
            self.wBoard = curses.newwin(a, width)

        self.wInfo = curses.newwin(d, c + 1, a - 1, 0)
        self.wTimeInd = curses.newwin(d, b, a - 1, c)

    def fillBoard(self):
        height, width = self.wBoard.getmaxyx()

        for ny in range(1, height - 1):

            for nx in range(1, width - 1):

                biome = self.map.mapreturn((self.origin_x + nx) / 30, (self.origin_y + ny) / 30)
                if biome == "OCEAN":
                    self.wBoard.addstr(ny, nx, "&", curses.color_pair(5))
                elif biome == "BEACH":
                    self.wBoard.addstr(ny, nx, "??", curses.color_pair(1))
                elif biome == "SCORCHED":
                    self.wBoard.addstr(ny, nx, "??", curses.color_pair(2))
                elif biome == "BARE":
                    self.wBoard.addstr(ny, nx, "c", curses.color_pair(2))
                elif biome == "TUNDRA":
                    self.wBoard.addstr(ny, nx, "??", curses.color_pair(3))
                elif biome == "SNOW":
                    self.wBoard.addstr(ny, nx, " ", curses.color_pair(3))
                elif biome == "TEMPERATE_DESERT":
                    self.wBoard.addstr(ny, nx, "??", curses.color_pair(2))
                elif biome == "SHRUBLAND":
                    self.wBoard.addstr(ny, nx, "??", curses.color_pair(4))
                elif biome == "TAIGA":
                    self.wBoard.addstr(ny, nx, "c", curses.color_pair(3))
                elif biome == "GRASSLAND":
                    self.wBoard.addstr(ny, nx, "??", curses.color_pair(4))
                elif biome == "TEMPERATE_DECIDUOUS_FOREST":
                    self.wBoard.addstr(ny, nx, "%", curses.color_pair(4))
                elif biome == "TEMPERATE_RAIN_FOREST":
                    self.wBoard.addstr(ny, nx, "$", curses.color_pair(4))
                elif biome == "SUBTROPICAL_DESERT":
                    self.wBoard.addstr(ny, nx, "$", curses.color_pair(6))
                elif biome == "TROPICAL_SEASONAL_FOREST":
                    self.wBoard.addstr(ny, nx, "??", curses.color_pair(4))
                elif biome == "TROPICAL_RAIN_FOREST":
                    self.wBoard.addstr(ny, nx, "???", curses.color_pair(4))
                if (self.player.currentBiome != biome and nx == self.player.cursor_x and ny == self.player.cursor_y):
                    self.player.currentBiome = biome
                    self.InfoLine.append("You are now in {}".format(biome))
                if (
                        self.player.Biome_x_less != biome and nx == self.player.cursor_x - 1 and ny == self.player.cursor_y):
                    self.player.Biome_x_less = biome
                if (
                        self.player.Biome_x_plus != biome and nx == self.player.cursor_x + 1 and ny == self.player.cursor_y):
                    self.player.Biome_x_plus = biome
                if (
                        self.player.Biome_y_less != biome and nx == self.player.cursor_x and ny == self.player.cursor_y - 1):
                    self.player.Biome_y_less = biome
                if (
                        self.player.Biome_y_plus != biome and nx == self.player.cursor_x and ny == self.player.cursor_y + 1):
                    self.player.Biome_y_plus = biome

    def fillMenu(self):
        self.wMenu.clear()

        for i in range(1, len(self.Textmenu)):
            if (i == self.MenuSelect):
                self.wMenu.addstr(2 * i - 1, 1, self.Textmenu[i], curses.color_pair(3))
            else:
                self.wMenu.addstr(2 * i - 1, 1, self.Textmenu[i])

    def fillWInfo(self, k):
        self.wInfo.clear()

        self.wInfo.addstr(1, 1, "Last key pressed: {}".format(k))  ## TEST PURPOSE

        for i in range(2, 3):
            self.wInfo.addstr(i, 1, self.InfoLine[len(self.InfoLine) + 1 - i])

    def RefreshWin(self, k):
        self.fillBoard()

        self.wBoard.addstr(self.player.cursor_y, self.player.cursor_x, "@", curses.color_pair(7))

        self.fillWInfo(k)

        if (self.activeMenu):
            self.fillMenu()
        if (self.activeMenu):
            self.wMenu.border()

        self.wInfo.border()
        self.wTimeInd.border()
        self.wBoard.border()
        self.wInfo.refresh()
        self.wTimeInd.refresh()
        self.wBoard.refresh()
        if (self.activeMenu):
            self.wMenu.refresh()

    def main(self, screen):

        k = 0

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        # Clear and refresh the screen for a blank canvas
        screen.clear()
        screen.refresh()
        ## curses.halfdelay(10) ## cause a type of fps n in tenths of sec
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK);
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLUE);
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK);
        curses.init_pair(7, curses.COLOR_RED, curses.COLOR_MAGENTA);

        self.iniateWin(screen)

        # Loop where k is the last character pressed
        while (self.activeGame):
            if (k == ord('q') and not self.activeMenu):
                self.activeGame = False
                break
            elif (k == curses.KEY_RESIZE):
                self.iniateWin(screen)
            elif (k == ord('m') or (k == ord('q') and self.activeMenu)):
                self.activeMenu = not self.activeMenu
                self.MenuSelect = 1
                self.iniateWin(screen)
            elif (k == curses.KEY_DOWN and self.activeMenu):
                self.MenuSelect += 1
                if (self.MenuSelect == 6):
                    self.MenuSelect = 1
            elif (k == curses.KEY_UP and self.activeMenu):
                self.MenuSelect -= 1
                if (self.MenuSelect == 0):
                    self.MenuSelect = 5
            elif (k == curses.KEY_DOWN and not self.activeMenu and self.player.Biome_y_plus not in self.BlockingBiome):
                self.player.cursor_y += 1
                if (self.player.cursor_y == self.player.bundary_y_less):
                    self.player.cursor_y -= 1
                    self.origin_y += 1
            elif (k == curses.KEY_UP and not self.activeMenu and self.player.Biome_y_less not in self.BlockingBiome):
                self.player.cursor_y -= 1
                if (self.player.cursor_y == self.player.bundary_y_plus):
                    self.player.cursor_y += 1
                    self.origin_y -= 1
            elif (k == curses.KEY_RIGHT and not self.activeMenu and self.player.Biome_x_plus not in self.BlockingBiome):
                self.player.cursor_x += 1
                if (self.player.cursor_x == self.player.bundary_x_less):
                    self.player.cursor_x -= 1
                    self.origin_x += 1
            elif (k == curses.KEY_LEFT and not self.activeMenu and self.player.Biome_x_less not in self.BlockingBiome):
                self.player.cursor_x -= 1
                if (self.player.cursor_x == self.player.bundary_x_plus):
                    self.player.cursor_x += 1
                    self.origin_x -= 1
            elif (k == ord('a') and self.activeMenu):
                if (self.MenuSelect == 1):
                    self.ShowHistoric(screen)

            self.RefreshWin(k)
            k = screen.getch()

            pass


def main():
    main = screen()


main()
