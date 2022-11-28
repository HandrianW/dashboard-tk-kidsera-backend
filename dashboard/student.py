import json
from bson.json_util import dumps
from flask import Blueprint, request
from .db import insert_student, get_student, getAll_student, update_student, delete_student
from bson.objectid import ObjectId
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required
from datetime import datetime


bp = Blueprint('students',__name__)
api = Api(bp)

class Students(Resource):
    # @jwt_required()
    def get(self):
        data = getAll_student()
        return json.loads(dumps(data))

    # @jwt_required()
    def post(self):
        today = datetime.now().strftime("%d/%m/%Y")
        req = request.form
        data = {
            'nama' : req['nama'],
            'jenis_kelamin' : req['jenis_kelamin'], 
            'nisn' : req['nisn'], 
            'nik' : req['nik'], 
            'no_kk' : req['no_kk'], 
            'tingkat_kelas' : req['tingkat_kelas'], 
            'id_rombongan_belajar' : int(req['id_rombongan_belajar']), 
            'tanggal_masuk' :req['tanggal_masuk'],
            'tanggal_lulus' :req['tanggal_lulus'],
            'nomor_induk' : req['nomor_induk'],
            'status' : req['status'],
            'tinggi_badan' : int(req['tinggi_badan']),
            'berat_badan' : int(req['berat_badan']),
            'lingkar_kepala' : int(req['lingkar_kepala']),
            'alergi' : req['alergi'],
            'nama_ayah' : req['nama_ayah'],
            'nama_ibu' : req['nama_ibu'],
            'pekerjaan_ayah' : req['pekerjaan_ayah'],
            'pekerjaan_ibu' : req['pekerjaan_ibu'],
            'created_at' : today
        }
        insert_student(data)
        return {'Success': True}

api.add_resource(Students, '/API/students')


class Student(Resource):
    # @jwt_required()
    def get(self, student_id):
        id = student_id
        ObjInstance = ObjectId(id)
        filter = {'_id' : ObjInstance}
        data = get_student(filter)
        return json.loads(dumps(data))
    
    # @jwt_required()
    def put(self, student_id):
        ObjInstance = ObjectId(student_id)
        filter = {'_id':ObjInstance}
        if (get_student(filter) is None):
            return {"message":"ID tidak valid"}
        else:
            req = request.form
            name = req.get("nama")
            newVal = {
                "$set":{
                    "name":req.get("nama"),
                    "sex":req.get("jenis_kelamin"),
                    "nik":req.get("nik"),
                    "kk":req.get("kk"),
                    "level":req.get("tingkat"),
                    "studyGroup":req.get("rombel"),
                    "dateIn":req.get("tanggal_masuk"),
                    "dateOut":req.get("tanggal_keluar"),
                    "nipd":req.get("nipd"),
                    "status":req.get("status"),
                    "height":req.get("tinggi"),
                    "weight":req.get("berat"),
                    "head_circumference":req.get("lingkar_kepala"),
                    "alergi":req.get("alergi"),
                }
            }

            update_student(filter, newVal)
            return {"success":True}

    # @jwt_required()
    def delete(self, student_id):
        ObjInstance = ObjectId(student_id)
        filter = {'_id':ObjInstance}
        data = delete_student(filter)
        return {"success":True}

api.add_resource(Student, '/API/students/<student_id>')
