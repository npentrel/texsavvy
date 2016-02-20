from jinja2 import Environment, FileSystemLoader
import os

# Capture our current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

def render():
    j2_env = Environment(loader=FileSystemLoader(current_dir), trim_blocks=True)
    print j2_env.get_template('static/cv.html').render(
        name='Rashiq',
        tagline='Android Developer'
    )

if __name__ == '__main__':
    render()
