import tkinter
import PIL


def run():
    root = tkinter.Tk()
    root.title('Dragon Quest 1')
    root.geometry('{}x{}'.format(800, 600))

    # Create variables
    status_text = """Solo
Lv: 1
HP: 15
MP: 0
G: 120
E: 0
Str: 5
Agi: 5
Atk: 5
Def: 2"""

    # Create controls
    top_frame = tkinter.Frame(root, bg='red', width=800, height=400)
    bottom_frame = tkinter.Frame(root, bg='green', width=800, height=200)
    left_frame = tkinter.Frame(top_frame, bg='blue', width=200, height=400)
    right_frame = tkinter.Frame(top_frame, bg='yellow', width=600, height=400)
    status_label = tkinter.Label(left_frame, text=status_text, bg='black', fg='white', font='none 18 bold',
                                 relief=tkinter.RIDGE)

    # background_image = PIL.ImageTk.Image.open('resources/background.png')
    # background_image = background_image.resize((600, 400))
    # background_photo_image = PIL.ImageTk.PhotoImage(background_image)
    # background_label = tkinter.Label(right_frame, image=background_photo_image)
    # background_label.pack()

    # enemy_photo_image = PhotoImage(file='resources/DQ_Slime.png')
    # enemy_photo_image = enemy_photo_image.subsample(10)
    # enemy_label = Label(right_frame, image=enemy_photo_image)
    # enemy_label.place(relwidth=1, relheight=1)

    canvas = tkinter.Canvas(right_frame, bg='black', width=600, height=400)
    canvas.pack()

    background_photo_image = tkinter.PhotoImage(file='resources/background.png')
    dimensions = f'image size: {background_photo_image.width()}x{background_photo_image.height()}'
    background_label = tkinter.Label(right_frame, image=background_photo_image, text=dimensions)
    background_label.pack()
    background_photo_image = background_photo_image.subsample(10)
    canvas.create_image(300, 200, image=background_photo_image)

    enemy_photo_image = tkinter.PhotoImage(file='resources/DQ_Slime.png')
    enemy_photo_image = enemy_photo_image.subsample(10)
    canvas.create_image(30, 20, image=enemy_photo_image)

    # Configure grid
    root.grid_rowconfigure(1)
    root.grid_columnconfigure(0)

    # Add controls to grid
    top_frame.grid(row=0)
    bottom_frame.grid(row=1)
    left_frame.grid(row=0, column=0)
    right_frame.grid(row=0, column=1)
    status_label.place(x=0, y=0, relwidth=1, relheight=1)

    root.mainloop()
