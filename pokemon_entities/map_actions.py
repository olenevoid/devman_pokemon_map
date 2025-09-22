import folium
from pokemon_entities.models import Pokemon
from django.http.request import HttpRequest


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(
        folium_map: folium.Map,
        lat: float,
        lon: float,
        image_url: str = DEFAULT_IMAGE_URL
):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def fill_map_with_pokemons(
        pokemons: list[Pokemon],
        request: HttpRequest,
        folium_map: folium.Map | None = None
) -> folium.Map:
    if not folium_map:
        folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon in pokemons:
        for pokemon_entity in pokemon['entities']:
            add_pokemon(
                folium_map,
                pokemon_entity['lat'],
                pokemon_entity['lon'],
                request.build_absolute_uri(pokemon['img_url'])
            )

    return folium_map
