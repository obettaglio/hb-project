import json

data = open('topictree.json').read()
data = json.loads(data)

topics = {}


def find_topics(node):
    """Add video topics as keys and arrays of corresponding videos as values to a dictionary."""

    topic = node.get('slug', None)

    if topic not in topics:
        topics[topic] = []

    children = node.get('children', None)

    if children:
        for child in children:
            find_topics(child)

    else:
        topics[topic].append(node)

find_topics(data)
