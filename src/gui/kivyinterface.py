from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock


import os

class LoadFileWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def open(self, path, filename):
        sm.current = "main"
        mainScreen = sm.get_screen('main')
        mainScreen.renderData(path, filename)


class MainWindow(Screen):
    userChatText = ObjectProperty(None)
    completeLabel = ObjectProperty(None)
    current = ""

    def to_be_called(self, dt):
        self.userChatText.text = str(self.userTypedText)
        self.do_the_loop()
        #self.event.cancel()

    def do_the_loop(self):
        if len(self.dataList) > 0:
            line = self.dataList.pop(0)
            data = [x.strip() for x in line.split(',')]
            print('data[0]=',data[0])
            if data[1].isnumeric():
                userTimestamp = int(data[1])
            else:
                userTimestamp = self.prevTime + 100
            print('userTimestamp=', userTimestamp)
            typedChar = data[0]
            if data[0] == '*SPACE*':
                typedChar = ' '
            elif data[0] == '*BS*':
                typedChar = ''
                self.userTypedText = self.userTypedText[:-1]
            elif data[0] == '*ENTER*':
                typedChar = '\n'
            if self.prevTime == 0:
                self.userTypedText = typedChar
                Clock.schedule_once(self.to_be_called, 0.5)
            else:
                self.userTypedText = self.userTypedText + typedChar
                diffTime = (userTimestamp - self.prevTime)/1000
                print(diffTime)
                Clock.schedule_once(self.to_be_called, diffTime)
            self.prevTime = userTimestamp
        else:
            self.completeLabel.text = 'Finished'

    def renderData(self, path, filename):
        self.userTypedText = ''
        self.completeLabel.text = ''
        self.dataList = []
        self.prevTime = 0
        file = open(os.path.join(path, filename[0]), "r")

        for line in file:
            if len(line) > 10:
                self.dataList.append(line)
        self.do_the_loop()





class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("./gui/ui.kv")

sm = WindowManager()

screens = [LoadFileWindow(name="loadFile"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"


class MyMainApp(App):
    def build(self):
        return sm

def main():
    MyMainApp().run()

if __name__ == "__main__":
    main()
