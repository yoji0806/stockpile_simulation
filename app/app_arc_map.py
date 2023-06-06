"""
Adapted from: https://pydeck.gl/gallery/arc_layer.html

Map of commutes to work within a segment of downtown San Francisco using a
deck.gl ArcLayer.

Green indicates a start point, and red indicates the destination.

The data is collected by the US Census Bureau and viewable in the 2017
LODES data set: https://lehd.ces.census.gov/data/
"""

import os

import dash
import dash_deck
import dash_html_components as html
import pydeck as pdk
import pandas as pd

# mapbox_api_token = os.getenv("MAPBOX_ACCESS_TOKEN")
with open('.mapbox_token', 'r') as file:
    mapbox_access_token = file.read().rstrip()
    
mapbox_api_token = mapbox_access_token


DATA_URL = "./assets/df_evacuee_data_kobe_chuo_portisland_rounded.csv"



# A bounding box for downtown San Francisco, to help filter this commuter data
DOWNTOWN_BOUNDING_BOX = [
    -122.43135291617365,
    37.766492914983864,
    -122.38706428091974,
    37.80583561830737,
] 


def in_bounding_box(point):
    """Determine whether a point is in our downtown bounding box"""
    lng, lat = point
    in_lng_bounds = DOWNTOWN_BOUNDING_BOX[0] <= lng <= DOWNTOWN_BOUNDING_BOX[2]
    in_lat_bounds = DOWNTOWN_BOUNDING_BOX[1] <= lat <= DOWNTOWN_BOUNDING_BOX[3]
    return in_lng_bounds and in_lat_bounds


df_arc = pd.read_csv(DATA_URL)
## Filter to bounding box
#df_arc = df_arc[df_arc[["lng_w", "lat_w"]].apply(lambda row: in_bounding_box(row), axis=1)

GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]

# Specify a deck.gl ArcLayer
arc_layer = pdk.Layer(
    "ArcLayer",
    data=df_arc,
    get_width="S000 * 2",
    get_source_position=["lng_h", "lat_h"],
    get_target_position=["lng_w", "lat_w"],
    get_tilt=15,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True,
)

# view_state = pdk.ViewState(
#     latitude=37.7576171, longitude=-122.5776844, bearing=45, pitch=50, zoom=8,
# )
view_state = pdk.ViewState(
    latitude=34.72481, longitude=135.29442, bearing=0, pitch=50, zoom=12,
)




TOOLTIP_TEXT = {
    "html": "{S000}人 (避難所計：{sum_p})人<br /> 移動距離：{dis}km"
}
#r = pdk.Deck(arc_layer, initial_view_state=view_state, mapbox_key=mapbox_api_token,)
r = pdk.Deck(arc_layer, initial_view_state=view_state)


app = dash.Dash(__name__)

app.layout = html.Div(
    dash_deck.DeckGL(
        r.to_json(), id="deck-gl", tooltip=TOOLTIP_TEXT, mapboxKey=mapbox_api_token
    )
)





if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8051", debug=True)