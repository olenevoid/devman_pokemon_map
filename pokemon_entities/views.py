from django.shortcuts import render
from pokemon_entities import db_requests as db
from pokemon_entities.map_actions import fill_map_with_pokemons


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
