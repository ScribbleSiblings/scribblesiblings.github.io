import urllib.request
import json

from math import modf

from generate import load_json_from_file

def topological_sort(edge_lists, nodes, base_nodes):

    dependancies = {node:edge_lists.get(node, [])[:] for node in nodes}
    s = [x for x in base_nodes]
    l = []

    if len(s) == 0 and len(nodes) > 0:
        raise ValueError("JSON has cyclical night order dependancies.")

    while len(s) > 0:
        n = s.pop()
        l.append(n)
        for node in dependancies[n]:
            s.append(node)
    
    return l


def auto_insert_nightorder(in_json):

    with urllib.request.urlopen("https://script.bloodontheclocktower.com/data/nightsheet.json") as url:
        preexisting_data = json.load(url)
    
    preexisting_first_night = {preexisting_data["firstNight"][i]:i for i in range(len(preexisting_data["firstNight"]))}
    preexisting_other_night = {preexisting_data["otherNight"][i]:i for i in range(len(preexisting_data["otherNight"]))}

    indeces = {}
    index = 0

    for character in in_json:
        id = character.get("id", None)
        indeces[id] = index
        index += 1

    # First night
    
    dependancy_edges = {}
    character_nodes = set()
    official_nodes = set()

    for character in in_json:
        id = character.get("id", None)
        if id is not None and id != "_meta":
            preceeding_character = character.get("preceedingFirstNightId", None)
            if preceeding_character is not None:
                character_nodes.add(id)
                character_nodes.add(preceeding_character)
                if preceeding_character in preexisting_first_night:
                    official_nodes.add(preceeding_character)
                if preceeding_character not in dependancy_edges:
                    dependancy_edges[preceeding_character] = []
                dependancy_edges[preceeding_character].append(id)
    
    first_night_ordering = topological_sort(dependancy_edges, character_nodes, official_nodes)
    current_order = 0
    counter = 0
    for id in first_night_ordering:
        if id in preexisting_first_night:
            current_order = preexisting_first_night[id]
            counter = 0
        else:
            counter += 1
            current_order += 1 / (2**counter)
            in_json[indeces[id]]["firstNight"] = current_order
    
    # Other nights

    dependancy_edges = {}
    character_nodes = set()
    official_nodes = set()

    for character in in_json:
        id = character.get("id", None)
        if id is not None and id != "_meta":
            preceeding_character = character.get("preceedingOtherNightId", None)
            if preceeding_character is not None:
                character_nodes.add(id)
                character_nodes.add(preceeding_character)
                if preceeding_character in preexisting_other_night:
                    official_nodes.add(preceeding_character)
                if preceeding_character not in dependancy_edges:
                    dependancy_edges[preceeding_character] = []
                dependancy_edges[preceeding_character].append(id)
    
    other_night_ordering = topological_sort(dependancy_edges, character_nodes, official_nodes)
    current_order = 0
    counter = 0
    for id in other_night_ordering:
        if id in preexisting_other_night:
            current_order = preexisting_other_night[id]
            counter = 0
        else:
            counter += 1
            current_order += 1 / (2**counter)
            in_json[indeces[id]]["otherNight"] = current_order

    return in_json

if __name__ == "__main__":
    json_file = "collection"
    new_json = auto_insert_nightorder(load_json_from_file(json_file))
    pretty_json = json.dumps(new_json, indent=4)
    with open(json_file + ".json", "w") as out:
        out.write(pretty_json)