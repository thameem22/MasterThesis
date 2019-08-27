import os

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from service.compare_independent_samples import StudentsT
from service.feature_impl import Feature


class LoadFileWindow(Screen):
    """
        This is a class to load a file in a screen.
    """

    def open(self, path, filename):
        """
            This method loads a chat in the browser and switches to main screen

            Parameters:
            path (string): The path of the CSV file
            filename (string): The name of the CSV file
        """
        sm.current = "main"
        mainScreen = sm.get_screen('main')
        mainScreen.renderData(path, filename)


class PopupWindow(Screen):
    """
        This is a class to show the contents in a screen.

        Attributes:
            prevScreen (string): To store previous screen name.
    """
    prevScreen = None

    def open(self, choice):
        """
            This method displays the results when a feature is selected from drop down.

            Parameters:
            choice (string): A feature name.
        """
        result = feature.calculateFeature(choice)
        self.prevScreen = 'main'
        self.contentText.text = result

    def loadResult(self, result):
        """
            This method displays the results of t test.

            Parameters:
            result (string): The results from t test.
        """
        self.prevScreen = 'compare'
        self.contentText.text = result

    def close(self):
        """
            This method switches back to the previous screen.
        """
        sm.current = self.prevScreen


class MainWindow(Screen):
    """
        This is a class to display the default screen.

        Attributes:
            userChatText (string): The string to store the text typed by a user.
            completeLabel (string): The string to display completed message.
    """
    userChatText = ObjectProperty(None)
    completeLabel = ObjectProperty(None)
    current = ""

    def appendOutput(self, dt):
        """
            This method appends the text to be shown in chat.

            Parameters:
            dt (int): the difference in time between previous and current character.
        """
        self.userChatText.text = str(self.userTypedText)
        self.displayOutputInTimestamp()
        # self.event.cancel()

    def displayOutputInTimestamp(self):
        """
            This method displays the chat in browser as per the timestamp.
        """
        if len(self.dataList) > 0:
            line = self.dataList.pop(0)
            data = [x.strip() for x in line.split(',')]
            if data[1].isnumeric():
                userTimestamp = int(data[1])
            else:
                userTimestamp = self.prevTime + 100
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
                Clock.schedule_once(self.appendOutput, 0.5)
            else:
                self.userTypedText = self.userTypedText + typedChar
                diffTime = (userTimestamp - self.prevTime) / 1000
                Clock.schedule_once(self.appendOutput, diffTime)
            self.prevTime = userTimestamp
        else:
            self.completeLabel.text = 'Finished'

    def renderData(self, path, filename):
        """
            This method loads a CSV file and displays the chat in browser.

            Parameters:
            path (string): The path of a file.
            filename (string): The name of a file.
        """
        self.userTypedText = ''
        self.completeLabel.text = ''
        self.dataList = []
        self.prevTime = 0
        file = open(os.path.join(path, filename[0]), "r")

        for line in file:
            if len(line) > 10:
                self.dataList.append(line)
        feature.featureInit(self.dataList)
        self.displayOutputInTimestamp()

    def fetchFeatureData(self, value):
        """
            This method fetches the output when a feature is selected.

            Parameters:
            value (string): The name of a feature.
        """
        sm.current = "popup"
        popupScreen = sm.get_screen('popup')
        popupScreen.open(value)


class LoadDialogCallerWindow(Screen):
    """
        This is a class to load the caller directory in a screen.
    """

    def load(self, path):
        """
            This method loads the window to get the callers path.

            Parameters:
            path (string): The path of the callers directory.
        """
        compareScreen = sm.get_screen('compare')
        compareScreen.callerTextInput.text = path
        self.cancel()

    def cancel(self):
        """
            This method switches back to the compare screen.
        """
        compareScreen = sm.get_screen('compare')
        compareScreen.dismissPopup()


class LoadDialogReceiverWindow(Screen):
    """
        This is a class to load the receiver directory in a screen.
    """

    def load(self, path):
        """
            This method loads the window to get the receivers path.

            Parameters:
            path (string): The path of the receivers directory.
        """
        compareScreen = sm.get_screen('compare')
        compareScreen.receiverTextInput.text = path
        self.cancel()

    def cancel(self):
        """
            This method switches back to the compare screen.
        """
        compareScreen = sm.get_screen('compare')
        compareScreen.dismissPopup()


class CompareWindow(Screen):
    """
        This is a class to compare the caller and receiver chat in a screen.

        Attributes:
            compareErrorLabel (string): The string to display an error message.
    """
    compareErrorLabel = ObjectProperty(None)

    def dismissPopup(self):
        """
            This method switches back to main screen.
        """
        self._popup.dismiss()

    def showLoadCaller(self):
        """
            This method loads the window to get the callers path.
        """
        content = LoadDialogCallerWindow()
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def showLoadReceiver(self):
        """
            This method loads the window to get the receivers path.
        """
        content = LoadDialogReceiverWindow()
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def compare_data(self):
        """
            This method compares the callers and receivers path using t test.
        """
        if self.callerTextInput.text == '':
            self.compareErrorLabel.text = 'Caller Path is mandatory'
        elif self.receiverTextInput.text == '':
            self.compareErrorLabel.text = 'Receiver Path is mandatory'
        else:
            self.compareErrorLabel.text = ''

            studentT = StudentsT()
            output = studentT.run(self.callerTextInput.text, self.receiverTextInput.text)

            sm.current = "popup"
            popupScreen = sm.get_screen('popup')
            popupScreen.loadResult(output)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("./gui/ui.kv")

sm = WindowManager()
feature = Feature()

screens = [LoadFileWindow(name="loadFile"), MainWindow(name="main"), PopupWindow(name="popup")
    , LoadDialogCallerWindow(name="loadDialogCaller"), LoadDialogReceiverWindow(name="loadDialogReceiver")
    , CompareWindow(name="compare")]
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
