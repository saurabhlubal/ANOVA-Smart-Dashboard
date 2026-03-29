import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

root = tk.Tk()
root.title("ANOVA Smart Dashboard")
root.geometry("950x700")
root.configure(bg="#eef2f3")

groups = []
names = []
entries = []

# ---------- HEADER ----------
header = tk.Label(root, text="📊 ANOVA SMART ANALYSIS DASHBOARD",
                  font=("Helvetica", 18, "bold"),
                  bg="#4a90e2", fg="white", pady=10)
header.pack(fill="x")

# ---------- CREATE INPUT ----------
def create_fields():
    try:
        num = int(num_groups_entry.get())
    except:
        messagebox.showerror("Error", "Enter valid number")
        return
    
    for widget in frame_inputs.winfo_children():
        widget.destroy()
    
    entries.clear()
    
    for i in range(num):
        tk.Label(frame_inputs, text=f"Group {i+1}", bg="#eef2f3").grid(row=i, column=0)
        
        name_entry = tk.Entry(frame_inputs)
        name_entry.grid(row=i, column=1)
        
        values_entry = tk.Entry(frame_inputs, width=30)
        values_entry.grid(row=i, column=2)
        
        entries.append((name_entry, values_entry))

# ---------- LOAD DATA ----------
def load_data():
    groups.clear()
    names.clear()
    
    try:
        for name_entry, values_entry in entries:
            name = name_entry.get()
            values = list(map(float, values_entry.get().split()))
            
            names.append(name)
            groups.append(values)
            
        messagebox.showinfo("Success", "✅ Data Loaded Successfully!")
    except:
        messagebox.showerror("Error", "Invalid input")

# ---------- SHOW STATS ----------
def show_stats():
    if not groups:
        messagebox.showerror("Error", "Load data first")
        return
    
    for row in tree.get_children():
        tree.delete(row)
    
    for i, g in enumerate(groups):
        tree.insert("", "end", values=(
            names[i],
            f"{np.mean(g):.2f}",
            f"{np.std(g):.2f}",
            min(g),
            max(g)
        ))

# ---------- GRAPHS ----------
def show_graphs():
    if not groups:
        messagebox.showerror("Error", "Load data first")
        return
    
    means = [np.mean(g) for g in groups]
    
    # 🎯 CURVED DISTRIBUTION (KDE)
    plt.figure(figsize=(8,4))
    for i, g in enumerate(groups):
        sns.kdeplot(g, label=names[i], fill=True)
    
    plt.title("📈 Data Distribution Curve")
    plt.legend()
    plt.show()
    
    # Box Plot
    plt.figure(figsize=(8,4))
    plt.boxplot(groups, labels=names)
    plt.title("📦 Box Plot Comparison")
    plt.show()
    
    # Bar Graph
    plt.figure(figsize=(8,4))
    bars = plt.bar(names, means)
    
    for i, bar in enumerate(bars):
        plt.text(bar.get_x()+bar.get_width()/2,
                 bar.get_height(),
                 f"{means[i]:.2f}",
                 ha='center')
    
    plt.title("📊 Mean Comparison")
    plt.show()

# ---------- FINAL REPORT ----------
def final_report():
    if not groups:
        messagebox.showerror("Error", "Load data first")
        return
    
    f_stat, p_value = stats.f_oneway(*groups)
    means = [np.mean(g) for g in groups]
    stds = [np.std(g) for g in groups]
    
    report.delete(1.0, tk.END)
    
    report.insert(tk.END, "===== FINAL REPORT =====\n\n")
    report.insert(tk.END, f"F-value: {f_stat:.4f}\n")
    report.insert(tk.END, f"P-value: {p_value:.6f}\n\n")
    
    if p_value < 0.05:
        report.insert(tk.END, "✔ Significant difference exists.\n")
    else:
        report.insert(tk.END, "✖ No significant difference.\n")
    
    max_i = np.argmax(means)
    min_i = np.argmin(means)
    best_consistent = np.argmin(stds)
    
    report.insert(tk.END, "\n🏆 Best Group: " + names[max_i] + "\n")
    report.insert(tk.END, "📉 Lowest Group: " + names[min_i] + "\n")
    report.insert(tk.END, "📊 Most Consistent: " + names[best_consistent] + "\n\n")
    
    report.insert(tk.END,
        "Description:\nThis tool performs ANOVA to compare multiple groups,\n"
        "visualizes distributions, and generates insights for decision-making."
    )

# ---------- UI ----------
top_frame = tk.Frame(root, bg="#eef2f3")
top_frame.pack(pady=10)

tk.Label(top_frame, text="Number of Groups:", bg="#eef2f3").grid(row=0, column=0)
num_groups_entry = tk.Entry(top_frame)
num_groups_entry.grid(row=0, column=1)

tk.Button(top_frame, text="➕ Create Fields", command=create_fields,
          bg="#6fcf97", width=15).grid(row=0, column=2, padx=10)

frame_inputs = tk.Frame(root, bg="#eef2f3")
frame_inputs.pack(pady=10)

# Buttons
btn_frame = tk.Frame(root, bg="#eef2f3")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="📥 Load Data", command=load_data,
          bg="#56ccf2", width=15).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="📊 Show Stats", command=show_stats,
          bg="#bbdefb", width=15).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="📈 Graphs", command=show_graphs,
          bg="#d1c4e9", width=15).grid(row=0, column=2, padx=5)

tk.Button(btn_frame, text="📄 Final Report", command=final_report,
          bg="#f8bbd0", width=15).grid(row=0, column=3, padx=5)

# Table
columns = ("Group", "Mean", "Std Dev", "Min", "Max")
tree = ttk.Treeview(root, columns=columns, show="headings", height=6)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(pady=10)

# Report box
report = tk.Text(root, height=10, width=100)
report.pack(pady=10)

root.mainloop()