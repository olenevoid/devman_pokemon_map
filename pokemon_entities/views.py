from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from pokemon_entities import db_requests as db
from pokemon_entities.map_actions import fill_map_with_pokemons
from pokemon_entities.models import Pokemon
from django.shortcuts import get_object_or_404


def show_all_pokemons(request: HttpRequest) -> HttpResponse:
    pokemons = db.get_pokemons_with_active_entities()
    folium_map = fill_map_with_pokemons(pokemons, request)

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append(
            {
                'pokemon_id': pokemon['pokemon_id'],
                'img_url': pokemon['img_url'],
                'title_ru': pokemon['title_ru'],
            }
        )

    context = {
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    }

    return render(request, 'mainpage.html', context=context)


def show_pokemon(request: HttpRequest, pokemon_id: int) -> HttpResponse:
    requested_pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    parsed_pokemon = db.parse_pokemon(requested_pokemon)
    folium_map = fill_map_with_pokemons([parsed_pokemon,], request)

    context = {
        'map': folium_map._repr_html_(),
        'pokemon': parsed_pokemon
    }

    return render(request, 'pokemon.html', context=context)
