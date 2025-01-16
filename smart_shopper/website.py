from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from smart_shopper.models import Store, Catagories
import structlog

logger = structlog.get_logger()

# Initialize the Dash app with bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = html.Div([
    html.H1("Smart Shopper", className="text-center my-4"),
    dbc.Container([
        dbc.Form([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Email"),
                    dbc.Input(type="email", id="email-input", placeholder="Enter your email")
                ]),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Companies"),
                    dbc.Checklist(
                        id="company-input",
                        options=[
                            {"label": "Costco", "value": Store.COSTCO},
                            {"label": "Target", "value": Store.TARGET},
                            {"label": "Walmart", "value": Store.WALMART},
                            {"label": "Amazon", "value": Store.AMAZON},
                            {"label": "Hyvee", "value": Store.HYVEE},
                            {"label": "Aldi", "value": Store.ALDI},
                        ],
                        inline=True
                    )
                ]),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Message"),
                    dbc.Textarea(id="text-input", placeholder="What are you looking for deals on? Type in something like 'I want to get deals on coffee and snacks'")
                ]),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Frequency"),
                    dbc.RadioItems(
                        id="frequency-input",
                        options=[
                            {"label": "Weekly", "value": "weekly"},
                            {"label": "Bi-weekly", "value": "biweekly"},
                        ]
                    )
                    
                ]),
            ], className="mb-3"),
            dbc.Button("Submit", id="submit-button", color="primary"),
        ]),
        html.Div(id="output-message", className="mt-3")
    ])
])

@callback(
    Output("output-message", "children"),
    Input("submit-button", "n_clicks"),
    State("email-input", "value"),
    State("text-input", "value"),
    State("company-input", "value"),
    State("frequency-input", "value"),
    prevent_initial_call=True
)
def submit_form(n_clicks, email, message, company, frequency):
    logger.info(f"Email: {email}, Message: {message}, Company: {company}, Frequency: {frequency}")
    if email and message and company and frequency:
        return html.Div(f"Submitted! Email: {email}, for companies {company} with message: {message} and frequency: {frequency}", 
                       className="alert alert-success")
    else:
        return html.Div("Please fill in all fields", 
                       className="alert alert-warning")

if __name__ == '__main__':
    app.run_server(debug=True)