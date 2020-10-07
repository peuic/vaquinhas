from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/result', methods=["POST"])
def search():
    name = request.form['name']
    court = request.form['court']
    lawsuit_list = search_candidate(name, court)
    return render_template("result.html", lawsuit_list = lawsuit_list, name=name, court=court)


def search_candidate(name, court):
    formatted_name = name.replace(" ", "%20")
    url = f'https://sedesc1-jud-01.tse.jus.br/mural-consulta-back-end/rest/publicacao/consulta/10/%22{name}%22[part]%20%20e%20(%22{court}%22[trib]%20%20)'
    response = requests.get(url)
    lawsuit_list =  response.json()
    for lawsuit in lawsuit_list['collection']:
        lawsuit['url'] = get_publication_url(lawsuit['id'])
    return lawsuit_list['collection']


def get_publication_url(_id):
    return f"https://sedesc1-jud-01.tse.jus.br/mural-consulta-back-end/rest/publicacao/download/{_id}"


if __name__ == '__main__':
    app.run(debug=True)