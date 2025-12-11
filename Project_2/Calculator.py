from tkinter import *

class Calculator(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.formula = "0"
        self.build()

    def build(self):
        # Отображение формулы
        self.lbl = Label(self, text=self.formula, font=("Times New Roman", 21, "bold"),
                         bg="#000", fg="#FFF", anchor=E)
        self.lbl.pack(fill="both", pady=20, padx=10)

        # Кнопки
        btns = [
            "C", "DEL", "*", "=",
            "1", "2", "3", "/",
            "4", "5", "6", "+",
            "7", "8", "9", "-",
            "(", "0", ")", "x^"
        ]

        btn_frame = Frame(self)
        btn_frame.pack()

        x = 0
        y = 0
        for bt in btns:
            com = lambda x=bt: self.press(x)
            Button(btn_frame, text=bt, bg="#FFF", font=("Times New Roman", 15), command=com,
                   width=5, height=2).grid(row=y, column=x, padx=5, pady=5)
            x += 1
            if x > 3:
                x = 0
                y += 1

    def press(self, key):
        if key == "C":
            self.formula = "0"
        elif key == "DEL":
            self.formula = self.formula[:-1] if len(self.formula) > 1 else "0"
        elif key == "x^":
            try:
                self.formula = str(eval(self.formula) ** 2)
            except:
                self.formula = "Error"
        elif key == "=":
            try:
                self.formula = str(eval(self.formula))
            except:
                self.formula = "Error"
        else:
            if self.formula == "0":
                self.formula = ""
            self.formula += key
        self.update_display()

    def update_display(self):
        self.lbl.config(text=self.formula)

if __name__ == '__main__':
    root = Tk()
    root.title("Калькулятор")
    root.geometry("500x600")
    root.configure(bg="#000")
    root.resizable(False, False)

    calc = Calculator(root)
    calc.pack(expand=True, fill="both")

    root.mainloop()
