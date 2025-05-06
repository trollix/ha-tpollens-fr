def parse_pollens_api_response(json_data):
    attributes = {
        "location": None,
        "date_update": None,
        "source": None,
        "today": {},
        "tomorrow": {},
        "day_after_tomorrow": {}
    }

    pollen_labels = {
        "gram": "graminées",
        "boul": "bouleau",
        "aul": "aulne",
        "oliv": "olivier",
        "ambr": "ambroisie",
        "arm": "armoise"
    }

    # On récupère les données communes dans le premier bloc
    common = json_data["features"][0]["properties"]
    attributes["location"] = common["lib_zone"]
    attributes["date_update"] = common["date_maj"]
    attributes["source"] = common["source"]

    for feature in json_data["features"]:
        props = feature["properties"]
        entry = {
            "date": props["date_ech"],
            "dominant": props["pollen_resp"],
            "code_qual": props["code_qual"],
            "lib_qual": props["lib_qual"],
            "pollens": {
                pollen_labels[key]: props.get(f"code_{key}", 0.0)
                for key in pollen_labels
            }
        }

        if props["date_ech"] == props["date_dif"]:
            attributes["today"] = entry
        elif not attributes["tomorrow"]:
            attributes["tomorrow"] = entry
        else:
            attributes["day_after_tomorrow"] = entry

    state = attributes["today"]["lib_qual"] if attributes["today"] else "n/a"
    return state, attributes
