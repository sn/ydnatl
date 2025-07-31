#from ydnatl import *
import timeit
from ydnatl.tags.html import *
from ydnatl.tags.layout import *
from ydnatl.tags.text import *
from ydnatl.core.element import *

# Dynamic content based on conditions


iterations = 1000

python_time = timeit.timeit(
    stmt="""
from ydnatl.tags.html import HTML, Head, Body, Title
from ydnatl.tags.layout import Div
from ydnatl.tags.text import H1, Paragraph
from ydnatl.core.element import HTMLElement

day_of_week = "Monday"
html = HTML()
header = Head()
body = Body()

body.append(
    Div(
        H1("My Headline"),
        Paragraph("Basic paragraph element"),
    )
)

if day_of_week == "Monday": 
    header.append(Title("Unfortunately, it's Monday!"))
else:
    header.append(Title("Great! It's no longer Monday!"))

html.append(header)
html.append(body)


html.render()"""
)

cython_time = timeit.timeit(
    stmt="""
from ydnatl.tags.html import HTML, Head, Body, Title
from ydnatl.tags.layout import Div
from ydnatl.tags.text import H1, Paragraph
from ydnatl.core.element import HTMLElement

day_of_week = "Monday"

html = HTML()
header = Head()
body = Body()

body.append(
    Div(
        H1("My Headline"),
        Paragraph("Basic paragraph element"),
    )
)

if day_of_week == "Monday": 
    header.append(Title("Unfortunately, it's Monday!"))
else:
    header.append(Title("Great! It's no longer Monday!"))

html.append(header)
html.append(body)


html.render_c()""",
    number=iterations
)

print(f"Python method: {python_time:.6f} seconds")
print(f"Cython method: {cython_time:.6f} seconds")
print(f"Speedup: {python_time / cython_time:.2f}x")

#print(html.render())
#print(html.render_c())