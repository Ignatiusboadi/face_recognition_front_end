import dash
import dash_bootstrap_components.themes as themes


# api_url = 'http://127.0.0.1:8001'
api_url = 'https://face-recognition-image-963201605868.us-central1.run.app'
FONT_AWESOME = (
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
)

app = dash.Dash(__name__, title='FACE RECOGNITION', external_stylesheets=[themes.SIMPLEX, FONT_AWESOME],
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
                update_title=None, suppress_callback_exceptions=True)

server = app.server
