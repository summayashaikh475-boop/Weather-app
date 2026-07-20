# import tkinter as tk

# root = tk.Tk()
# root.title("Weather App")
# root.geometry("400x400")

# root.mainloop()



import tkinter as tk
def test():
    text = city_entry.get()
    result_label.config(text=f"You entered: {text}")

root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")
city_entry = tk.Entry(root, width=25)
city_entry.pack(pady=10)
btn = tk.Button(root, text="Test Button", command=test)
btn.pack(pady=10)
result_label = tk.Label(root, text="")
result_label.pack(pady=20)

root.mainloop()

    