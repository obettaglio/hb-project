import json

from video_topics import (counting_topics, place_value_topics, addition_topics,
                          subtraction_topics, addition_subtraction_topics,
                          measurement_data_topics, geometry_topics)

topics = open('videos-by-topic.json').read()
topics = json.loads(topics)

all_videos = []
video_titles = []


def add_videos_by_topic(topics_lst, exam_topic_str):
    """Find all videos in topic list and add them to all_videos.

    Add a custom key 'exam_topic' to each video in topic."""

    for topic in topics_lst:
        topic_videos = topics.get(topic, None)

        if topic_videos is None:
            continue

        for video in topic_videos:
            # print video['title']

            if video['title'] not in video_titles:
                video['exam_topic'] = exam_topic_str
                all_videos.append(video)
                print "Added: " + video['title']
                video_titles.append(video['title'])

        # all_videos.extend(topic_videos)

add_videos_by_topic(counting_topics, 'counting')
add_videos_by_topic(place_value_topics, 'place_value')
add_videos_by_topic(addition_topics, 'addition')
add_videos_by_topic(subtraction_topics, 'subtraction')
add_videos_by_topic(addition_subtraction_topics, 'addition_subtraction')
add_videos_by_topic(measurement_data_topics, 'measurement_data')
add_videos_by_topic(geometry_topics, 'geometry')

print len(all_videos)

all_videos = json.dumps(all_videos)

video_file = open('static/data/videos.json', 'w')
video_file.write(all_videos)
video_file.close()
