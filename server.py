from flask import Flask, jsonify, abort, send_from_directory

import generate
import ikeagen

app = Flask(__name__, static_folder='public/', static_url_path='/')


@app.route('/api/description/<int:count>/')
def get_description(count):
    descriptions = []
    if count > 1000:
        abort(422)
    for _ in range(count):
        descriptions.append({
            "description": generate.get_description(),
            "name": ikeagen.generate()
        })
    response = jsonify(descriptions)
    return response


if __name__ == "__main__":
    @app.route('/<path:path>')
    def send_js(path):
        return send_from_directory('public', path)


    app.run()
