from app import app, api_url
from dash.exceptions import PreventUpdate
from dash import dcc, html, ctx, callback
from dash.dependencies import Input, Output, State
from faker import Faker
from google.cloud import storage
import dash_bootstrap_components as dbc
import cv2
import os
import requests
from datetime import datetime

input_size = 4
input_offset = 4


cred = 'focus-surfer-435213-g6.json'

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred


def upload_to_gcp(source_file_name, destination_folder):
    bucket_name = 'face-verification-images'
    destination_blob_name = f'{destination_folder}/{source_file_name}'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


layout = html.Div(style={'background-color': 'Azure', 'height': '100vh'}, children=[
    dbc.Row(children=[
        dbc.Col(children=[
            html.H2('FACE RECOGNITION SYSTEM', style={'textAlign': 'center', 'font-weight': 'bold',
                                                      'color': '#3B1C0A', 'padding-top': '10px', 'font-size': '200%'}),
        ], width=11),
        dbc.Col(dbc.Button(id='logout', children='Logout', n_clicks=None))], justify='center'),
    dbc.Tabs(children=[
        dbc.Tab(label='ENROLLMENT', style={'background-color': 'AliceBlue'}, children=[
            dcc.ConfirmDialog(
                id='enroll-take-picture', submit_n_clicks=0,
                message='Your face will be scanned. Kindly look into the camera and click OK when ready.',
            ),
            dbc.Container(style={'background-color': 'GhostWhite'}, children=[
                dbc.Row([
                    dbc.Col(html.H2("User Registration", className="text-center mb-4"), width=12)
                ]),

                dbc.Row(children=[
                    dbc.Col(children=[
                        dbc.Card([
                            dbc.CardBody(style={'background-color': 'GhostWhite'}, children=[
                                dbc.Label("Username:", html_for="username-input"),
                                dcc.Input(id='enroll-username-input', type='text', placeholder='Enter Username',
                                          className="form-control mb-3"),
                                dbc.Label("Password:", html_for="password-input"),
                                dcc.Input(id='enroll-password-input', type='password', placeholder='Enter Password',
                                          className="form-control mb-3"),
                                dbc.Label("Email:", html_for="email-input"),
                                dcc.Input(id='enroll-email-input', type='email', placeholder='Enter Email',
                                          className="form-control mb-3"),
                                dbc.Label("Access:", html_for="email-input"),
                                dcc.Dropdown(id='enroll-access-type', clearable=False, value=0,
                                             options=[{'value': 1, 'label': 'Admin Access'},
                                                      {'value': 0, 'label': 'No Admin Access'}],
                                             style={'color': 'black'}),
                                html.Br(),
                                dbc.Row(children=[dbc.Col(children=[
                                    dbc.Button("Take Picture", id='enroll-take-pic-btn', color="primary",
                                               className='text-center', n_clicks=0, outline=True, size='md',
                                               style={'padding-left': '45px', 'padding-right': '45px'}), ],
                                    width={'offset': 3}, style={'padding-left': '25px', 'padding-right': '25px'})],
                                    justify="center"),
                                html.Br(),
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Button("Enroll", id='enroll-btn', color="success", n_clicks=0,
                                                   outline=True, className='mt-1', size='md',
                                                   style={'padding-left': '60px', 'padding-right': '60px'}),
                                        width={'offset': 3}, style={'padding-left': '35px', 'padding-right': '35px'})],
                                    justify="center"), ])])], width=4)], justify="center"),
                dbc.Row([
                    dbc.Col(html.Div(id='enroll-output-message', className="mt-4 text-center",
                                     style={'color': 'red', 'text-weight': 'bold'}),
                            width=12)])
            ], fluid=True)]),
        dbc.Tab(label="VERIFICATION", children=[
            dcc.ConfirmDialog(
                id='verify-take-picture', submit_n_clicks=0,
                message='Your face will be scanned. Kindly look into the camera and click OK when ready.',
            ),
            dbc.Container(children=[
                html.Br(),
                dbc.Row(children=[
                    dbc.Col(children=[
                        dbc.Row(dbc.Col(html.Img(id='image-placeholder', src=app.get_asset_url('scan.webp'))),
                                justify='center'),
                        dbc.Row(dbc.Col(dbc.Button('CLICK TO VERIFY', id='verify-btn', color="success", n_clicks=0,
                                                   outline=True, className='mt-1', size='md',
                                                   style={'padding-left': '60px', 'padding-right': '60px'}),
                                        width={'size': 2, 'offset': 1}), justify='center')
                    ], width={'size': 4, 'offset': 4})
                ]),
                dbc.Row([
                    dbc.Col(html.Div(id='verify-output-message', className="mt-4 text-center",
                                     style={'color': 'red', 'text-weight': 'bold'}),
                            width=12)])
            ], fluid=True)
        ]),
        dcc.Tab(label='UNENROLL USER', children=[
dbc.Container(style={'background-color': 'GhostWhite'}, children=[
                dbc.Row([
                    dbc.Col(html.H2("User Registration", className="text-center mb-4"), width=12)
                ]),

                dbc.Row(children=[
                    dbc.Col(children=[
                        dbc.Card([
                            dbc.CardBody(style={'background-color': 'GhostWhite'}, children=[
                                dbc.Label("Username:", html_for="username-input"),
                                dcc.Input(id='unenroll-username-input', type='text', placeholder='Enter Username',
                                          className="form-control mb-3"),
                                dbc.Label("Password:", html_for="password-input"),
                                dcc.Input(id='unenroll-password-input', type='password', placeholder='Enter Password',
                                          className="form-control mb-3"),
                                dbc.Label("Email:", html_for="email-input"),
                                dcc.Input(id='unenroll-email-input', type='email', placeholder='Enter Email',
                                          className="form-control mb-3"),
                                dbc.Label("Access:", html_for="email-input"),
                                dcc.Dropdown(id='unenroll-access-type', clearable=False, value=0,
                                             options=[{'value': 1, 'label': 'Admin Access'},
                                                      {'value': 0, 'label': 'No Admin Access'}],
                                             style={'color': 'black'}),
                                html.Br(),
                                dbc.Row(children=[dbc.Col(children=[
                                    dbc.Button("Take Picture", id='unenroll-take-pic-btn', color="primary",
                                               className='text-center', n_clicks=0, outline=True, size='md',
                                               style={'padding-left': '45px', 'padding-right': '45px'}), ],
                                    width={'offset': 3}, style={'padding-left': '25px', 'padding-right': '25px'})],
                                    justify="center"),
                                html.Br(),
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Button("Unenroll User", id='unenroll-btn', color="success", n_clicks=0,
                                                   outline=True, className='mt-1', size='md',
                                                   style={'padding-left': '60px', 'padding-right': '60px'}),
                                        width={'offset': 3}, style={'padding-left': '35px', 'padding-right': '35px'})],
                                    justify="center"), ])])], width=4)], justify="center"),
                dbc.Row([
                    dbc.Col(html.Div(id='unenroll-output-message', className="mt-4 text-center",
                                     style={'color': 'red', 'text-weight': 'bold'}),
                            width=12)])
            ], fluid=True)
        ]),
    ]),
])


@callback(Output('enroll-take-picture', 'displayed'),
          Output('enroll-take-pic-btn', 'n_clicks'),
          [Input('enroll-take-pic-btn', 'n_clicks')])
def display_confirm(value):
    print('enroll clicked')
    if value:
        return True, 0
    return False, 0


@callback(
    Output('enroll-output-message', 'children', allow_duplicate=True),
    [Input('enroll-take-picture', 'submit_n_clicks')],
    [State('enroll-username-input', 'value')], config_prevent_initial_callbacks=True

)
def scan_face_to_enroll(n_clicks, username):
    if n_clicks > 0:
        print('enroll to take picture clicked')
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            raise FileNotFoundError('Could not take picture.')
        print('about to take picture')
        ret, frame = video_capture.read()
        if not ret:
            raise FileNotFoundError('Could not take picture.')
        print('filefound')
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return "Error: Could not access the camera."
        print('camera found')
        ret, frame = cap.read()

        if ret:
            cv2.imwrite(f"{username}.jpg", frame)

            cap.release()
            print(f'{username}.jpg')
            return f"Image taken successfully!"
        else:
            cap.release()
            return "Error: Could not capture image."

    return ""


@callback(Output('enroll-output-message', 'children'),
          Input('enroll-btn', 'n_clicks'),
          Input('enroll-access-type', 'value'),
          Input('token', 'data'),
          [State('enroll-username-input', 'value'),
           State('enroll-password-input', 'value'),
           State('enroll-email-input', 'value'),]
          )
def enroll_user(n_clicks, is_admin, bearer_token, username, password, email):
    if n_clicks > 0:
        headers = {
            'Authorization': f"Bearer {bearer_token}"
        }
        enroll_url = f"{api_url}/enroll"
        filename = f"{username}.jpg"
        upload_to_gcp(filename, 'enrollment-images')
        try:
            with open(filename, "rb") as image_file:
                files = {
                    "image": (filename, image_file, "image/jpg")
                }
                print('opening filename')
                data = {
                    "username": username,
                    "email": email,
                    "is_admin": is_admin,
                    "password": password
                }
                # print('data created')
                print(data)
                print(files)
                response = requests.post(enroll_url, headers=headers, data=data, files=files)
                print(response.json())
        except FileNotFoundError:
            return f"Error: The file {filename} does not exist."
        # os.remove(filename)
        if response.status_code == 200:
            return f"{response.json()['message']}"
        else:
            return f"Error: {response.status_code}, {response.text}"


@callback(Output('url', 'pathname', allow_duplicate=True),
          Output('token', 'data'),
          Output('logout', 'n_clicks'),
          Input('logout', 'n_clicks'),
          config_prevent_initial_callbacks=True
          )
def log_out(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    if n_clicks:
        return '/', None, None


@callback(Output('verify-take-picture', 'displayed'),
          Output('verify-btn', 'n_clicks'),
          Input('verify-btn', 'n_clicks'))
def verify(n_clicks):
    if n_clicks:
        return True, 0
    return False, 0


@callback(
    Output('verify-output-message', 'children', allow_duplicate=True),
    Output('image-placeholder', 'src'),
    [Input('verify-take-picture', 'submit_n_clicks'),
     Input('token', 'data'), ],
    config_prevent_initial_callbacks=True)
def scan_face_to_verify(n_clicks, access_token):
    if n_clicks > 0:
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            raise FileNotFoundError('Could not take picture.')

        ret, frame = video_capture.read()
        if not ret:
            raise FileNotFoundError('Could not take picture.')

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return "Error: Could not access the camera.", app.get_asset_url('scan.webp')

        ret, frame = cap.read()
        username = Faker().name()
        if ret:
            filename = f"{username}.jpg"
            cv2.imwrite(filename, frame)
            upload_to_gcp(filename, 'verification-images')

            cap.release()
            face_recognition_url = f'{api_url}/face_recognition'

            headers = {
                'Authorization': f'Bearer {access_token}'
            }

            with open(filename, "rb") as image_file:
                files = {
                    "image": (filename, image_file, "image/jpg")
                }
                response = requests.post(face_recognition_url, headers=headers, files=files)
                os.remove(filename)
            print(response.status_code)
            print(response.json())
            cur_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            if response.json().get('recognized') == 1:
                return f"Verified Successfully at {cur_time}.", app.get_asset_url('authenticated.webp')
            elif response.json().get('recognized') == 0:
                return 'Sorry, we could not verify you. Try again or contact the Admin.', app.get_asset_url('scan.webp')
            else:
                return response.json().get('message'), app.get_asset_url('scan.webp')
        else:
            cap.release()
            return "Error: Could not capture image.", app.get_asset_url('scan.webp')

    return "", app.get_asset_url('scan.webp')
