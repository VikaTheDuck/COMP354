from tkinter import *


class TextEditor:
    newInput = False
    input = ""
    entryList = []
    iterator = 0
    highContrast = False

    # Window Objects
    window = None
    output = None
    textEntry = None
    enter = None
    previous = None
    next = None
    contrast = None

    def create_window(self):
        self.window = Tk()
        self.window.configure(bg="#646464")
        self.output = Text(self.window, wrap=WORD, bg="#cee8ff")
        self.textEntry = Entry(self.window, bg="#f1f4f8", width=93)

        self.window.title("Algorithm Calculator")
        self.window.geometry("646x345")
        self.window.resizable(False, False)

        self.output.grid(row=0, column=0, columnspan=4, rowspan=5)
        self.output.config(state=DISABLED)

        self.textEntry.grid(row=5, column=0, columnspan=4, sticky=W)

        self.enter = Button(self.window, text="Enter", width=10, command=self.click_enter, bg="#268c21")
        self.enter.grid(row=5, column=4)

        self.previous = Button(self.window, text="Previous", width=10, command=self.click_previous, bg="#ffb600")
        self.previous.grid(row=3, column=4)

        self.next = Button(self.window, text="Next", width=10, command=self.click_next, bg="#ffb600")
        self.next.grid(row=4, column=4)

        self.contrast = Button(self.window, text="High Contrast", width=10, command=self.click_contrast, bg="#ffffff")
        self.contrast.grid(row=0, column=4)

    # Click enter function
    def click_enter(self):
        self.newInput = True
        self.input = self.textEntry.get()
        self.entryList.append(self.input)
        self.iterator = len(self.entryList)
        self.textEntry.delete(0, END)

        self.output.config(state=NORMAL)
        self.output.insert(INSERT, ">" + self.input + "\n")
        self.output.config(state=DISABLED)

    def click_previous(self):
        if self.iterator > 0:
            self.iterator -= 1
            self.textEntry.delete(0, END)
            self.textEntry.insert(INSERT, self.entryList[self.iterator])

    def click_next(self):
        if self.iterator < len(self.entryList) - 1:
            self.iterator += 1
            self.textEntry.delete(0, END)
            self.textEntry.insert(INSERT, self.entryList[self.iterator])

    def click_contrast(self):
        if self.highContrast:
            self.highContrast = False
            self.window.configure(bg="#646464")
            self.output.configure(bg="#cee8ff")
            self.textEntry.configure(bg="#f1f4f8")
            self.enter.configure(bg="#268c21")
            self.previous.configure(bg="#ffb600")
            self.next.configure(bg="#ffb600")
        else:
            self.highContrast = True
            self.window.configure(bg="#ffffff")
            self.output.configure(bg="#ffffff")
            self.textEntry.configure(bg="#ffffff")
            self.enter.configure(bg="#ffffff")
            self.previous.configure(bg="#ffffff")
            self.next.configure(bg="#ffffff")

    def check_input(self):
        if self.newInput:
            self.newInput = False
            return self.input
        else:
            return None

    def output_text(self, output_string):
        self.output.config(state=NORMAL)
        self.output.insert(INSERT, output_string + "\n")
        self.output.config(state=DISABLED)


if __name__ == '__main__':
    window = TextEditor()
    window.create_window()
    while True:
        # Updates the UI
        window.window.update()

        # Checks for text input from the window
        input = window.check_input()
        #TODO CALCULATOR
        if input is not None:
            # Pass input to the parser (Just printing for now instead)
            print(input)

            # Pass error or output back to the window from the parser
            #window.output_text(outputstring)
