from pokemon_entities.models import Pokemon, PokemonEntity


def parse_pokemon(pokemon: Pokemon):
    entities = pokemon.pokemonentity_set.all()

    parsed_pokemon = {
        'pokemon_id': pokemon.pk,
        'title_ru': pokemon.name,
        'title_en': '',
        'title_jp': '',
        'description': '',
        'img_url': pokemon.image.url,
        'next_evolution': '',
        'entities': [parse_pokemon_entity(entity) for entity in entities]
    }

    return parsed_pokemon


def parse_pokemon_entity(pokemon_entity: PokemonEntity):
    parsed_entity = {
        'level': pokemon_entity.level,
        'lat': pokemon_entity.latitude,
        'lon': pokemon_entity.longitude,
        'exists': pokemon_entity.is_active() 
    }
    return parsed_entity


def get_pokemons_with_entities():
    pokemons: list[Pokemon] = Pokemon.objects.filter(pokemonentity__gt=0)
    return [parse_pokemon(pokemon) for pokemon in pokemons.distinct()]
