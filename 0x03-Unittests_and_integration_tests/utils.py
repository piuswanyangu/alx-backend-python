def access_nested_map(nested_map, path):
    for key in path:
        nested_map = nested_map[key]  #will raise keyerror if key is missing
    return nested_map