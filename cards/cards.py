import functools
import yaml
from glob import glob



@functools.lru_cache()
def cards():

    return "test"

@functools.lru_cache()
def all_cards():
    result = {}
    list_of_card_files = glob('./cards/*/*.yaml')
    for file in list_of_card_files:
        with open(file, 'r') as stream:
            cur_val = yaml.load(stream)
            result[cur_val["Name"].lower()] = cur_val
    return result

@functools.lru_cache()
def dungeons():
    result = {}
    list_of_card_files = glob('./cards/dungeons/*.yaml')
    for file in list_of_card_files:
        with open(file, 'r') as stream:
            cur_val = yaml.load(stream)
            result[cur_val["Name"].lower()] = cur_val
    return result

@functools.lru_cache()
def enemies():
    result = {}
    list_of_card_files = glob('./cards/enemies/*.yaml')
    for file in list_of_card_files:
        with open(file, 'r') as stream:
            cur_val = yaml.load(stream)
            result[cur_val["Name"].lower()] = cur_val
    return result

@functools.lru_cache()
def bosses():
    result = {}
    list_of_card_files = glob('./cards/bosses/*.yaml')
    for file in list_of_card_files:
        with open(file, 'r') as stream:
            cur_val = yaml.load(stream)
            result[cur_val["Name"].lower()] = cur_val
    return result

@functools.lru_cache()
def items():
    result = {}
    list_of_card_files = glob('./cards/items/*.yaml')
    for file in list_of_card_files:
        with open(file, 'r') as stream:
            cur_val = yaml.load(stream)
            result[cur_val["Name"].lower()] = cur_val
    return result

@functools.lru_cache()
def equipment():
    result = {}
    list_of_card_files = glob('./cards/equipment/*.yaml')
    for file in list_of_card_files:
        with open(file, 'r') as stream:
            cur_val = yaml.load(stream)
            result[cur_val["Name"].lower()] = cur_val
    return result

@functools.lru_cache()
def classes():
    result = {}
    list_of_card_files = glob('./cards/classes/*.yaml')
    for file in list_of_card_files:
        with open(file, 'r') as stream:
            cur_val = yaml.load(stream)
            result[cur_val["Name"].lower()] = cur_val
    return result

@functools.lru_cache()
def buildings():
    result = {}
    list_of_card_files = glob('./cards/buildings/*.yaml')
    for file in list_of_card_files:
        with open(file, 'r') as stream:
            cur_val = yaml.load(stream)
            result[cur_val["Name"].lower()] = cur_val
    return result
