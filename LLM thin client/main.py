# main.py

from tkinter import Tk
from data_handler import DataHandler
from simple_gui import SimpleGUI

def main():
    data_handler = DataHandler()
    root = Tk()
    root.title("LLM Thin Client")

    gui = SimpleGUI(root, data_handler)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=0)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)

    root.state('normal') # Works on Windows
    root.minsize(1020, 680)

    gui.run()

if __name__ == "__main__":
    main()
