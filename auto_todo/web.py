import http.server
import re

from .parser import Tasks

PORT = 9999
HOST = '0.0.0.0'
TOKEN = 'CHANGE ME'
FILE_PATH = 'todo.txt'
REFRESH = '30'


def strip_todo(task: str) -> str:
    regex = r"(@[u|i]\d)|(\+\S+)|(due\:\d{4}-\d\d-\d\d)"
    return re.sub(regex, '', task).strip()


def get_due_date(task: str) -> str:
    regex = r"due\:(\d{4}-\d\d-\d\d)"
    match = re.search(regex, task)
    if match:
        return match.group(1)
    return ''


def date_is_close(date: str) -> bool:
    from datetime import datetime
    now = datetime.now()
    date = datetime.strptime(date, '%Y-%m-%d')
    delta = date - now
    return delta.days < 3


def date_is_past(date: str) -> bool:
    from datetime import datetime
    now = datetime.now()
    date = datetime.strptime(date, '%Y-%m-%d')
    delta = date - now
    return delta.days < 0


def get_date_color(date: str) -> str:
    return ''


def render_due_date(date: str) -> str:
    if date == '':
        return '<td></td>'
    colour = ''
    if date_is_past(date):
        colour = '.due-past'
    if date_is_close(date):
        colour = '.due-close'
    return f'<td class={colour}>{date}</td>'


priority_colours = {
    'A': 'red',
    'B': 'orange',
    'C': 'yellow',
    'D': 'green',
    'E': 'blue',
    'F': 'indigo',
    'G': 'violet'
}

priority_int_to_char = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
}


def get_urgency(task: str) -> str:
    urgency = re.search(r'@u\d', task)
    if urgency:
        urgency = urgency.group(0)[2]
        colour = priority_colours[priority_int_to_char[int(urgency)]]
        return f'<td style="color: {colour}">{urgency}</td>'
    return '<td></td>'


def get_importance(task: str) -> str:
    importance = re.search(r'@i\d', task)
    if importance:
        importance = importance.group(0)[2]
        colour = priority_colours[priority_int_to_char[int(importance)]]
        return f'<td style="color: {colour}">{importance}</td>'
    return '<td></td>'


def get_priority(priority: str) -> str:
    if priority == '^':
        return '<td></td>'
    colour = priority_colours[priority]
    return f'<td style="color: {colour}">{priority}</td>'

def color()->str:
    style = """
    <style>
    .due-past {
        color: red;
    }
    .due-close {
        color: orange;
    }
    body{
        margin: 0;
        padding: 0;
        font-family: sans-serif;
        background-color: #111;
        color: #ccc;
    }
    table{
        width: 100%;
        border-collapse: collapse;
        font-size: max(2vw, 1.3vh);
        border: 0;
    }
    td, th{
    padding: 1rem;
    border: 0;
    }
    tr:nth-child(odd){
        background-color: #222;
    }
    </style>
    """
    return render(style)

def monochrome()->str:
    style = """
    <style>
    body{
        margin: 0;
        padding: 0;
        font-family: sans-serif;
        background-color: #fff;
        color: #000 !important;
    }
    table{
        width: 100%;
        border-collapse: collapse;
        font-size: 2rem;
        border: 0;
    }
    td:nth-child(1){
        font-size: 3rem;
    }
    td, th{
    padding: 1rem;
    border: 0;
    color: #000 !important;
    }
    tr:nth-child(odd){
        background-color: #eee;
    }
    </style>
    """
    return render(style)

def render(style) -> str:
    tasks = Tasks(FILE_PATH)
    tasks.load()

    html = (f'<!DOCTYPE html>'
            f'<html><head><title>Todo.txt</title>{style}</head><body>')
    html += '<table border="1">'
    html += ('<tr>'
             '<th>Task</th>'
             '<th>Priority</th>'
             '<th>Urgency</th>'
             '<th>Importance</th>'
             '<th>Projects</th>'
             '<th>Due</th>'
             '</tr>')
    for task in tasks.tasks:
        if len(task.todo.strip()) < 2:
            continue
        if task.finished:
            continue
        projects = ', '.join([p[1:] for p in task.projects])
        task_description = strip_todo(task.todo)
        due_date = get_due_date(task.todo)
        html += (f'<tr>'
                 f'<td>{task_description}</td>' +
                 get_priority(task.priority) +
                 get_urgency(task.todo) +
                 get_importance(task.todo) +
                 f'<td>{projects}</td>' +
                 render_due_date(due_date) +
                 f'</tr>')
    html += '</table>'
    html += '</body></html>'
    return html


if __name__ == '__main__':
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == f'/{TOKEN}':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Refresh', REFRESH)
                self.end_headers()
                self.wfile.write(monochrome().encode('utf-8'))
            elif self.path == f'/{TOKEN}/color':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Refresh', REFRESH)
                self.end_headers()
                self.wfile.write(color().encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()


    httpd = http.server.HTTPServer((HOST, PORT), Handler)
    print(f'Serving at {HOST}:{PORT}')
    httpd.serve_forever()
