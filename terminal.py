

ip = "10.38.254.252"
user = "red"
pas = "W1ldcat$"


import tkinter as tk
import subprocess
import threading

class TerminalEmulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mazi's Terminal Emulator")
        self.geometry("600x400")

        self.output_text = tk.Text(self, wrap=tk.WORD)
        self.output_text.pack(expand=True, fill=tk.BOTH)
        self.output_text.config(state=tk.DISABLED)

        self.input_field = tk.Entry(self)
        self.input_field.pack(fill=tk.X)
        self.input_field.bind("<Return>", self.execute_command)
        button = tk.Button(self.output_text, text="Breadrack3 Switch1")
        button.pack(pady=10)  # Add some padding around the button
        self.process = None

    def execute_command(self, event=None):
        command = self.input_field.get()
        self.input_field.delete(0, tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"$ {command}\n", "prompt")
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)

        if command.lower() == "exit":
            self.quit()
            return

        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        threading.Thread(target=self.read_output, args=()).start()

    def read_output(self):
        while self.process.poll() is None:
            output = self.process.stdout.readline().decode('utf-8')
            if output:
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, output)
                self.output_text.config(state=tk.DISABLED)
                self.output_text.see(tk.END)

if __name__ == "__main__":
    app = TerminalEmulator()
    app.mainloop()
