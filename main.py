import picoweb
import ujson
import math
import uasyncio as asyncio
import Stepper
from machine import Pin
from bdc import calcBDC

app = picoweb.WebApp(__name__)

In1 = Pin(23,Pin.OUT) # IN1-> GPIO2 
In2 = Pin(19,Pin.OUT) # IN1-> GPIO0 
In3 = Pin(22,Pin.OUT) # IN1-> GPIO4 
In4 = Pin(33,Pin.OUT) # IN1-> GPIO5

s1 = Stepper.create(In1,In2,In3,In4, delay=10, mode='FULL_STEP')


@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ballistic Calculator</title>
    </head>
    <body>
        <h1>Ballistic Calculator</h1>
        <form action="/rotate" method="post">
            <label for="bc">Ballistic coeficient:</label>
            <input type="number" step=0.001 id="bc" name="ballistic coeficient" required><br><br>
            <label for="v">Initial velocity [m/s]:</label>
            <input type="number" step=0.001 id="v" name="initial velocity" required><br><br>
            <label for="sh">The Sight height over bore [cm]:</label>
            <input type="number" step=0.001 id="sh" name="sight hight over bore" required><br><br>
            <label for="zero">The zero range of the rifle [m]:</label>
            <input type="number" step=0.001 id="zero" name="rifle zero" required><br><br>
            <label for="drag_function">Drag function:</label>
            <input type="text" id="drag_function" name="drag function" required><br><br>
            <label for="computationMeters">Range fo computation [m]:</label>
            <input type="number" step=0.001 id="computationMeters" name="distance" required><br><br>
            <input type="submit" value="Compute distance">
        </form>
    </body>
    </html>
    """
    yield from resp.awrite(html_content)

@app.route("/rotate", methods=['POST'])
def rotate(req, resp):
    yield from req.read_form_data()
    if 'ballistic coeficient' in req.form:
        try:
            bc = float(req.form.get("ballistic coeficient", 0))
            v = float(req.form.get("initial velocity", 0))
            sh = float(req.form.get("sight hight over bore", 0))
            zero = float(req.form.get("rifle zero", 0))
            drag_function = req.form.get("drag function", "")
            computationMeters = float(req.form.get("distance", 0))
            print(f"dane pobrane")
            MOA = calcBDC(bc, v, sh, zero, drag_function, computationMeters)
            print(f"MOA obliczone")
            angle = int(MOA)*5
            print(f"Kat policzony")
            set_stepper_motor_angle(angle, MOA)
            message = f"Rotation by {MOA:.2f} MOA. Returning to main page..."
            yield from picoweb.start_response(resp)
            response_html = f"""
                <html>
                <head>
                    <meta http-equiv="refresh" content="5;url=/">
                </head>
                <body>
                    <p>{message}</p>
                </body>
                </html>
                """
            yield from resp.awrite(response_html)
        except ValueError:
            yield from picoweb.http_error(resp, "400", "Invalid input: Please enter a valid number.")
    else:
        yield from picoweb.http_error(resp, "400", "Missing angle parameter.")

def set_stepper_motor_angle(angle, MOA):
    print(f"obracanie")
    s1.angle(angle)  # Ustawianie wymaganego kąta
    print(f"Stepper motor set to {angle} degrees")  # Wydruk stanu dla debugowania
    print(f"Correction: {MOA} MOA")

def run():
    app.run(debug=True, host="0.0.0.0", port=80)

loop = asyncio.get_event_loop()
loop.create_task(run())