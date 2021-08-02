import curses


class screen():

    def __init__(self):
        self.newwidth = 100000000000
        self.activeMenu = False
        self.MenuSelect = 1
        self.cursor_x = 0
        self.cursor_y = 0
        self.InfoLine = ["first", "second", "third", "fourth", "fifth"]
        self.Textmenu = ["","historic", "second", "third", "fourth", "fifth"]

        curses.wrapper(self.main)

    ## TO REWORK
    def ShowHistoric(self,screen):
        k =0
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
        self.wHistoric = curses.newwin(int(height*0.8), int(width*0.8), int(height*0.1), int(width*0.1))
        self.wHistoric.box()

        for i in range(0, len(self.InfoLine)):
            self.wHistoric.addstr(i+1, 1, self.InfoLine[i])
        self.wHistoric.refresh()

        while (k != ord('q')):
            if (k == curses.KEY_RESIZE):
                self.iniateWin(screen)
                self.fillBoard()

                self.wMenu.border()
                self.wInfo.border()
                self.wTimeInd.border()
                self.wBoard.border()

                self.wBoard.addstr(self.cursor_y, self.cursor_x, "@", curses.color_pair(1))

                keystr = "Last key pressed: {}".format(k)

                self.wInfo.addstr(1, 1, keystr)
                for i in range(2, 5):
                    self.wInfo.addstr(i, 1, self.InfoLine[len(self.InfoLine) + 1 - i])

                if (self.activeMenu):
                    self.fillMenu()

                    for i in range(1, len(self.Textmenu)):
                        if (i == self.MenuSelect):
                            self.wMenu.addstr(2 * i - 1, 1, self.Textmenu[i], curses.color_pair(3))
                        else:
                            self.wMenu.addstr(2 * i - 1, 1, self.Textmenu[i])
                self.wInfo.refresh()
                self.wTimeInd.refresh()
                self.wBoard.refresh()
                self.wMenu.refresh()
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

    ##fill for pupose of test
    def fillBoard(self):
        height, width = self.wBoard.getmaxyx()

        for y in range(1, height - 1):
            for x in range(1, (width - 1)):
                self.wBoard.insch(y, x, ord('*'))

    def fillMenu(self):
        height, width = self.wMenu.getmaxyx()
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                self.wMenu.insch(y, x, ord(' '))

    def main(self, screen):

        k = 0

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        # Clear and refresh the screen for a blank canvas
        screen.clear()
        screen.refresh()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.iniateWin(screen)

        # Loop where k is the last character pressed
        while (k != ord('q')):

            if (k == curses.KEY_RESIZE):
                self.iniateWin(screen)
            elif (k == ord('m')):
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
            elif (k == curses.KEY_DOWN and not self.activeMenu):
                self.cursor_y += 1
            elif (k == curses.KEY_UP and not self.activeMenu):
                self.cursor_y -= 1
            elif (k == curses.KEY_RIGHT and not self.activeMenu):
                self.cursor_x += 1
            elif (k == curses.KEY_LEFT and not self.activeMenu):
                self.cursor_x -= 1
            elif (k == ord('a') and  self.activeMenu):
                if(self.MenuSelect==1):
                    self.ShowHistoric(screen)

            self.fillBoard()

            if (self.activeMenu):
                self.wMenu.border()
            self.wInfo.border()
            self.wTimeInd.border()
            self.wBoard.border()

            self.wBoard.addstr(self.cursor_y, self.cursor_x, "@", curses.color_pair(1))

            keystr = "Last key pressed: {}".format(k)

            self.wInfo.addstr(1, 1, keystr)
            for i in range(2, 5):
                self.wInfo.addstr(i, 1, self.InfoLine[len(self.InfoLine)+1-i])

            if (self.activeMenu):
                self.fillMenu()

                for i in range(1, len(self.Textmenu)):
                    if (i == self.MenuSelect):
                        self.wMenu.addstr(2 * i - 1, 1, self.Textmenu[i], curses.color_pair(3))
                    else:
                        self.wMenu.addstr(2 * i - 1, 1, self.Textmenu[i])
            self.wInfo.refresh()
            self.wTimeInd.refresh()
            self.wBoard.refresh()
            if (self.activeMenu):
                self.wMenu.refresh()

            k = screen.getch()

            pass


def main():
    main = screen()


main()
