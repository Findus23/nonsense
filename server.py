from flask import Flask, jsonify, url_for, redirect, abort

app = Flask(__name__)

import generate


@app.route('/api/description/<int:count>/')
def get_description(count):
    descriptions = []
    if (count > 1000):
        abort(422)
    for _ in range(count):
        descriptions.append(generate.get_description())
    return jsonify(descriptions)


@app.route("/")
def redirect_to_correct_api():
    return redirect(url_for("get_description", count=10))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
