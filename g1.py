import customtkinter

customtkinter.set_appearance_mode('dark')

root = customtkinter.CTk()
root.minsize(400,300)
root.title("DnD Image Resizar")

header_label = customtkinter.CTkLabel(master=root,
                                      text='Add image to resize',
                                      font=(None,24))
header_label.pack(pady=20)

name_entry = customtkinter.CTkEntry(master=root, 
                                    placeholder_text="Enter Height")
name_entry.pack(pady=10)

name_entry2 = customtkinter.CTkEntry(master=root, 
                                    placeholder_text="Enter Width")
name_entry2.pack(pady=10)

root.mainloop()