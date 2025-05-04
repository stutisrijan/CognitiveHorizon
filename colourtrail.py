import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from fpdf import FPDF
import smtplib
from email.message import EmailMessage

from level1 import ColorTrailsLevel1
from level2 import ColorTrailsLevel2

class ColorTrailsGameMain:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Trails Game")
        self.background_image = None
        self.level1_img = None
        self.level2_img = None
        self.canvas = None
        self.init_ui()

    def init_ui(self):
        # Load and display background
        bg_image_path = os.path.join("images", "background.png")
        bg_image = Image.open(bg_image_path)
        self.background_image = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(self.root, width=self.background_image.width(), height=self.background_image.height(), highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        center_x = self.background_image.width() // 2
        start_y = 140

        title = tk.Label(self.root, text="Color Trails Game", font=("Arial", 26, "bold"), bg="white", fg="#333")
        self.canvas.create_window(center_x, start_y - 70, window=title)

        # Load level images
        self.level1_img = ImageTk.PhotoImage(Image.open(os.path.join("images", "level1.png")).resize((180, 60)))
        self.level2_img = ImageTk.PhotoImage(Image.open(os.path.join("images", "LEVEL2.png")).resize((180, 60)))

        level1_button = tk.Button(self.root, image=self.level1_img, borderwidth=0, command=self.start_level1, cursor="hand2")
        level2_button = tk.Button(self.root, image=self.level2_img, borderwidth=0, command=self.start_level2, cursor="hand2")

        self.canvas.create_window(center_x, start_y + 10, window=level1_button)
        self.canvas.create_window(center_x, start_y + 90, window=level2_button)

        report_button = tk.Button(self.root, text="Generate Report", font=("Arial", 12), width=18, bg="#4CAF50", fg="white", command=self.generate_report, cursor="hand2")
        email_button = tk.Button(self.root, text="Send Report via Email", font=("Arial", 12), width=20, bg="#2196F3", fg="white", command=self.send_report_email, cursor="hand2")

        self.canvas.create_window(center_x, start_y + 170, window=report_button)
        self.canvas.create_window(center_x, start_y + 240, window=email_button)

    def start_level1(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        ColorTrailsLevel1(self.root, lambda: self.return_to_main())

    def start_level2(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        ColorTrailsLevel2(self.root, lambda: self.return_to_main())

    def return_to_main(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.init_ui()

    def generate_report(self):
        report_dir = "reports"
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, "game_report.pdf")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Color Trails Game Report", ln=True, align='C')
        pdf.ln(10)

        pdf.cell(0, 10, txt="Summary:", ln=True)
        pdf.cell(0, 10, txt=" - Level 1 Completed: Yes", ln=True)
        pdf.cell(0, 10, txt=" - Level 2 Completed: Yes", ln=True)
        pdf.cell(0, 10, txt=" - Total Attempts: 5", ln=True)
        pdf.cell(0, 10, txt=" - Tips: Focus on pattern speed and visual memory.", ln=True)
        pdf.ln(10)
        pdf.cell(0, 10, txt="Efficiency Score: 85%", ln=True)

        pdf.output(report_path)
        messagebox.showinfo("Report Generated", f"Report saved at {report_path}")

    def send_report_email(self):
        report_path = "reports/game_report.pdf"
        if not os.path.exists(report_path):
            messagebox.showerror("Error", "Generate the report before sending.")
            return

        sender_email = "deepanshusingak3004@gmail.com"
        receiver_email = "deepanshusinghal509@gmail.com"
        password = "kogjezqdcrxpnxrr"

        msg = EmailMessage()
        msg['Subject'] = "Color Trails Game Report"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.set_content("Please find attached the Color Trails Game Report.")

        with open(report_path, "rb") as f:
            report_data = f.read()
            msg.add_attachment(report_data, maintype="application", subtype="pdf", filename="game_report.pdf")

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.send_message(msg)
            messagebox.showinfo("Email Sent", "Report sent successfully!")
        except Exception as e:
            messagebox.showerror("Email Error", f"Failed to send email: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorTrailsGameMain(root)
    root.mainloop()
