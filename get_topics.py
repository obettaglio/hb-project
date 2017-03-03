import json

data = open('topictree.json').read()
data = json.loads(data)

topics = {}


def find_topics(node):
    """Add video topics as keys and arrays of corresponding videos as values to a dictionary."""

    topic = node.get('slug', None)

    if topic not in topics and topic is not None:
        topics[topic] = []

    children = node.get('children', None)

    if children:
        for child in children:
            find_topics(child)

    else:
        topics[topic].append(node)


def find_topic_paths(node):
    """Add video topic paths as keys and arrays of corresponding videos as values to a dictionary."""

    # "topic_page_url": "/math/early-math/cc-early-math-add-sub-basics/cc-early-math-add-sub-intro"

    topic_path = node.get('topic_page_url', None)

    if topic_path:
        last_slash = topic_path.rfind('/')
        topic_path = topic_path[:last_slash]

        if topic_path not in topics:
            topics[topic_path] = []

        children = node.get('children', None)

        if children:
            for child in children:
                find_topics(child)

        else:
            topics[topic_path].append(node)


find_topics(data)
# find_topic_paths(data)
