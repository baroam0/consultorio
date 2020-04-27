import csv
import sqlite3

from apps.bancos.models import Banco, TipoCuenta
from apps.catalogosenfermedades.models import Catalogo
from apps.obrassociales.models import Nucleador, Prestacion, ObraSocial, NucleadorPrestacion
from apps.pacientes.models import Paciente, TipoDocumento
from apps.profesionales.models import Especialidad

conexion = sqlite3.connect("backupdb.sqlite3")


def carga_banco():
    cursor = conexion.cursor()
    tiposcuentas = cursor.execute(''' SELECT * FROM bancos_tipocuenta ''')
    for i in tiposcuentas.fetchall():
        tipodoc = TipoCuenta(descripcion=str(i[1]), abreviatura=str(i[2]))
        tipodoc.save()
        print("Grabando...")
    cursor.close()

    cursor = conexion.cursor()
    bancos = cursor.execute(''' SELECT * FROM bancos_banco ''')
    for i in bancos.fetchall():
        tipodoc = Banco(descripcion=str(i[1]))
        tipodoc.save()
        print("Grabando...")
    cursor.close()


def carga_cie10():
    a = 1
    with open('cie10.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i in csv_reader:
            catalogo = Catalogo(
                clave=i[0],
                descripcion=i[1]
            )
            catalogo.save()
            print("Grabando... " + str(i[1]))


def carga_obrasocial():
    cursor = conexion.cursor()
    nucleadores = cursor.execute(''' SELECT * FROM obrassociales_nucleador ''')
    for i in nucleadores.fetchall():
        nucleador = Nucleador(descripcion=str(i[1]))
        nucleador.save()
        print("Grabando... " + str(i[1]))
    cursor.close()

    cursor = conexion.cursor()
    prestaciones = cursor.execute(''' SELECT * FROM obrassociales_prestacion ''')
    for i in prestaciones.fetchall():
        prestacion = Prestacion(
            codigo=str(i[1]),
            descripcion=str(i[2]),
        )
        prestacion.save()
        print("Grabando... " + str(i[1]))
    cursor.close()

    cursor = conexion.cursor()
    obrassociales = cursor.execute(''' SELECT * FROM obrassociales_obrasocial ''')
    for i in obrassociales.fetchall():
        obrasocial = ObraSocial(
            descripcion = i[1],
            abreviatura = i[2],
            telefono = i[6],
            telefono_opcional = i[3],
            correo_electronico = i[4],
            observacion = i[5]
            )
        obrasocial.save()
        print("Grabando... " + str(i[1]))
    cursor.close()

    cursor = conexion.cursor()
    nucleadoresprestaciones = cursor.execute(''' SELECT * FROM obrassociales_nucleadorprestacion ''')
    for i in nucleadoresprestaciones.fetchall():
        nucleador = Nucleador.objects.get(pk=i[2])
        obrasocial = ObraSocial.objects.get(pk=i[3])
        prestacion = Prestacion.objects.get(pk=i[4])
        nucleadorprestacion = NucleadorPrestacion(
            nucleador = nucleador, 
            obrasocial = obrasocial, 
            prestacion = prestacion, 
            importe = 1
        )
        nucleadorprestacion.save()
        print("Grabando... " + str(i[1]))
    cursor.close()


def  carga_especialidad():
    cursor = conexion.cursor()
    especialidades = cursor.execute(''' SELECT * FROM profesionales_especialidad ''')
    for i in especialidades.fetchall():
        especialidad = Especialidad(descripcion=str(i[1]))
        especialidad.save()
        print("Grabando... " + str(i))
    cursor.close()


def carga_paciente():
    cursor = conexion.cursor()
    tipodocs = cursor.execute(''' SELECT * FROM pacientes_tipodocumento ''')
    for i in tipodocs.fetchall():
        tipodoc = TipoDocumento(descripcion=str(i[1]))
        tipodoc.save()
        print("Grabando...")
    cursor.close()

    cursor = conexion.cursor()
    pacientes = cursor.execute(''' SELECT * FROM pacientes_paciente ''')
    for i in pacientes.fetchall():
        tipodoc = TipoDocumento.objects.get(pk=i[8])
        paciente = Paciente(
            nombre = i[1], apellido = i[2], tipodocumento = tipodoc,
            numero_documento = i[7], fecha_nacimiento = i[10], 
            telefono = i[3], telefono_opcional = i[4], domicilio = i[5],
            correo_electronico = i[9], ocupacion = i[15], fecha_admision = i[11],
            profesional_tratante = None, medicacion = i[14], fue_al_psicologo = i[12],
            grupo_familiar = i[13], observacion = i[6]
        )
        paciente.save()
        print("Grabando... " + str(i))
    cursor.close()












