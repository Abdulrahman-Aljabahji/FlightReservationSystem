import tkinter as tk
from tkinter import messagebox

class PaymentWindow:
    def __init__(self, on_payment_success):
        self.on_payment_success = on_payment_success
        self.window = tk.Toplevel()
        self.window.title("Payment Details")
        self.build_ui()

    def build_ui(self):
        tk.Label(self.window, text="Cardholder Name").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.window)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.window, text="Card Number").grid(row=1, column=0)
        self.card_entry = tk.Entry(self.window)
        self.card_entry.grid(row=1, column=1)

        tk.Label(self.window, text="Expiry Date (MM/YY)").grid(row=2, column=0)
        self.expiry_entry = tk.Entry(self.window)
        self.expiry_entry.grid(row=2, column=1)

        tk.Label(self.window, text="CVV").grid(row=3, column=0)
        self.cvv_entry = tk.Entry(self.window, show="*")
        self.cvv_entry.grid(row=3, column=1)

        tk.Button(self.window, text="Pay", command=self.validate_and_pay).grid(row=4, columnspan=2, pady=10)
        tk.Button(self.window, text="Cancel", command=self.window.destroy).grid(row=5, columnspan=2, pady=5)

    def validate_and_pay(self):
        if not self.name_entry.get().strip() or not self.card_entry.get().strip():
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        self.window.destroy()
        self.on_payment_success()  # Call back to reserve logic
