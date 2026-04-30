from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

locations = {}

# Page opened on device B
@app.route('/track')
def track():
    user = request.args.get("user")

    return f"""
    <html>
    <body>
        <h2>Sharing your location...</h2>
        <script>
            navigator.geolocation.getCurrentPosition(function(position) {{
                fetch('/update', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        user: '{user}',
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    }})
                }}).then(() => {{
                    document.body.innerHTML = "Location shared successfully!";
                }});
            }});
        </script>
    </body>
    </html>
    """

# Receive location from B
@app.route('/update', methods=['POST'])
def update():
    data = request.json
    locations[data['user']] = {
        "lat": data['lat'],
        "lng": data['lng']
    }
    return {"status": "ok"}

# View location on A
@app.route('/view/<user>')
def view(user):
    loc = locations.get(user)

    if not loc:
        return "No location yet"

    return redirect(f"https://www.google.com/maps?q={loc['lat']},{loc['lng']}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
