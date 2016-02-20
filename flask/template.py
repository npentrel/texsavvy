from jinja2 import Environment, FileSystemLoader
import os

# Capture our current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

def render(data):
    j2_env = Environment(loader=FileSystemLoader(current_dir), trim_blocks=True)
    pos1Title = data['positions']['values'][0]['title']
    template = j2_env.get_template('static/cv.html').render(
        name=data['formattedName'],
        tagline=data['headline'],
        email=data['emailAddress'],
        pictureUrl=data['pictureUrls']['values'][0],
        linkedin=data['publicProfileUrl'],
        position1title=data['positions']['values'][0]['title'],
        position1summary=data['positions']['values'][0]['summary'],
        position1startMonth= data['positions']['values'][0]['startDate']['month'],
        position1startYear= data['positions']['values'][0]['startDate']['year']
    )

    return template

if __name__ == '__main__':
    render({})
