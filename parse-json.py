import json
import re

def parse_json(json_string):

    cleaned = re.sub("^```(?:json)?\s*", "", json_string)
    cleaned = re.sub("\s*```$", "", cleaned)
    cleaned = cleaned.strip()

    try:
        data = json.loads(json_string)
        return data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    