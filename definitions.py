from rdflib import Graph
import random

ontology_path = "data/definitions.owl"
g = Graph()
g.parse(ontology_path, format="xml")

def fetch_definitions():
    query = """
    SELECT ?term ?definition WHERE {
        ?term rdfs:comment ?definition .
    }
    """
    results = g.query(query)
    return {str(row.term.split('#')[-1]): str(row.definition) for row in results}

def generate_quiz_data(num_questions=5):
    all_definitions = fetch_definitions()
    quiz_data = {}
    answers = {}
    options = list(all_definitions.keys())

    for _ in range(num_questions):
        term, definition = random.choice(list(all_definitions.items()))
        incorrect_choices = random.sample([opt for opt in options if opt != term], 3)
        choices = incorrect_choices + [term]
        random.shuffle(choices)
        quiz_data[definition] = choices
        answers[definition] = term

    return quiz_data, answers

def calculate_score(answers, user_answers):
    score = 0
    for question, correct_answer in answers.items():
        if user_answers.get(question) == correct_answer:
            score += 1
    return score

def get_definition(term):
    return fetch_definitions().get(term, "definition not found.")
