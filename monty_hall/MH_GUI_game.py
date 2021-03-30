import doors
import MH_game_mechanics as mhgm
from PIL import Image, ImageTk
import random
import tkinter as tk


DEBUG_MODE = False
BG_COL = '#9933FF'
TITLE_BG = 'green' if DEBUG_MODE else BG_COL
FRAME_BG = 'grey' if DEBUG_MODE else BG_COL
FRAME_PADY = 30


WORLD_SIZE = '550x400'

SMPTE_FILE_NAME = 'MontyHall_Images/SMPTE_Color_Bars.png'
LETS_MAKE_A_DEAL = 'MontyHall_Images/lets-make-a-deal2.jpg'
CAR_PRIZE = 'MontyHall_Images/car.png'
GOAT_PRIZE = 'MontyHall_Images/goat.jpg'
MONTY_HALL = 'MontyHall_Images/monty-hall.jpg'


def main():
    """
    Play Let's Make a Deal! as made famous in the Monty Hall problem.
    """
    root = create_world()

    smpte_canvas = run_smpte_intro(root)
    root.after(500, smpte_canvas.pack_forget())

    run_dashboard(root)

    root.mainloop()


def create_world():
    world = tk.Tk()
    world.title("Monty Hall's Game Show")
    world.configure(bg=BG_COL)
    world.geometry(WORLD_SIZE)

    return world


def run_smpte_intro(root):
    smpte_canvas = tk.Canvas(root, width=500, height=375, highlightthickness=0, name="smpte_canvas")
    smpte = tk.PhotoImage(file=SMPTE_FILE_NAME)
    smpte_canvas.create_image(0, 0, anchor="nw", image=smpte)

    smpte_canvas.pack()
    root.update_idletasks()

    return smpte_canvas


def run_dashboard(root):
    welcome_frame = tk.Frame(root, bg=FRAME_BG, name='welcome_img_frame')

    welcome_pic = ImageTk.PhotoImage(Image.open(LETS_MAKE_A_DEAL))
    image_panel = tk.Label(welcome_frame, image=welcome_pic, name="welcome_img_label")
    image_panel.image = welcome_pic     # stores reference so image doesn't get garbage collected

    explainer_button = make_button(welcome_frame, 'Introduction', 'intro_btn', show_instructions, root)

    play_button = make_button(welcome_frame, 'Play', 'play_btn', initiate_game, root)

    image_panel.grid(row=0, column=0)
    explainer_button.grid(row=0, column=0, sticky='SW', padx=30, pady=15)
    play_button.grid(row=0, column=0, sticky='SE', padx=30, pady=15)

    welcome_frame.pack(pady=FRAME_PADY)
    root.update_idletasks()


def show_instructions(root, previous_frame):
    previous_frame.pack_forget()

    instruction_frame = tk.Frame(root, name='scene_frame', bg=FRAME_BG)

    # set title panel
    title_panel, title_var = set_title_panel(instruction_frame, "Welcome to \nLet's Make a Deal!")

    instructions = "You're about to be a contestant on a famous game show! Your host, Monty Hall, will " \
                   "present you with 3 doors. Choose the right door to win a prize. Practice opening doors " \
                   "below..."

    text_panel = set_text_panel(instruction_frame, instructions, "instructions_panel")

    doors_frame, door_patches = set_doors(instruction_frame)

    return_button = make_button(
        instruction_frame,      'Back',             'back_btn',
        return_to_dashboard,    root,               instruction_frame
    )

    title_panel.grid(column=0, row=0)
    text_panel.grid(column=0, row=1)
    doors_frame.grid(column=0, row=2)
    return_button.grid(column=0, row=3)

    instruction_frame.pack()

    # add bindings
    add_bindings(root, door_patches, 'instructions')


def return_to_dashboard(root, previous_frame):
    previous_frame.destroy()
    run_dashboard(root)


def initiate_game(root, previous_frame):
    previous_frame.destroy()
    game = mhgm.Game()
    play_shuffle(root, game)


def play_shuffle(root, game):
    scene, door_patches = construct_doors_scene(root, game, "Are you feeling lucky?")
    shuffle_doors(scene.children['doors_frame'], door_patches)
    play_select(root, game)


def play_select(root, game, message="Select a door to open..."):
    scene, door_patches = construct_doors_scene(root, game, message)

    # add bindings
    add_bindings(root, door_patches, game, ignore=game.query_monty_choices())


def montys_intervention(root, game):
    root.children['scene_frame'].pack_forget()

    mi_frame = tk.Frame(root, bg=FRAME_BG, name='mi_frame')
    mi_frame.pack(pady=FRAME_PADY)

    title = f"You chose Door {game.query_player_choice()}!"
    title_panel, title_var = set_title_panel(mi_frame, title, 'mi_title')

    intervention_canvas = tk.Canvas(
        mi_frame,       width=500,      highlightthickness=0,
        height=300, bg=BG_COL, name="intervention_canvas"
    )
    mh_image = ImageTk.PhotoImage(Image.open(MONTY_HALL))
    intervention_canvas.create_image(0, 0, anchor="nw", image=mh_image)

    title_panel.grid()
    intervention_canvas.grid(pady=20)

    root.update_idletasks()

    root.after(2000, title_var.set(f"Monty has decided to help you out..."))
    root.update_idletasks()

    root.after(2000, title_var.set(f"He opens Door {game.query_monty_choices()[0]}, to reveal a goat!"))
    root.update_idletasks()

    root.after(3000, mi_frame.forget())


def final_reveal(root, game):
    root.children['scene_frame'].pack_forget()

    fr_frame = tk.Frame(root, bg=FRAME_BG, name='fr_frame')
    fr_frame.pack(pady=FRAME_PADY)

    player_won = game.check_player_won()
    prize = "beautiful car" if player_won else "hideous goat"
    title = f"Congratulations, you won this {prize}!"
    title_panel, title_var = set_title_panel(fr_frame, title, 'fr_title')

    prize_canvas = tk.Canvas(
        fr_frame, width=500, highlightthickness=0,
        height=200, bg=BG_COL, name="fr_canvas"
    )

    prize_image = (
        tk.PhotoImage(file=CAR_PRIZE) if player_won else
        ImageTk.PhotoImage(Image.open(GOAT_PRIZE))
    )

    prize_canvas.create_image(0, 1, anchor="nw", image=prize_image)
    prize_canvas.image = prize_image

    replay_btn = make_button(fr_frame, 'Play again', 'replay_btn', initiate_game, root)
    quit_btn = make_button(fr_frame, 'Quit', 'quit_btn', quit_game, root)

    title_panel.grid(row=0, column=0)
    prize_canvas.grid(row=1, column=0, pady=10)
    replay_btn.grid(row=2, column=0, sticky='NW', padx=30, pady=15)
    quit_btn.grid(row=2, column=0, sticky='NE', padx=30, pady=15)

    root.update_idletasks()


def construct_doors_scene(root, game, title_message):
    scene = tk.Frame(root, name='scene_frame', bg=FRAME_BG)

    # set title panel
    title_panel, title_var = set_title_panel(scene, title_message)

    # set doors panel
    doors_frame, door_patches = set_doors(scene, game)

    title_panel.grid(column=0, row=0)
    doors_frame.grid(column=0, row=1)

    scene.pack(pady=30)

    # set door params
    montys_choices = game.query_monty_choices()
    players_choice = game.query_player_choice()

    if montys_choices:
        for door_num in door_patches.keys():
            if door_num in montys_choices:
                door_patches[door_num].open_door(prize_reveal=True)
            else:
                if door_num == players_choice:
                    door_patches[door_num].update_door_mark('Stick!')
                else:
                    door_patches[door_num].update_door_mark('Twist!')

    root.update_idletasks()

    return scene, door_patches


def set_title_panel(frame, title, name="title_panel"):
    text = tk.StringVar()
    text.set(title)
    panel = tk.Label(
        frame,              textvariable=text,          bg=TITLE_BG,
        fg='black',         font="Courier 23",          name=name,
        height=2,           anchor='n',                 wraplength=500
    )

    return panel, text


def set_text_panel(frame, message, name='text_panel'):
    return tk.Label(
        frame,              text=message,           bg=TITLE_BG,
        fg='black',         relief='flat',          font="Courier 11",
        justify='left',     wraplength=500,         name=name
    )


def make_button(frame, text, name, function, *args):
    return tk.Button(
        frame,      text=text,            width=15,
        name = name,
        command=lambda x=args[0], y=frame if len(args) < 2 else args[1]: function(x, y)
    )


def set_doors(frame, game='instructions'):
    doors_frame = tk.Frame(frame, bg=FRAME_BG, width=400, height=200, name="doors_frame")
    door_patches = dict()
    door_nums = (1, 2, 3) if game == 'instructions' else game.doors.keys()

    for door_num in door_nums:
        prize = False if game == 'instructions' else game.check_prize(door_num)
        door_patches[door_num] = doors.Door(doors_frame, door_num, 0, door_num, prize)

    return doors_frame, door_patches


def shuffle_doors(frame, patches):
    for i in range(10):
        rand = random.choice(list(patches.keys()))

        frame.after(100, patches[rand].toggle_shuffle_colour())
        frame.update_idletasks()

        frame.after(100, patches[rand].toggle_shuffle_colour())
        frame.update_idletasks()


def add_bindings(root, door_patches, game, ignore=None):
    if not ignore:
        ignore = []

    for door in door_patches:
        if door_patches[door].door_num not in ignore:
            door_patches[door].patch.bind('<Enter>', lambda event, d=door_patches[door]: d.highlight_select())
            door_patches[door].patch.bind('<Leave>', lambda event, d=door_patches[door]: d.highlight_deselect())
            door_patches[door].patch.bind(
                '<Button-1>',
                lambda event, w=root, x=door, y=door_patches, z=game: on_click_door(w, x, y, z)
            )

    root.update_idletasks()


def on_click_door(root, door, door_patches, game):
    if game == 'instructions':
        door_patches[door].toggle_open(prize_reveal=False)
    else:
        remove_bindings(root, door_patches)
        if game.query_player_choice():
            game.update_player_choice(door_patches[door].door_num)
            door_patches[door].toggle_open(prize_reveal=True)

            root.after(2000, final_reveal(root, game))

        else:
            game.update_player_choice(door_patches[door].door_num)

            available = game.get_selectable_doors("prize", "chosen")
            game.update_monty_choice(available)

            montys_intervention(root, game)

            play_select(root, game, "Now, would you like to \nstick or twist?")

    root.update_idletasks()


def remove_bindings(root, door_patches, ignore=None):
    if not ignore:
        ignore = []

    for door in door_patches.keys():
        if door not in ignore:
            door_patches[door].patch.unbind('<Enter>')
            door_patches[door].patch.unbind('<Leave>')
            door_patches[door].patch.unbind('<Button-1>')

    root.update_idletasks()


def quit_game(root, frame):
    root.destroy()


if __name__ == '__main__':
    main()