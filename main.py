from app import app, api_url
from dash.exceptions import PreventUpdate
from faker import Faker
from dash import dcc, html, ctx, callback
from dash.dependencies import Input, Output, State
from google.cloud import storage
import dash_bootstrap_components as dbc
import cv2
import os
import requests
from datetime import datetime

input_size = 4
input_offset = 4

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


def upload_to_gcp(source_file_name, destination_folder):
    bucket_name = 'face-verification-images'
    destination_blob_name = f'{destination_folder}/{source_file_name}'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


layout = html.Div(style={'height': '100vh'}, children=[
    dbc.Row(children=[
        dbc.Col(children=[
            html.H2('FACE RECOGNITION SYSTEM', style={'textAlign': 'center', 'font-weight': 'bold',
                                                      'color': '#C71585', 'padding-top': '10px', 'font-size': '200%'}),
        ], width=11),
        dbc.Col(dbc.Button(id='logout', children='Logout', n_clicks=None))], justify='center'),
    dbc.Tabs(children=[
        dbc.Tab(label='ENROLLMENT', children=[
            dcc.ConfirmDialog(
                id='enroll-take-picture', submit_n_clicks=0,
                message='Your face will be scanned. Kindly look into the camera and click OK when ready.', ),
            dbc.Container(children=[
                dbc.Row(children=[
                    dbc.Col(style={'text-weight': 'bold'}, children=[
                        dbc.Card(style={'background-image': 'url("/assets/grad.webp"'}, children=[
                            dbc.CardBody(children=[
                                dbc.Label("Name:", html_for="enroll-name-input", style={'color': 'white'}),
                                dcc.Input(id='enroll-name-input', type='text', placeholder='Enter Full Name',
                                          className="form-control mb-3"),
                                dbc.Label("Username:", html_for="enroll-username-input", style={'color': 'white'}),
                                dcc.Input(id='enroll-username-input', type='text', placeholder='Enter Username',
                                          className="form-control mb-3"),
                                dbc.Label("Password:", html_for="enroll-password-input", style={'color': 'white'}),
                                dcc.Input(id='enroll-password-input', type='password', placeholder='Enter Password',
                                          className="form-control mb-3"),
                                dbc.Label("Email:", html_for="enroll-email-input", style={'color': 'white'}),
                                dcc.Input(id='enroll-email-input', type='email', placeholder='Enter Email',
                                          className="form-control mb-3"),
                                dbc.Label("Access:", html_for="enroll-email-input", style={'color': 'white'}),
                                dcc.Dropdown(id='enroll-access-type', clearable=False, value=0,
                                             options=[{'value': 1, 'label': 'Admin Access'},
                                                      {'value': 0, 'label': 'No Admin Access'}],
                                             style={'color': 'black'}),
                                html.Br(),
                                dbc.Row(children=[dbc.Col(children=[
                                    dbc.Button("Take Picture", id='enroll-take-pic-btn', color="warning",
                                               className='text-center', n_clicks=0, outline=True, size='md',
                                               style={'padding-left': '45px', 'padding-right': '45px',
                                                      'text-weight': 'bold'}), ],
                                    width={'offset': 3}, style={'padding-left': '25px', 'padding-right': '25px'})],
                                    justify="center"),
                                html.Br(),
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Button("Enroll", id='enroll-btn', color="light", n_clicks=0,
                                                   outline=True, className='mt-1', size='md',
                                                   style={'padding-left': '60px', 'padding-right': '60px'}),
                                        width={'offset': 3}, style={'padding-left': '35px', 'padding-right': '35px'})],
                                    justify="center"),
                                dbc.Row(children=[
                                    dbc.Col(
                                        dcc.Loading(html.Div(id='enroll-output-message', className="mt-4 text-center",
                                                             style={'color': 'red', 'text-weight': 'bold'}),
                                                    fullscreen=True, type='circle'),
                                        width=12, )])])])], width=4)], justify="center"),
            ], fluid=True, style={'padding-top': '60px'})]),
        dbc.Tab(label="VERIFICATION", children=[
            dcc.ConfirmDialog(
                id='verify-take-picture', submit_n_clicks=0,
                message='Your face will be scanned. Kindly look into the camera and click OK when ready.',
            ),
            dbc.Container(children=[
                dbc.Row(dbc.Col(children=[
                    dbc.Card(style={'background-image': 'url("/assets/ver.png"'}, children=[dbc.CardBody(children=[
                        dbc.Row(children=[
                            dbc.Col(children=[
                                dbc.Row(dbc.Col(html.Img(id='image-placeholder', src=app.get_asset_url('scan.webp'),
                                                         style={'padding-left': '15px', 'padding-right': '15px'})), ),
                                html.Br(),
                                dbc.Row(dbc.Col(dbc.Button("VERIFY", id='verify-btn', color="light", n_clicks=0,
                                                           outline=True, className='mt-1', size='md',
                                                           style={'padding-left': '60px', 'padding-right': '60px',
                                                                  'color': 'red'}), width={'offset': 3},
                                                style={'padding-left': '35px', 'padding-right': '35px'}),
                                        justify='center'),
                                dbc.Row(children=[
                                    dbc.Col(
                                        dcc.Loading(html.Div(id='verify-output-message', className="mt-4 text-center",
                                                             style={'color': 'red', 'text-weight': 'bold'}),
                                                    fullscreen=True, type='circle'))])
                            ], width=12)])])])], width=4), justify='center'),
            ], fluid=True, style={'padding-top': '60px'})
        ]),
        dcc.Tab(label='USER UPDATE & DELETION', children=[
            dbc.Container(children=[
                dbc.Row(children=[
                    dbc.Col(style={'text-weight': 'bold'}, children=[
                        dbc.Card(style={'background-image': 'url("/assets/grad.webp"'}, children=[
                            dbc.CardBody(children=[
                                dbc.Label("Name:", html_for="update-name-input", style={'color': 'white'}),
                                dcc.Input(id='update-name-input', type='text', placeholder='Enter Full Name',
                                          className="form-control mb-3"),
                                dbc.Label("Username:", html_for="update-username-input", style={'color': 'white'}),
                                dcc.Input(id='update-username-input', type='text', placeholder='Enter Username',
                                          className="form-control mb-3"),
                                dbc.Label("Password:", html_for="update-password-input", style={'color': 'white'}),
                                dcc.Input(id='update-password-input', type='password', placeholder='Enter Password',
                                          className="form-control mb-3"),
                                dbc.Label("Email:", html_for="update-email-input", style={'color': 'white'}),
                                dcc.Input(id='update-email-input', type='email', placeholder='Enter Email',
                                          className="form-control mb-3"),
                                html.Br(),
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Button("Update", id='update-btn', color="light", n_clicks=0,
                                                   outline=True, className='mt-1', size='md',
                                                   style={'padding-left': '60px', 'padding-right': '60px'}),
                                        width={'offset': 3}, style={'padding-left': '35px', 'padding-right': '35px'})],
                                    justify="center"),
                                dbc.Row(children=[
                                    dbc.Col(
                                        dcc.Loading(html.Div(id='update-output-message', className="mt-4 text-center",
                                                             style={'color': 'red', 'text-weight': 'bold'}),
                                                    fullscreen=True, type='circle'),
                                        width=12, )])])])], width=4)], justify="center"),
            ], fluid=True, style={'padding-top': '60px'}),
            dbc.Container(children=[
                dbc.Row(children=[
                    dbc.Col(children=[
                        dbc.Card(style={'background-image': 'url("/assets/del_bg.jpg"'}, children=[
                            dbc.CardBody(children=[
                                dbc.Label("Username:", html_for="unenroll-username-input"),
                                dcc.Input(id='unenroll-username-input', type='text', placeholder='Enter Username',
                                          className="form-control mb-3"),
                                html.Br(),
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Button("Delete User", id='unenroll-btn', color="success", n_clicks=0,
                                                   outline=True, className='mt-1', size='md',
                                                   style={'padding-left': '60px', 'padding-right': '60px'}),
                                        width={'offset': 3}, style={'padding-left': '35px', 'padding-right': '35px'})],
                                    justify="center"),
                                dbc.Row(style={'background-color': 'Beige'}, children=[
                                    dbc.Col(
                                        dcc.Loading(html.Div(id='unenroll-output-message', className="mt-4 text-center",
                                                             style={'color': 'red', 'text-weight': 'bold'}),
                                                    type='circle', fullscreen=True), width=12)])
                            ])])], width=4)], justify="center")
            ], fluid=True, style={'padding-top': '20px'}),
        ]),
    ]),
])


@callback(Output('enroll-take-picture', 'displayed'),
          Output('enroll-take-pic-btn', 'n_clicks'),
          [Input('enroll-take-pic-btn', 'n_clicks')])
def display_confirm(value):
    if value:
        return True, 0
    return False, 0


@callback(Output('unenroll-output-message', 'children'),
          Input('unenroll-btn', 'n_clicks'),
          Input('token', 'data'),
          State('unenroll-username-input', 'value'))
def delete_user(n_clicks, bearer_token, username):
    if not n_clicks:
        raise PreventUpdate
    if n_clicks > 0:
        headers = {
            'Authorization': f"Bearer {bearer_token}"
        }
        unenroll_url = f"{api_url}/unenroll"
        data = {'username': username}
        response = requests.delete(unenroll_url, headers=headers, data=data)
        if response.status_code == 200:
            return 'User removed from database successfully'
        else:
            try:
                return f"{response.status_code}, {response.json()['message']}"
            except KeyError:
                return "You are unauthorized to carry out this action."


@callback(Output('update-output-message', 'children'),
          Input('update-btn', 'n_clicks'),
          Input('token', 'data'),
          State('update-username-input', 'value'),
          State('update-name-input', 'value'),
          State('update-password-input', 'value'),
          State('update-email-input', 'value'))
def update_user(n_clicks, bearer_token, username, name, password, email):
    if not n_clicks:
        raise PreventUpdate
    update_url = f"{api_url}/update"
    headers = {
        'Authorization': f"Bearer {bearer_token}"
    }
    data = {
        'username': username,
        'name': name,
        'password': password,
        'email': email
    }
    response = requests.put(update_url, data=data, headers=headers)
    if response.status_code == 200:
        return f"{name.split()[0]}'s data updated successfully."
    else:
        return f"Failed to update data of {name.split()[0]}."


@callback(
    Output('enroll-output-message', 'children', allow_duplicate=True),
    [Input('enroll-take-picture', 'submit_n_clicks')],
    [State('enroll-username-input', 'value')], config_prevent_initial_callbacks=True)
def scan_face_to_enroll(n_clicks, username):
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
            return "Error: Could not access the camera."

        ret, frame = cap.read()

        if ret:
            cv2.imwrite(f"{username}.jpg", frame)

            cap.release()
            return f"Image taken successfully!"
        else:
            cap.release()
            return "Error: Could not capture image."

    return ""


@callback(Output('enroll-output-message', 'children'),
          Output('enroll-name-input', 'value'),
          Output('enroll-email-input', 'value'),
          Output('enroll-password-input', 'value'),
          Output('enroll-username-input', 'value'),
          Input('enroll-btn', 'n_clicks'),
          Input('enroll-access-type', 'value'),
          Input('token', 'data'),
          [State('enroll-name-input', 'value'),
           State('enroll-username-input', 'value'),
           State('enroll-password-input', 'value'),
           State('enroll-email-input', 'value')]
          )
def enroll_user(n_clicks, is_admin, bearer_token, name, username, password, email):
    if not n_clicks:
        raise PreventUpdate
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

                data = {
                    "name": name,
                    "username": username,
                    "email": email,
                    "is_admin": is_admin,
                    "password": password
                }

                response = requests.post(enroll_url, headers=headers, data=data, files=files)
        except FileNotFoundError:
            return f"Error: The file {filename} does not exist.", '', '', '', ''
        os.remove(filename)
        if response.status_code == 200:
            return f"{response.json()['message']}", '', '', '', ''
        else:
            return f"Error: {response.status_code}, {response.text}", '', '', '', ''


@callback(Output('url', 'pathname', allow_duplicate=True),
          Output('token', 'data'),
          Output('logout', 'n_clicks'),
          Input('logout', 'n_clicks'),
          config_prevent_initial_callbacks=True
          )
def log_out(n_clicks):
    if not n_clicks:
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
            cur_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            if response.json().get('recognized') == 1:
                try:
                    return f"Verified Successfully at {cur_time}.", app.get_asset_url('authenticated.webp')
                finally:
                    os.remove(filename)
            elif response.json().get('recognized') == 0:
                try:
                    return 'Sorry, we could not verify you. Try again or contact the Admin.', app.get_asset_url(
                        'scan.webp')
                finally:
                    os.remove(filename)
            else:
                try:
                    return response.json().get('message'), app.get_asset_url('scan.webp')
                finally:
                    os.remove(filename)
        else:
            cap.release()
            return "Error: Could not capture image.", app.get_asset_url('scan.webp')

    return "", app.get_asset_url('scan.webp')
