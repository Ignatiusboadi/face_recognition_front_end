from app import app
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import login_page as login
import main
import os

app.layout = html.Div(style={'background-color': 'GhostWhite', 'height': '100vh', 'padding-top': '50px',
                             'padding-bottom': '50px', 'background-image': 'url("/assets/face_ver.png"'},
                      children=[
                          dcc.Location(id='url', refresh=False),
                          html.Div(id='page-content'),
                          dcc.Store(id='token', data=0),
                          dbc.Row(children=[
                              dbc.Col(html.H5([html.I(className='fa fa-copyright'), ' Group 1 2024'],
                                              style={'padding-top': '85px', 'color': 'white'}),
                                      width={"size": 2, 'offset': 10})])])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
              Input('token', 'data'))
def display_page(pathname, token):
    if pathname == '/' or not token:
        return login.layout
    elif pathname == '/main' and token:
        return main.layout
    else:
        return '404: Page not found'


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8051)))
