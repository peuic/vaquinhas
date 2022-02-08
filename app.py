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
    url = 'https://sedesc1-jud-01.tse.jus.br/mural-consulta-back-end/rest/publicacao/consulta/'
    data_raw = '{"texto":"\\"PARTE\\"[part]  e (\\"TRIBUNAL\\"[trib]  )","quantidade":5,"token":"03AGdBq27N9ynk8l4tUjPw9WR6rvXDppSK_vFL51UXE5umgG4OVTDjka83aK-2qsBQwW0CgW57LMB96DuhGg_6CYB0IlFitYMje2Sy5uM6dl2wJNqKLJvKcqkW7zfL4R-WA9uEvCyy3rpcu3EeuNU4drSRrpfGKO5vb-CphiL9C6eIgtMpdDSTzMGS9Mimwgr78uyi2JH6moJG4LEjY84RqA8StSv2eH2o8EFf_6t_PTA7bsQI5sE_remUzih1PZaS7ICXTj3ufJIZaGtOP2Vm_AZkmL-op1A1vl-GitO9Vb3D3xlOSd7lcq9RebnyxJOb0fwfCs_bcl9INWOkIRvdyczKPAN496HF0aAurWBpQkEJQgqe_fBYQZWYjoX0_yMtq0OqNH5rJ9CtJHNJOfejG1wijwxUXJOyx-VHItL2VTTjh3MM3mz0oNRNkHavyMjdqtruXy1rXyuYEC05AI9HDAb38Y9sefV-WOxAxBhv5k-Lp6iZ1vRxv391sZsCgH5dNzPMTr09bhnFUF6EIYqo12f53KET0-u07etb9AZxfGEjEy3MTxelwhuU7mYjAPWqwmz8ln0LKQ6Ez8MepKukCngxFITcVql-FPwG5mORKR3K5HJmQwqjzFex3lmGKBJlp1BWbG46KZStpIlm_JkpbK0EMukOLjccihGVR1JhuVSW92UQR_V77ZfouqCltwANFKdQhVP15lyuSgvYPWBq5Fp3nDEmmTKsUOm-_1DE5LzPVUuY9DrsWfjyOwa0GrEeO7PaYp-T8lTa6kYsFCMOhhB2klEVB1lIgGMC9UKfPwV7BqczYzD_6xwuBX5QMizPAN-yxU6HeGJakB2D3AQfgF9m4nRbQHTUKk_7O9X9bJ5HIzXqfkn_9yRxYCQihXqercFSun2mfMJkd4ygVW8Ud942muorbCp3Ok6kllPwwL1kN7tVtg9sSptBVXzcETkorAyPlrMajCK9MB9XvcutI72mPkctnaourBdB9U6mTM1Le4aA0qBtylnPMPKPD0Quh1ZFFb0q8Soff4MhYKa6AGZ1VWYn3AbaXJhfZryg84pabQ5P4UMUx7cFqbgQ5vd1Lam3s-JSf5J6vuOKbIsX3kxedI_hDt1BXh8E1kuxfn4et-bIeKuOOmme8mPq__tg4UIe6P5zx8EmsymCxqo5SNShTxBfAm-daVC7Nx-gyPrAW9cHc-4qHoFNynhrZqZ09WtWFJ677zAt8xytFkH17Vu3Wn55DCoiAm3WWgr7W-V9WSz7dHdMgFs"}'
    data = data_raw.replace("PARTE", name).replace("TRIBUNAL", court)

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'Origin': 'https://mural-consulta.tse.jus.br',
        'Referer': 'https://mural-consulta.tse.jus.br/',
    }
    response = requests.post(url, headers=headers, data=data)

    lawsuit_list =  response.json()
    for lawsuit in lawsuit_list['collection']:
        lawsuit['url'] = get_publication_url(lawsuit['id'])

    return lawsuit_list['collection']


def get_publication_url(_id):
    return f"https://sedesc1-jud-01.tse.jus.br/mural-consulta-back-end/rest/publicacao/download/{_id}"


if __name__ == '__main__':
    app.run(debug=True)