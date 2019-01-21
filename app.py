from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
import uvicorn

from functions_equations import *


app = Starlette(debug=True, template_directory='templates')
#app.mount('/static', StaticFiles(directory='statics'), name='static')
app.mount('/data', StaticFiles(directory='data'), name='data')


@app.route('/')
async def homepage(request):
    #template = app.get_template('index.html')
    #content = template.render(request=request)
    #return HTMLResponse(content)

    student = 'unknown_student'
    cnt_equations = 20
    numbers_template = [2, 3]
    numbers_template = [2]

    number_low = 0
    number_low = -10
    number_high = 10

    numbers_must_be = 'any'
    numbers_must_be = [6, -6, 9, -9]    # Даша их путала - сделали чтобы в примерах обязательно они были

    answers_mode = 'cycle'
    answers_template = [0, 1, 2, 3, 4, 5],

    answers_mode = 'any'

    E = Create_Equations(
            student=student,
            cnt_equations=cnt_equations,
            numbers_template=numbers_template,
            number_low=number_low,
            number_high=number_high,
            numbers_must_be=numbers_must_be,
            answers_mode=answers_mode,
            answers_template=answers_template,
            )
    content = E.create_page_with_equations()

    return HTMLResponse(content)


@app.route('/error')
async def error(request):
    """
    An example error.
    Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = app.get_template('404.html')
    content = template.render(request=request)
    return HTMLResponse(content, status_code=404)


@app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = app.get_template('500.html')
    content = template.render(request=request)
    return HTMLResponse(content, status_code=500)


@app.on_event('startup')
def startup():
    print('Ready to go')


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
