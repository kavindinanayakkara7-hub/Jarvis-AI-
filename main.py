import tkinter as tk

from gui import JarvisGUI


def main():
    root = tk.Tk()

    app = JarvisGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()