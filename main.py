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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comarch Targeting System - Ballistic Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #1f1f1f; 
            color: #ffffff; 
            overflow: hidden;
            cursor: url('cursor.png'), auto;
        }
        .container {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            max-width: 600px;
            margin: 100px auto; 
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
            background-color: rgba(0, 0, 0, 0.7); 
        }
        h1 {
            text-align: center;
            font-size: 2em;
            margin-bottom: 20px;
        }
        h1 span {
            display: block; 
            font-size: 1.5em; 
            font-weight: normal;
            color: #1c75db; 
        }
        .separator {
            width: 100%;
            height: 2px;
            background-color: #1c75db;
            margin: 10px 0;
        }
        form {
            width: 100%;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        label {
            font-weight: bold;
        }
        input[type="number"],
        input[type="text"],
        select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ffffff;
            border-radius: 6px;
            box-sizing: border-box;
            background-color: #000000;
            color: #ffffff;
        }
        input[type="submit"] {
            width: 100%;
            padding: 12px;
            background-color: #1c75db;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        input[type="submit"]:hover {
            background-color: #2c8cf4;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1><span>Comarch</span> Targeting System <span class="separator"></span> Ballistic Calculator</h1>
        <form action="/rotate" method="post">
            <label for="bc">Ballistic coefficient:</label>
            <input type="number" step="0.001" id="bc" name="ballistic coeficient" required>
            <label for="v">Initial velocity [m/s]:</label>
            <input type="number" step="0.001" id="v" name="initial velocity" required>
            <label for="sh">The Sight height over bore [cm]:</label>
            <input type="number" step="0.001" id="sh" name="sight height over bore" required>
            <label for="zero">The zero range of the rifle [m]:</label>
            <input type="number" step="0.001" id="zero" name="rifle zero" required>
            <label for="drag_function">Drag function:</label>
            <select id="drag_function" name="drag function" required>
                <option value="G1">G1</option>
                <option value="G2">G2</option>
                <option value="G3">G3</option>
                <option value="G4">G4</option>
            </select>
            <label for="computationMeters">Range for computation [m]:</label>
            <input type="number" step="0.001" id="computationMeters" name="distance" required>
            <input type="submit" value="Compute distance">
        </form>
    </div>
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
            with open("data.txt", "w") as file:
                file.write("{},{},{},{},{}\n".format(bc, v, sh, zero, drag_function))
            print(f"dane zapisane")
            MOA_V, MOA_H = calcBDC(bc, v, sh, zero, drag_function, computationMeters, 0, 0)
            print(f"MOA obliczone")
            angle = int(MOA_V)*5
            print(f"Kat policzony")
            set_stepper_motor_angle(angle, MOA_V)
            message = f"Rotation by {MOA_V:.2f} MOA. Returning to main page..."
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

def set_stepper_motor_angle(angle, MOA_V):
    print(f"obracanie")
    s1.angle(angle)  # Ustawianie wymaganego kąta
    print(f"Stepper motor set to {angle} degrees")  # Wydruk stanu dla debugowania
    print(f"Correction: {MOA_V} MOA")

def run():
    app.run(debug=True, host="0.0.0.0", port=80)

loop = asyncio.get_event_loop()
loop.create_task(run())