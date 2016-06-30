import Tkinter as tk
import tkFont
import threading
import logging
import MBImport


class WidgetLogger(logging.Handler):
    def __init__(self, widget):
        logging.Handler.__init__(self)
        self.setLevel(logging.INFO)
        self.widget = widget
        self.widget.config(state='disabled')

    def emit(self, record):
        self.widget.config(state='normal')
        # Append message (record) to the widget
        self.widget.insert(tk.END, self.format(record) + '\n')
        self.widget.see(tk.END)  # Scroll to the bottom
        self.widget.config(state='disabled')


class MBTransfer:
    def __init__(self):
        # self.MBI = MBImport.MBImport(-99, -99)  # TESTING
        self.MBI = MBImport.MBImport(41095, 293010)  # LIVE

        self.root = tk.Tk()
        self.root.title("Mindbody Client Transfer")
        self.root.iconbitmap("vocademy.ico")

        self.mainframe = tk.Frame(self.root, padx=6, pady=6)
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.old_client = tk.StringVar()
        self.new_client = tk.StringVar()

    def handle_click(self, *args):
        def transfer():
            new_id = self.MBI.import_client(self.old_client.get())
            self.new_client.set(new_id)

            # Add blank line to log
            self.mainframe.children['log_output'].config(state='normal')
            self.mainframe.children['log_output'].insert(tk.END, '----\n')
            self.mainframe.children['log_output'].see(tk.END)  # Scroll to the bottom
            self.mainframe.children['log_output'].config(state='disabled')

        self.new_client.set(' ')
        t = threading.Thread(target=transfer)
        t.start()

    def setup_ui(self):
        input_frame = tk.Frame(self.mainframe, padx=2, pady=2)
        input_frame.grid(column=1, columnspan=1, row=1, rowspan=2, sticky=tk.N+tk.W)

        old_client_entry = tk.Entry(input_frame, width=20, textvariable=self.old_client)
        old_client_entry.grid(column=2, columnspan=1, row=1, sticky=tk.W)

        # tk.Label(self.mainframe, textvariable=new_client).grid(column=2, row=2, sticky=tk.E)
        tk.Entry(input_frame, width=20, textvariable=self.new_client, state="readonly").grid(column=2, columnspan=1, row=2, sticky=tk.W)

        tk.Label(input_frame, text="Old Client ID: ").grid(column=1, row=1, sticky=tk.E)
        tk.Label(input_frame, text="New Client ID: ").grid(column=1, row=2, sticky=tk.E)

        btn_font = tkFont.Font(family='Helvetica', size=18, weight='bold')
        tk.Button(self.mainframe, text="Transfer", font=btn_font, command=self.handle_click).grid(column=3, row=1, rowspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        # log_output = Tk.Message(mainframe, textvariable=log_message).grid(column=1, columnspan=3, row=4, sticky=S)
        scrollbar = tk.Scrollbar()
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E))
        log_output = tk.Text(self.mainframe, width=100, height=10, name='log_output', bg="gray95", fg="dark red", yscrollcommand=scrollbar.set)
        log_output.grid(column=1, columnspan=3, row=3, sticky=tk.S)
        scrollbar.config(command=log_output.yview)

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        old_client_entry.focus()
        self.root.bind('<Return>', self.handle_click)

    def setup_logging(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)

        logging_handler = WidgetLogger(self.mainframe.children['log_output'])
        log.addHandler(logging_handler)

    def run_app(self):
        self.setup_ui()
        self.setup_logging()
        self.root.mainloop()


if __name__ == "__main__":
    mbt = MBTransfer()
    mbt.run_app()
