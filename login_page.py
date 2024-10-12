from app import api_url
from dash import dcc, html, Input, Output, State, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import requests
import datetime

email_n = "Once the loading screen finishes, please check your email for a token. Enter the token below and click 'Authenticate'."

layout = html.Div(children=[
    # dbc.Modal(
    #     [
    #         dbc.ModalBody(id='notification', ),
    #         dbc.ModalFooter(
    #             dbc.Button("OK", id="close-notification", className="ml-auto", n_clicks=0)
    #         ),
    #     ],
    #     id="notification-modal",
    #     is_open=False,
    # ),
    dbc.Row(children=[
        dbc.Col(children=[
            html.H2('FACE RECOGNITION SYSTEM',
                    style={'textAlign': 'center', 'font-weight': 'bold', 'color': '#C71585',
                           'font-size': '200%', 'padding-bottom': '40px'
                           }), ], )], justify='center'),
    dbc.Container(children=[
        dbc.Row(children=[
            dbc.Col(html.H2("Login", className="text-center mb-4",
                            style={'color': '#3B1C0A', 'text-weight': 'bold', 'padding-bottom': '40px', }),
                    width=12)]),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Card(style={'background-image': 'url("/assets/login_bg.png"'}, children=[
                    dbc.CardBody(children=[
                        dbc.Label("Username:", html_for="username-input"),
                        dcc.Input(id='username-input', type='text', placeholder='Enter Username',
                                  className="form-control mb-3"),
                        dbc.Label("Password:", html_for="password-input"),
                        dcc.Input(id='password-input', type='password', placeholder='Enter Password',
                                  className="form-control mb-3"),
                        html.Em(id='cred-output-message'),
                        html.Br(),
                        dbc.Row(children=[dbc.Col(children=[
                            dbc.Button("Generate Token", id='token-btn', color="primary",
                                       className='text-center', outline=True, size='md',
                                       style={'padding-left': '45px', 'padding-right': '45px'}), ],
                            width={'offset': 3},
                            style={'padding-left': '25px', 'padding-right': '25px'})],
                            justify="center"),
                        html.Br(),
                        dcc.Loading(html.Em(email_n, id='auth-output', style={'color': 'green', 'font-size': '14px'}),
                                    type='default', fullscreen=True, ),
                        html.Br(),
                        dbc.Label("Token:", html_for="token-input"),
                        dcc.Input(id='token-input', type='text', placeholder='Enter Token',
                                  className="form-control mb-3"),
                        html.Br(),
                        dbc.Row([
                            dbc.Col(
                                dbc.Button("Authenticate", id='auth-btn', color="success",
                                           outline=True, className='mt-1', size='md',
                                           style={'padding-left': '60px', 'padding-right': '60px',
                                                  'color': 'darkgreen'}),
                                width={'offset': 3}, style={'padding-left': '35px', 'padding-right': '35px'})],
                            justify="center"), ])])], width=4)], justify="center"),
        dbc.Row([
            dbc.Col(html.P(id='output-message', className="mt-4 text-center",
                           style={'color': 'red', 'text-weight': 'bold'}), )])
    ], fluid=True)])


@callback(
    Output('auth-output', 'children'),
    Output('token', 'data', allow_duplicate=True),
    # Output('notification-modal', 'is_open'),
    # Output('notification', 'children'),
    Input('token-btn', 'n_clicks'),
    State('username-input', 'value'),
    State('password-input', 'value'),
    config_prevent_initial_callbacks=True
)
def generate_token(n_clicks, username, password):
    if not n_clicks or username is None or password is None:
        raise PreventUpdate
    token_url = f'{api_url}/token'

    auth_data = {
        'username': username,
        'password': password
    }

    token_response = requests.post(token_url, data=auth_data)
    # print(token_response.status_code)
    access_token = token_response.json().get('access_token')

    if token_response.status_code == 200:
        return 'Kindly check your email for a token, enter it below and click Authenticate.', access_token,  # False, ""
    return 'Wrong Username or Password', access_token  # , True, "Wrong Username or Password"


@callback(Output('url', 'pathname', allow_duplicate=True),
          Input('token', 'data'),
          Input('auth-btn', 'n_clicks'),
          State('token-input', 'value'),
          config_prevent_initial_callbacks=True)
def authenticate_user(syst_token, n_clicks, user_token):
    # print('authbtn', datetime.datetime.now(), n_clicks)
    if n_clicks is None:
        raise PreventUpdate
    # print('store', syst_token)
    # print('input', user_token)
    if not n_clicks or not syst_token:
        return '/'

    if syst_token is not None and user_token is not None and syst_token == user_token and n_clicks:
        return '/main'  # False, ""
    elif syst_token != user_token and n_clicks:
        return '/'  # , True, "Wrong Authentication Code"
