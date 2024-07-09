import PySimpleGUI as sg


def main_menu_layout(user) :
    return [
        [sg.Text("You are logged in as "+user)],
        [sg.Text("")],
        [sg.Text("Please choose from the following options what you would like to do.")],
        [sg.Radio(f"Fetch top 2000 Military Scores", 1)],
        [sg.Radio(f'Refresh local map', 1)    ],
        [sg.Radio(f'Search Island', 1)    ],
        [sg.Radio(f'Ship Building', 1)    ],
        [sg.Radio(f'Check Attacks', 1)    ],
        [sg.Button('Ok'), sg.Button('Cancel')] 
    ]

fetch_ms_layout = [
    [sg.Text("Fetching Military scores...")],
    [sg.ProgressBar(2000, orientation='h', size=(20,20), key='fetching_progress')]
]

refresh_map_layout = [
    [sg.Text("Refreshing local map...")],
    [sg.ProgressBar(25, orientation='h', size=(20,20), key='map_progress')]
]

def create_island_search_layout(trade_goods, miracles, xcoord_max, xcoord_min, ycoord_max, ycoord_min, citymax, citymin, toggle_btn_off):
    return [
        [sg.Combo(trade_goods, default_value="none",enable_events=True,s=(20,5),k='goods_combo')],
        [sg.Checkbox(miracles[i],key=miracles[i]) for i in range(0,2)],
        [sg.Checkbox(miracles[i],key=miracles[i]) for i in range(2,5)],
        [sg.Checkbox(miracles[i],key=miracles[i]) for i in range(5,8)],
        [sg.Text("X coordinate min and max"), sg.Slider((1,xcoord_max),default_value=xcoord_min, orientation='h', s=(10,15),k='xmin_slider'), sg.Slider((xcoord_min,100),default_value=xcoord_max, orientation='h', s=(10,15),k='xmax_slider')],
        [sg.Text("Y coordinate min and max"), sg.Slider((1,ycoord_max),default_value=ycoord_min, orientation='h', s=(10,15),k='ymin_slider'), sg.Slider((ycoord_min,100),default_value=ycoord_max, orientation='h', s=(10,15),k='ymax_slider')],
        [sg.Text("Minimum and maximum number of cities"), sg.Slider((0,citymax),default_value=citymin, orientation='h', s=(10,15),k='citymin_slider'),sg.Slider((citymin,17),default_value=citymax, orientation='h', s=(10,15),k='citymax_slider')],
        [sg.Text("Show only ally cities"), sg.Button(image_data=toggle_btn_off, key='-TOGGLE-GRAPHIC-', button_color=(sg.theme_background_color(), sg.theme_background_color()),border_width=0, metadata=False)],
        [sg.Button('Ok'), sg.Button('Back')] 
    ]

island_results_layout = [
    [sg.Text("Island Name, Miracle, Trade Good, Number of cities")],
    [sg.Multiline(size=(50,15),k='island_res_ml')]
]

ship_cook_layout = [
    [sg.Text("Ship Building Helper Thingy")],
    [sg.Table([[1]],num_rows=3)]
]

check_attacks_layout = [
    [sg.Text("Attacks to Ally")],
    [sg.Table([[1]],num_rows=3)]
]

def create_main_layout(trade_goods, miracles, xcoord_max, xcoord_min, ycoord_max, ycoord_min, citymax, citymin, toggle_btn_off,user):
    return  [
        [sg.Column(main_menu_layout(user),visible=True,key='main_menu'),
        sg.Column(fetch_ms_layout,visible=False, key='fetch_ms'),
        sg.Column(refresh_map_layout, visible=False, key='refresh_map'),
        sg.Column(create_island_search_layout(trade_goods, miracles, xcoord_max, xcoord_min, ycoord_max, ycoord_min, citymax, citymin, toggle_btn_off), visible=False, key='island_search'),
        sg.Column(island_results_layout, visible=False, key='island_results'),
        sg.Column(ship_cook_layout, visible=False, key='ship_cook'),
        sg.Column(check_attacks_layout, visible=False, key='check_attacks'),
        ]
    ]
   

modeselect_layout  = [  
    [sg.Text('Select authentication mode:')],
    [sg.Radio(f'Cookie', 1)],
    [sg.Radio(f'Login with email and password (BETA)', 1)    ],
    [sg.Button('Select'), sg.Button('Cancel')]  
]

cookie_layout = [
    [sg.Text("Please provide a valid 'ikariam' cookie:"), sg.InputText()],
    [sg.Button('Ok'), sg.Button('Cancel')]  
]

email_layout = [
    [sg.Text("Email:"), sg.InputText()],
    [sg.Text("Password:"), sg.InputText()],
    [sg.Button('Ok'), sg.Button('Cancel')]  
]

w84auth_layout = [
    [sg.Text("Authenticating, Please wait...")]
]

login_layout = [
    [sg.Column(modeselect_layout,visible=True, key="login"),
     sg.Column(cookie_layout,visible=False, key="cookie"),
     sg.Column(email_layout,visible=False, key="email"),
     sg.Column(w84auth_layout,visible=False, key="w84auth")]
]


def print_island_res(i,window):
    sg.cprint_set_output_destination(window,'island_res_ml')
    sg.cprint(i[0],i[1],i[2],i[5],sep=", ")