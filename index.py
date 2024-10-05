from app import app
from dash import dcc, html, ctx, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import login_page as login
import main

# Define the layout that switches between pages
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='token', data=0),
    dbc.Row(children=[
        dbc.Col(html.H5([html.I(className='fa fa-copyright'), ' Group 1 2024'], style={'padding-top': '5px'}),
                width={"size": 2, 'offset': 10})])])


# Update page layout based on URL
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
              Input('token', 'data'))
def display_page(pathname, token):
    if pathname == '/' or not token:
        return login.layout  # Show login page if not authenticated
    elif pathname == '/main' and token:
        return main.layout  # Main page after successful login
    else:
        return '404: Page not found'


if __name__ == '__main__':
    app.run_server(debug=True)

# import requests
#
# from flask import request
# import dash_bootstrap_components as dbc
# import dash_auth
# import cv2
# import os
# import requests
# import time
#
# input_size = 4
# input_offset = 4
#
# api_url = 'http://127.0.0.1:8000'
#
# token_url = f'{api_url}/token'
#
# auth_data = {
#     'username': 'user1',
#     'password': 'user1'
# }
#
# token_response = requests.post(token_url, data=auth_data)
# if token_response.status_code == 200:
#     bearer_token = token_response.json().get('access_token')
#     print(bearer_token)
#
# app.layout = html.Div(style={'background-color': 'Azure', 'height': '100vh'}, children=[
#     html.H2('FACE RECOGNITION SYSTEM',
#             style={'textAlign': 'center', 'font-weight': 'bold', 'color': '#3B1C0A', 'padding-top': '10px',
#                    'font-size': '200%'}),
#     dbc.Tabs(children=[
#         dbc.Tab(label='ENROLLMENT', style={'background-color': 'AliceBlue'}, children=[
#             dcc.ConfirmDialog(
#                 id='take-picture', submit_n_clicks=0,
#                 message='Your face will be scanned. Kindly look into the camera and click OK when ready.',
#             ),
#             dbc.Container(style={'background-color': 'GhostWhite'}, children=[
#                 dbc.Row([
#                     dbc.Col(html.H2("User Registration", className="text-center mb-4"), width=12)
#                 ]),
#
#                 dbc.Row(children=[
#                     dbc.Col(children=[
#                         dbc.Card([
#                             dbc.CardBody(style={'background-color': 'GhostWhite'}, children=[
#                                 dbc.Label("Username:", html_for="username-input"),
#                                 dcc.Input(id='username-input', type='text', placeholder='Enter Username',
#                                           className="form-control mb-3"),
#                                 dbc.Label("Password:", html_for="password-input"),
#                                 dcc.Input(id='password-input', type='password', placeholder='Enter Password',
#                                           className="form-control mb-3"),
#                                 dbc.Label("Email:", html_for="email-input"),
#                                 dcc.Input(id='email-input', type='email', placeholder='Enter Email',
#                                           className="form-control mb-3"),
#                                 dbc.Label("Access:", html_for="email-input"),
#                                 dcc.Dropdown(id='access-type', clearable=False, value=0,
#                                              options=[{'value': 1, 'label': 'Admin Access'},
#                                                       {'value': 0, 'label': 'No Admin Access'}],
#                                              style={'color': 'black'}),
#                                 html.Br(),
#                                 dbc.Row(children=[dbc.Col(children=[
#                                     dbc.Button("Take Picture", id='take-pic-btn', color="primary",
#                                                className='text-center', n_clicks=0, outline=True, size='md',
#                                                style={'padding-left': '45px', 'padding-right': '45px'}), ],
#                                     width={'offset': 3}, style={'padding-left': '25px', 'padding-right': '25px'})],
#                                     justify="center"),
#                                 html.Br(),
#                                 dbc.Row([
#                                     dbc.Col(
#                                         dbc.Button("Enroll", id='enroll-btn', color="success", n_clicks=0,
#                                                    outline=True, className='mt-1', size='md',
#                                                    style={'padding-left': '60px', 'padding-right': '60px'}),
#                                         width={'offset': 3}, style={'padding-left': '35px', 'padding-right': '35px'})],
#                                     justify="center"), ])])], width=4)], justify="center"),
#                 dbc.Row([
#                     dbc.Col(html.Div(id='output-message', className="mt-4 text-center",
#                                      style={'color': 'red', 'text-weight': 'bold'}),
#                             width=12)])
#             ], fluid=True)]),
#         dbc.Tab(label="VERIFICATION", children=[
#
#         ])
#     ]),
#     dbc.Row(children=[
#         dbc.Col(html.H5([html.I(className='fa fa-copyright'), ' Group 1 2024'], style={'padding-top': '5px'}),
#                 width={"size": 2, 'offset': 10})
#     ])
# ])
#
#
# @callback(Output('take-picture', 'displayed'),
#           Output('take-pic-btn', 'n_clicks'),
#           [Input('take-pic-btn', 'n_clicks')])
# def display_confirm(value):
#     if value:
#         return True, 0
#     return False, 0
#
#
# @callback(
#     Output('output-message', 'children', allow_duplicate=True),
#     [Input('take-picture', 'submit_n_clicks')],
#     [State('username-input', 'value')], config_prevent_initial_callbacks=True
#
# )
# def scan_face(n_clicks, username):
#     if n_clicks > 0:
#         video_capture = cv2.VideoCapture(0)
#
#         if not video_capture.isOpened():
#             raise FileNotFoundError('Could not take picture.')
#
#         ret, frame = video_capture.read()
#         if not ret:
#             raise FileNotFoundError('Could not take picture.')
#
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         cap = cv2.VideoCapture(0)
#
#         if not cap.isOpened():
#             return "Error: Could not access the camera."
#
#         ret, frame = cap.read()
#
#         if ret:
#             cv2.imwrite(f"{username}.jpg", frame)
#
#             cap.release()
#             # print(f'{username}.jpg')
#             return f"Image taken successfully!"
#         else:
#             cap.release()
#             return "Error: Could not capture image."
#
#     return ""
#
#
# @callback(Output('output-message', 'children'),
#           Input('enroll-btn', 'n_clicks'),
#           Input('access-type', 'value'),
#           [State('username-input', 'value'),
#            State('password-input', 'value'),
#            State('email-input', 'value')]
#           )
# def enroll_user(n_clicks, is_admin, username, password, email):
#     if n_clicks > 0:
#         headers = {
#             'Authorization': f"Bearer {bearer_token}"
#         }
#         enroll_url = f"{api_url}/enroll"
#         filename = f"{username}.jpg"
#
#         try:
#             with open(filename, "rb") as image_file:
#                 files = {
#                     "image": (filename, image_file, "image/jpg")
#                 }
#
#                 data = {
#                     "username": username,
#                     "email": email,
#                     "is_admin": is_admin,
#                     "password": password
#                 }
#
#                 response = requests.post(enroll_url, headers=headers, data=data, files=files)
#         except FileNotFoundError:
#             return f"Error: The file {filename} does not exist."
#         os.remove(filename)
#         if response.status_code == 200:
#             return f"{response.json()['message']}"
#         else:
#             return f"Error: {response.status_code}, {response.text}"
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
