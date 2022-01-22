from flask import Flask, render_template, request, session, redirect
import json, requests
from flask_restful import Resource, Api, reqparse
from werkzeug import secure_filename
import os
# import sqlite3 as lite
# from peewee import *

app = Flask(__name__)
api = Api(app)

ALLOWED_EXTENSIONS = {'txt','pdf','png','jpg','jpeg','gif'}
app.secret_key = '!LTENJvvxNeCu46'
app.config['UPLOAD_FOLDER'] = 'static/uploads/siswa'

# DATABASE = "cars.db"
# database = SqliteDatabase(DATABASE)

# class BaseModel(Model):
# 	class Meta:
# 		database = database

# class Cars(BaseModel):
# 	carID = CharField(unique=True)
# 	carBrand = TextField()
# 	carType = TextField()
# 	carPrice = TextField()

# def create_tables():
# 	with database:
# 		database.create_tables([Cars])

class Siswa(Resource):
	def get(self):
		return {'name': 'hilman'}

	def put(self, user_id):
		users[user_id] 

api.add_resource(Siswa,'/siswa')

# 0072635123
@app.route('/')
def index():
	if 'nisn_siswa' in session:
		session_id = session.get('nisn_siswa')
	else:
		session_id = ''

	if 'admin_id' in session:
		admin_id = session.get('admin_id')
	else:
		admin_id = ''
	return render_template('index.html',session_id=session_id,admin_id=admin_id)

@app.route('/cari-siswa', methods=['POST'])
def cari_siswa():
	nisn_formdata = request.form['nisn'];
	alamatserver = "https://spds.mtsn1sidoarjo.sch.id/api/login/"+nisn_formdata
	headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
	siswa = requests.get(alamatserver)

	if 'nisn_siswa' in session:
		session['nisn_siswa'] = session.get('nisn_siswa')
	else:
		session['nisn_siswa'] = siswa.json()['id']
	return redirect('/edit-siswa')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/login-admin', methods=['POST'])
def login_admin():
	username_formdata = request.form['username'];
	password_formdata = request.form['password'];
	alamatserver = "https://spds.mtsn1sidoarjo.sch.id/api/login_admin/"+username_formdata+"/"+password_formdata
	headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
	admin = requests.get(alamatserver)

	if 'admin_id' in session:
		session['admin_id'] = session.get('admin_id')
	else:
		session['admin_id'] = admin.json()['id']
	return redirect('/list-siswa')

@app.route('/edit-siswa')
def edit_siswa():
	if 'nisn_siswa' in session:
		id_siswa = session.get('nisn_siswa')
	else:
		return redirect('/')

	alamatserver = "https://spds.mtsn1sidoarjo.sch.id/api/siswa/"+id_siswa
	headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
	siswa = requests.get(alamatserver)
	return render_template('edit-siswa.html',siswa=siswa.json(),id_siswa=id_siswa)

@app.route('/edit-ortu')
def edit_ortu():
	if 'nisn_siswa' in session:
		id_siswa = session.get('nisn_siswa')
	else:
		return redirect('/')

	alamatserver = "https://spds.mtsn1sidoarjo.sch.id/api/siswa/"+id_siswa
	headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
	ortu = requests.get(alamatserver)
	return render_template('edit-ortu.html',ortu=ortu.json())

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/simpan-siswa', methods=['POST'])
def simpan_siswa():
	if 'nisn_siswa' in session:
		id_siswa = session.get('nisn_siswa')
	else:
		return redirect('/')

	if request.method == 'POST':
		# nama_form = request.form['nama']
		# nisn_form = request.form['nisn']
		# gender_form = request.form['gender']
		# kelas_form = request.form['kelas']
		nik_siswa_form = request.form['nik_siswa']
		anak_ke_form = request.form['anak_ke']
		jumlah_sdr_form = request.form['jumlah_sdr']
		tempat_form = request.form['tempat']
		tgl_lahir_form = request.form['tgl_lahir']
		agama_form = request.form['agama']
		cita_cita_form = request.form['cita_cita']
		# userfile_form = request.form['file']

		f = request.files['userfile']
		f_name = ''
		if f and allowed_file(f.filename):
			f_name = secure_filename(f.filename) 
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
		datasiswa = {
			"nik_siswa" : nik_siswa_form,
			"anak_ke" : anak_ke_form, 
			"jumlah_sdr" : jumlah_sdr_form,
			"tempat" : tempat_form,
			"tgl_lahir" : tgl_lahir_form,
			"agama" : agama_form, 
			"cita_cita" : cita_cita_form,
			"dokumen1" : f_name
		}

		# datasiswa_json = json.dumps(datasiswa)
		alamatserver = "https://spds.mtsn1sidoarjo.sch.id/api/siswa/"+id_siswa+"/1"
		headers = {'Content-Type':'application/json'}
		r = requests.post(alamatserver, json=datasiswa, headers=headers)
		return redirect('/edit-ortu')

@app.route('/simpan-ortu/<ganti_link>', methods=['POST'])
def simpan_ortu(ganti_link=0):
	if 'nisn_siswa' in session:
		id_siswa = session.get('nisn_siswa')
	else:
		return redirect('/')

	if request.method == 'POST':
		nama_ayah_form = request.form['nama_ayah']
		nik_ayah_form = request.form['nik_ayah']
		nama_ibu_form = request.form['nama_ibu']
		nik_ibu_form = request.form['nik_ibu']
		alamat_ortu_form = request.form['alamat_ortu']
		kk_form = request.form['kk']
		# userfile_form = request.form['file']

		f = request.files['userfile']
		f_name = ''
		if f and allowed_file(f.filename):
			f_name = secure_filename(f.filename) 
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
		datasiswa = {
			"nama_ayah" : nama_ayah_form,
			"nik_ayah" : nik_ayah_form,
			"nama_ibu" : nama_ibu_form,
			"nik_ibu" : nik_ibu_form,
			"alamat_ortu" : alamat_ortu_form,
			"kk" : kk_form,
			"dokumen2" : f_name
		}

		# datasiswa_json = json.dumps(datasiswa)
		alamatserver = "https://spds.mtsn1sidoarjo.sch.id/api/siswa/"+id_siswa+"/2"
		headers = {'Content-Type':'application/json'}
		r = requests.post(alamatserver, json=datasiswa, headers=headers)
		if ganti_link == 1:
			return redirect('/edit-siswa')
		else:
			return redirect('/logout')

@app.route('/list-siswa', methods=['GET'])
def list_siswa():
	if 'admin_id' in session:
		admin_id = session.get('admin_id')
	else:
		return redirect('/')

	alamatserver = "https://spds.mtsn1sidoarjo.sch.id/api/siswa"
	headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
	r = requests.get(alamatserver)
	return render_template('list-siswa.html',semuasiswa = r.json())

@app.route('/detail-siswa/<id_siswa>')
def detail_siswa(id_siswa):
	if 'admin_id' in session:
		admin_id = session.get('admin_id')
	else:
		return redirect('/')

	alamatserver = "https://spds.mtsn1sidoarjo.sch.id/api/siswa/"+id_siswa
	headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
	siswa = requests.get(alamatserver)
	return render_template('detail-siswa.html',siswa=siswa.json())

@app.route('/logout')
def logout():
	if 'nisn_siswa' in session:
		session.pop('nisn_siswa',None)
	elif 'admin_id' in session:
		session.pop('admin_id',None)
	return redirect('/')
# @app.route('/add-car-save',methods=['POST'])
# def add_car_save():
# 	carID_form = request.form['dataID']
# 	carBrand_form = request.form['dataBrand']
# 	carType_form = request.form['dataType']
# 	carPrice_form = request.form['dataPrice']
# 	car_entry = Cars.create(
# 			carID = carID_form,
# 			carBrand = carBrand_form,
# 			carType = carType_form,
# 			carPrice = carPrice_form
# 		)
# 	return "Saved!"

if __name__ == '__main__':
	# create_tables()
	app.run(
		host="0.0.0.0",
		debug=True
	)
