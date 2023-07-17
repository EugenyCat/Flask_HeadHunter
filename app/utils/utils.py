import json


candidates_path = 'app/files/candidates.json'

def load_candidates_from_json(path:str=candidates_path) -> json:
    """
    Read json file and return dictionary.
    """
    with open('app/files/candidates.json', 'r', encoding='utf-8') as f:
        candidates = json.load(f)
    return candidates

def get_candidate(candidate_id:int) -> dict:
    """
    Return candidate by id
    """
    candidate = {}
    for person in load_candidates_from_json(candidates_path):
        if person.get('id') == candidate_id:
            candidate = person
    return candidate


def get_skills_list() -> set:
    """
    Return list of all skills
    """
    skills = []
    for person in load_candidates_from_json(candidates_path):
        skills += person.get('skills').split(',')
    return   sorted(set(element.lower().lstrip().rstrip() for element in skills))


def get_candidate_by_name(candidate_name:str) -> list:
    """
    Return candidate by name
    """
    candidate = []
    for person in load_candidates_from_json(candidates_path):
        if candidate_name.lower() in person.get('name').lower().split(' '):
            candidate.append(person)
    return candidate


def get_candidate_by_skill(skill_name:str) -> list:
    """
    Return candidate by skill
    """
    candidate = []
    for person in load_candidates_from_json(candidates_path):
        if skill_name.lower() in person.get('skills').lower().split(', '):
            candidate.append(person)
    return candidate