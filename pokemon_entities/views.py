import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities import db_requests as db


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
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


def fill_map_with_pokemons(pokemons, request, folium_map = None):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in pokemon['entities']:
            add_pokemon(
                folium_map, pokemon_entity['lat'],
                pokemon_entity['lon'],
                request.build_absolute_uri(pokemon['img_url'])
            )

    return folium_map


def show_all_pokemons(request):
    pokemons = db.get_pokemons_with_active_entities()
    folium_map = fill_map_with_pokemons(pokemons, request)

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon['pokemon_id'],
            'img_url': pokemon['img_url'],
            'title_ru': pokemon['title_ru'],
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = db.get_pokemon_with_active_entities(pokemon_id)
    folium_map = fill_map_with_pokemons([requested_pokemon,], request)

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon
    })
