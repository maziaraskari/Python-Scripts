import tkinter as tk
import paramiko
import subprocess




def say_hello():
    print("Hello World")
    #subprocess.run(["ls", "-l"])
    #subprocess.run(["sudo", "ssh", "red@10.38.254.224"])
    


window = tk.Tk()
window.title("Mazi's SSH")

label = tk.Label(window, text="Hello World")
label.pack(pady=10)  # Add some padding around the label
button = tk.Button(window, text="Breadrack3 Switch1", command=say_hello)
button.pack(pady=10)  # Add some padding around the button



window.mainloop()
    
