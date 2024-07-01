from jinja2 import Environment, FileSystemLoader
import os

template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
env = Environment(loader=FileSystemLoader(template_dir))


def render_template(template_name, context):
    template = env.get_template(template_name)
    return template.render(context)
