import tkinter as tk            # GUI library
from tkinter import filedialog, messagebox  # dialogs
from PIL import Image           # image handling
import datetime                
import os                       # file handling

class SecureStegoToolkit:
    def __init__(self, root):
        self.root = root        # main window
        self.root.title("Information Security Lab | Steganography Toolkit")
        self.root.geometry("850x600")   # window size
        self.root.configure(bg="#121212")  # background color
        
        # Session Data
        self.history_log = []   # activity log
        self.admin_pass = "ZirwaCheema123"  # admin password
        
        # Dashboard Layout
        self.sidebar = tk.Frame(self.root, bg="#1e1e1e", width=200)  # sidebar frame
        self.sidebar.pack(side="left", fill="y")  # sidebar position
        
        self.main_area = tk.Frame(self.root, bg="#121212")  # main frame
        self.main_area.pack(side="right", expand=True, fill="both")  # expand area
        
        self.setup_sidebar()    # load sidebar
        self.show_home()        # show home

    def setup_sidebar(self):
        tk.Label(self.sidebar, text="DASHBOARD", fg="#00ffd5",
                 bg="#1e1e1e", font=("Helvetica", 12, "bold")).pack(pady=30)  # title
        
        menu_items = [
            ("HIDE DATA", self.hide_step_1),     # hide option
            ("EXTRACT DATA", self.extract_screen),  # extract option
            ("AUDIT LOG", self.auth_history)     # log option
        ]
        
        for text, cmd in menu_items:
            tk.Button(self.sidebar, text=text, command=cmd,
                      bg="#2a2a2a", fg="white",
                      bd=0, width=18, height=2,
                      font=("Helvetica", 9, "bold")).pack(pady=10)  # menu button

    def clear_main(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()    # clear screen

    def show_home(self):
        self.clear_main()       # reset screen
        tk.Label(self.main_area, text="STEGANOGRAPHY TOOLKIT",
                 font=("Helvetica", 20, "bold"),
                 fg="#ffffff", bg="#121212").pack(pady=100)  # heading
        tk.Label(self.main_area, text="Advanced Anti-Forensics Analysis Tool",
                 font=("Helvetica", 10),
                 fg="#888888", bg="#121212").pack()  # subtitle

    # --- ENCODING PROCESS ---
    def hide_step_1(self):
        self.clear_main()       # clear area
        tk.Label(self.main_area, text="ENTER SECRET MESSAGE",
                 font=("Helvetica", 14),
                 fg="#00ffd5", bg="#121212").pack(pady=30)  # prompt
        self.msg_input = tk.Text(self.main_area, height=8,
                                 width=50, font=("Consolas", 10))  # text box
        self.msg_input.pack(pady=10)
        tk.Button(self.main_area, text="PROCEED TO ENCRYPTION",
                  command=self.hide_step_2,
                  bg="#00ffd5", fg="black",
                  width=25, height=2).pack(pady=20)  # next button

    def hide_step_2(self):
        self.data_to_hide = self.msg_input.get("1.0", "end").strip()  # get text
        if not self.data_to_hide:
            messagebox.showwarning("Warning", "Secret message cannot be empty!")
            return
        
        messagebox.showinfo("Security Alert",
                            "Applying Encryption Layers to the message...")  
        
        self.clear_main()       # clear screen
        tk.Label(self.main_area, text="PHASE 2: DEFINE CRYPTOGRAPHIC KEY",
                 font=("Helvetica", 14),
                 fg="#00ffd5", bg="#121212").pack(pady=30)  # heading
        tk.Label(self.main_area, text="Enter the password for bit-level locking:",
                 fg="white", bg="#121212").pack()  # instruction
        
        self.key_field = tk.Entry(self.main_area, show="*",
                                  width=30, font=("Arial", 12))  # password box
        self.key_field.pack(pady=15)
        
        tk.Button(self.main_area, text="CHOOSE IMAGE",
                  command=self.hide_final_step,
                  bg="#00ffd5", fg="black",
                  width=25, height=2).pack(pady=20)  # image select

    def hide_final_step(self):
        key = self.key_field.get()   # read key
        if not key:
            messagebox.showwarning("Required", "Security key is mandatory!")
            return
        
        src_path = filedialog.askopenfilename(
            title="Select Image", filetypes=[("PNG", "*.png")])  # input image
        if not src_path:
            return
        
        dest_path = filedialog.asksaveasfilename(
            defaultextension=".png", title="Save Protected File")  # output image
        if not dest_path:
            return

        try:
            encrypted = "".join(
                chr(ord(c) ^ ord(key[i % len(key)]))
                for i, c in enumerate(self.data_to_hide))  # XOR encrypt
            
            bin_data = ''.join(format(ord(i), '08b') for i in encrypted) \
                       + '1111111111111110'  # binary + marker
            
            img = Image.open(src_path).convert('RGB')  # open image
            pixels = img.load()    # pixel access
            
            ptr = 0               # data pointer
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    if ptr < len(bin_data):
                        r, g, b = pixels[x, y]
                        r = (r & ~1) | int(bin_data[ptr])  
                        pixels[x, y] = (r, g, b)
                        ptr += 1
            
            img.save(dest_path)    # save image
            self.history_log.append(
                f"[{datetime.datetime.now().strftime('%H:%M')}] ENCODED: {os.path.basename(dest_path)}")  # log save
            messagebox.showinfo("Success", "Data Hidden Successfully!")
            self.show_home()       # back home
        except Exception as e:
            messagebox.showerror("Error", str(e))  # error show

    # --- DECODING PROCESS ---
    def extract_screen(self):
        self.clear_main()        # clear screen
        tk.Label(self.main_area, text="EXTRACTION & DECRYPTION",
                 font=("Helvetica", 14),
                 fg="#34a853", bg="#121212").pack(pady=30)  # title
        tk.Label(self.main_area, text="Enter the secret key:",
                 fg="white", bg="#121212").pack()  # prompt
        self.ext_key_field = tk.Entry(self.main_area, show="*",
                                      width=30, font=("Arial", 12))  # key input
        self.ext_key_field.pack(pady=15)
        tk.Button(self.main_area, text="DECRYPT IMAGE DATA",
                  command=self.perform_extraction,
                  bg="#34a853", fg="white",
                  width=25, height=2).pack(pady=10)  # decrypt button

    def perform_extraction(self):
        key = self.ext_key_field.get()  # read key
        path = filedialog.askopenfilename(
            filetypes=[("PNG", "*.png")])  # select image
        if not path or not key:
            return
        
        try:
            img = Image.open(path).convert('RGB')  # open image
            pixels = img.load()   # pixel load
            bin_acc = ""          # bit store
            
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    r, g, b = pixels[x, y]
                    bin_acc += str(r & 1)  # read LSB
                    
                    if bin_acc.endswith('1111111111111110'):  
                        bin_acc = bin_acc[:-16]
                        enc_msg = "".join(
                            chr(int(bin_acc[i:i+8], 2))
                            for i in range(0, len(bin_acc), 8))  # binary to text
                        
                        decrypted = "".join(
                            chr(ord(c) ^ ord(key[i % len(key)]))
                            for i, c in enumerate(enc_msg))  # XOR decrypt
                        
                        messagebox.showinfo(
                            "Extracted Data", decrypted)  # show text
                        self.history_log.append(
                            f"[{datetime.datetime.now().strftime('%H:%M')}] DECODED: {os.path.basename(path)}")  # log
                        self.show_home()
                        return
            
            messagebox.showerror("Error", "Invalid key or image.")
        except:
            messagebox.showerror("Error", "Processing Failed.")

    # --- SECURE LOG ---
    def auth_history(self):
        auth_win = tk.Toplevel(self.root)  # popup window
        auth_win.title("Admin Auth")
        auth_win.geometry("300x150")
        tk.Label(auth_win, text="PASSWORD REQUIRED").pack(pady=15)  # label
        p_entry = tk.Entry(auth_win, show="*")  # password box
        p_entry.pack()
        tk.Button(auth_win, text="UNLOCK",
                  bg="#00ffd5",
                  command=lambda: self.show_history(p_entry.get(), auth_win)
                  ).pack(pady=15)  # unlock button

    def show_history(self, pwd, win):
        if pwd == self.admin_pass:  # password check
            win.destroy()
            self.clear_main()
            tk.Label(self.main_area, text="SYSTEM AUDIT LOG",
                     font=("Helvetica", 16, "bold"),
                     fg="#ffaa00", bg="#121212").pack(pady=40)  # title
            
            if not self.history_log:
                tk.Label(self.main_area,
                         text="No operations in current session.",
                         fg="gray", bg="#121212").pack()  # empty log
            
            for entry in self.history_log:
                tk.Label(self.main_area, text=entry,
                         fg="#00ff00", bg="#1e1e1e",
                         width=70, pady=5,
                         anchor="w", padx=20).pack(pady=2)  # log entry
        else:
            messagebox.showerror("Access Denied", "Incorrect Password")  # deny

if __name__ == "__main__":
    root = tk.Tk()               # create window
    app = SecureStegoToolkit(root)  # start app
    root.mainloop()              # run GUI
