import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Fungsi untuk membuat koneksi ke database MySQL
def connect_db():
    return mysql.connector.connect(
        host='localhost',  
        user='root',   
        password='',  
        database='rental.db'  
    )

# Fungsi untuk membuat tabel motor jika belum ada
def create_table():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS motors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            brand VARCHAR(255) NOT NULL,
            type VARCHAR(255) NOT NULL,
            year INT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

# Fungsi untuk menambahkan motor ke database
def add_motor(brand, type, year):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO motors (brand, type, year)
        VALUES (%s, %s, %s)
    ''', (brand, type, year))
    connection.commit()
    connection.close()

# Fungsi untuk menampilkan semua motor
def view_motors():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM motors')
    motors = cursor.fetchall()
    connection.close()
    return motors

# Fungsi untuk mengupdate motor di database
def update_motor(motor_id, brand, type, year):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE motors
        SET brand = %s, type = %s, year = %s
        WHERE id = %s
    ''', (brand, type, year, motor_id))
    connection.commit()
    connection.close()

# Fungsi untuk menghapus motor dari database
def delete_motor(motor_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM motors WHERE id = %s', (motor_id,))
    connection.commit()
    connection.close()

# Fungsi utama untuk menampilkan GUI
def main():
    create_table()

    # Mendefinisikan variabel global untuk entry fields
    global brand_entry, type_entry, year_entry, id_entry

    def add_motor_gui():
        def add_motor_to_db():
            brand = brand_entry.get()
            type = type_entry.get()
            year = int(year_entry.get())
            add_motor(brand, type, year)
            messagebox.showinfo("Info", "Motor berhasil ditambahkan!")
            add_motor_window.destroy()

        add_motor_window = tk.Toplevel(root)
        add_motor_window.title("Tambah Motor")

        brand_label = tk.Label(add_motor_window, text="Merk motor:")
        brand_label.pack()
        brand_entry = tk.Entry(add_motor_window)
        brand_entry.pack()

        type_label = tk.Label(add_motor_window, text="Tipe motor:")
        type_label.pack()
        type_entry = tk.Entry(add_motor_window)
        type_entry.pack()

        year_label = tk.Label(add_motor_window, text="Tahun produksi:")
        year_label.pack()
        year_entry = tk.Entry(add_motor_window)
        year_entry.pack()

        add_button = tk.Button(add_motor_window, text="Tambah Motor", command=add_motor_to_db)
        add_button.pack()

    def view_motors_gui():
        motors = view_motors()

        view_window = tk.Toplevel()
        view_window.title("Daftar Motor")

        scrollbar = tk.Scrollbar(view_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        motor_listbox = tk.Listbox(view_window, yscrollcommand=scrollbar.set, width=50, height=10)
        motor_listbox.pack(padx=10, pady=10)

        scrollbar.config(command=motor_listbox.yview)

        if not motors:
            motor_listbox.insert(tk.END, "Belum ada motor dalam database.")
        else:
            motor_listbox.insert(tk.END, "==== Daftar Motor ====")
            for motor in motors:
                motor_info = f"ID: {motor[0]}, Merk: {motor[1]}, Tipe: {motor[2]}, Tahun: {motor[3]}"
                motor_listbox.insert(tk.END, motor_info)

    def update_motor_gui():
        def update_motor_to_db():
            motor_id = int(id_entry.get())
            brand = brand_entry.get()
            type = type_entry.get()
            year = int(year_entry.get())
            update_motor(motor_id, brand, type, year)
            messagebox.showinfo("Info", "Motor berhasil diupdate!")
            update_motor_window.destroy()

        update_motor_window = tk.Toplevel(root)
        update_motor_window.title("Update Motor")

        id_label = tk.Label(update_motor_window, text="ID Motor:")
        id_label.pack()
        id_entry = tk.Entry(update_motor_window)
        id_entry.pack()

        brand_label = tk.Label(update_motor_window, text="Merk motor:")
        brand_label.pack()
        brand_entry = tk.Entry(update_motor_window)
        brand_entry.pack()

        type_label = tk.Label(update_motor_window, text="Tipe motor:")
        type_label.pack()
        type_entry = tk.Entry(update_motor_window)
        type_entry.pack()

        year_label = tk.Label(update_motor_window, text="Tahun produksi:")
        year_label.pack()
        year_entry = tk.Entry(update_motor_window)
        year_entry.pack()

        update_button = tk.Button(update_motor_window, text="Update Motor", command=update_motor_to_db)
        update_button.pack()

    def delete_motor_gui():
        def delete_motor_from_db():
            motor_id = int(id_entry.get())
            delete_motor(motor_id)
            messagebox.showinfo("Info", "Motor berhasil dihapus!")
            delete_motor_window.destroy()

        delete_motor_window = tk.Toplevel(root)
        delete_motor_window.title("Hapus Motor")

        id_label = tk.Label(delete_motor_window, text="ID Motor:")
        id_label.pack()
        id_entry = tk.Entry(delete_motor_window)
        id_entry.pack()

        delete_button = tk.Button(delete_motor_window, text="Hapus Motor", command=delete_motor_from_db)
        delete_button.pack()

    root = tk.Tk()
    root.title("Sistem Persewaan Motor")
    root.geometry("400x300")  # Ukuran jendela utama

    menu_frame = tk.Frame(root, padx=20, pady=20, bg="#00FFFF")  # Warna latar belakang frame
    menu_frame.pack(fill=tk.BOTH, expand=True)

    label = tk.Label(root, text="Menu Utama", font=("Arial", 20), fg="#333")  # Warna teks judul
    label.pack(pady=10)

    add_motor_button = tk.Button(menu_frame, text="Tambah Motor", width=20, command=add_motor_gui)
    add_motor_button.pack(pady=10)

    view_motor_button = tk.Button(menu_frame, text="Lihat Motor", width=20, command=view_motors_gui)
    view_motor_button.pack(pady=10)

    update_motor_button = tk.Button(menu_frame, text="Update Motor", width=20, command=update_motor_gui)
    update_motor_button.pack(pady=10)

    delete_motor_button = tk.Button(menu_frame, text="Hapus Motor", width=20, command=delete_motor_gui)
    delete_motor_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()