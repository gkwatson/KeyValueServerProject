from bottle import Bottle, run, request, HTTPError

app = Bottle()
key_value_store = dict()


@app.post('/set')
def set_endpoint():
    json_dict = request.json
    if not ("key" in json_dict and "value" in json_dict):
        raise HTTPError(status=400, body="Did not receive values for the keys 'key' and 'value' in the json POST")
    else:
        key = str(json_dict["key"])
        value = str(json_dict["value"])
        key_value_store[key] = value
        return f'{{"key": "{key}", "value": "{value}"}}'


@app.get('/get')
def get_endpoint():
    key = request.query.key
    if key is "":
        raise HTTPError(status=400, body="No 'key' provided in query string")
    elif key not in key_value_store:
        raise HTTPError(status=400, body="The provided 'key' has not been set")
    else:
        return f'{{"key": "{key}", "value": "{key_value_store[key]}"}}'


@app.post('/delete')
def delete_endpoint():
    json_dict = request.json
    if not ("key" in json_dict):
        raise HTTPError(status=400, body="Did not receive a value for the key 'key' in the json POST")
    else:
        key = str(json_dict["key"])
        if key not in key_value_store:
            return "The provided key did not exist"
        else:
            del key_value_store[key]
            return f'{{"key": "{key}"}}'


run(app, host='localhost', port=4000)
