from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404


def parse_pokemon(pokemon: Pokemon, only_active_entities: bool = False):
    if only_active_entities:
        entities = pokemon.get_active_entities()
    else:
        entities = pokemon.pokemonentity_set.all()

    parsed_pokemon = {
        'pokemon_id': pokemon.pk,
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'img_url': pokemon.image.url,
        'next_evolution': parse_evolution(pokemon.next_evolutions.first()),
        'previous_evolution': parse_evolution(pokemon.previous_evolution),
        'entities': [parse_pokemon_entity(entity) for entity in entities]
    }

    return parsed_pokemon


def parse_evolution(pokemon: Pokemon) -> dict:
    if not pokemon:
        return {}

    parsed_evolution = {
        "title_ru": pokemon.title_ru,
        "pokemon_id": pokemon.pk,
        "img_url": pokemon.image.url
    }

    return parsed_evolution


def parse_pokemon_entity(pokemon_entity: PokemonEntity):
    parsed_entity = {
        'level': pokemon_entity.level,
        'lat': pokemon_entity.latitude,
        'lon': pokemon_entity.longitude,
        'exists': pokemon_entity.is_active() 
    }
    return parsed_entity


def get_pokemons_with_active_entities() -> list[dict]:
    pokemons: list[Pokemon] = Pokemon.objects.filter(pokemonentity__gt=0)

    parsed_pokemons: list[dict] = []

    for pokemon in pokemons.distinct():
        if pokemon.has_active_entities():
            parsed_pokemons.append(parse_pokemon(pokemon, True))

    return parsed_pokemons


def get_pokemon_with_active_entities(pokemon_id: int) -> dict:
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    return parse_pokemon(pokemon, True)


def get_active_entities() -> list[dict]:
    entities = PokemonEntity.objects.filter(
        appeared_at__lte=localtime(),
        disappeared_at__gte=localtime()
    )

    return [parse_pokemon_entity(entity) for entity in entities]
