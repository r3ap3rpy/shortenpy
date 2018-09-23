from flask import Flask, render_template, request, send_from_directory,abort,redirect
import os
import hashlib
import json

app = Flask(__name__)

@app.errorhandler(404)
def custom404(e):
	return render_template('error.html',error = e.description),404

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsof.icon')

if os.path.isfile(os.path.join(app.root_path, 'static','cache','translate.json')):
	with open(os.path.join(app.root_path, 'static','cache','translate.json'),'r') as cache:
		derefedpages = json.loads(cache.read())
else:
	derefedpages = {}

@app.route('/',methods = ['GET','POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		Calc = hashlib.sha512(request.form.get('url').encode('utf-8')).hexdigest()
		if derefedpages.get((Calc[:4] + Calc[-4:])):			
			stringforderefer = 'http://shortenpy.pythonanywhere.com/deferme?key={}'.format((Calc[:4] + Calc[-4:]))
			
		else:
			derefedpages[(Calc[:4] + Calc[-4:])] = request.form.get('url')
			stringforderefer = 'http://shortenpy.pythonanywhere.com/deferme?key={}'.format((Calc[:4] + Calc[-4:]))
		with open(os.path.join(app.root_path, 'static','cache','translate.json'),'w') as cache:
			cache.write(json.dumps(derefedpages))
		return render_template('index.html',defered = stringforderefer)

		
@app.route('/deferme')
def deferer():

	if request.args.get('key'):
		if derefedpages.get(request.args.get('key')):
			with open(os.path.join(app.root_path, 'static','logs','redirects.txt'),'a') as log:
				log.write('{} :: {} :: {} :: {}\r\n'.format(request.remote_addr,request.url,derefedpages.get(request.args.get('key')),request.user_agent))			
			return redirect(derefedpages.get(request.args.get('key')))
		else:
			return abort(404, description='This page was not ever derefered by this service!')
	else:
		return abort(404, description='You need a key to use the dereferer service!')



if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 8080, debug = True)