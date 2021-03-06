from django.db import transaction
from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .forms import *
from django.core import serializers
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from .models import *

from io import BytesIO
from django.http import HttpResponse
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# Vista para el menu de inicio
def index(request):
    return render(
        request,
        'base/base.html',
    )

#--------------------------------------------------------------------

def consultaCiclo(request):
    ciclo_list=Ciclo.objects.order_by('codigo_ciclo')
    context = {
        'ciclo_list': ciclo_list,
    }
    return render(
        request,
        'app1/Ciclo.html', context
    )

class crearCiclo(CreateView):
    template_name = 'app1/crear_ciclo.html'
    form_class = CicloForm
    success_url = reverse_lazy('proyeccionsocial:consulta_ciclo')

class editarCiclo(UpdateView):
    model = Ciclo
    template_name = 'app1/crear_ciclo.html'
    form_class = CicloForm
    success_url = reverse_lazy('proyeccionsocial:consulta_ciclo')

class eliminarCiclo(DeleteView):
    model = Ciclo
    template_name = 'app1/eliminar_ciclo.html'
    success_url = reverse_lazy('proyeccionsocial:consulta_ciclo')

#--------------------------------------------------------------------

def consultaAlumno(request):
    alumno_list=Alumno.objects.order_by('codigo_alumno')
    context = {
        'alumno_list': alumno_list,
    }
    return render(
        request,
        'app1/Alumno.html', context
    )

class crearAlumno(CreateView):
    template_name = 'app1/crear_alumno.html'
    form_class = AlumnoForm
    success_url = reverse_lazy('proyeccionsocial:consulta_alumno')

class editarAlumno(UpdateView):
    model = Alumno
    template_name = 'app1/crear_alumno.html'
    form_class = AlumnoForm
    success_url = reverse_lazy('proyeccionsocial:consulta_alumno')

class eliminarAlumno(DeleteView):
    model = Alumno
    template_name = 'app1/eliminar_alumno.html'
    success_url = reverse_lazy('proyeccionsocial:consulta_alumno')

 #-----------------------------------------------------------------

class generarpdf(ListView):
    model = Alumno
    template_name = 'app1/Alumno.html'
    context_object_name = 'alumno'
    success_url = reverse_lazy('proyeccionsocial:generar_pdf')  
     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = 'static/img/logoUPSAgro.png'
        archivo_imagen2 = 'static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 740, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 740, 125, 90,preserveAspectRatio=True) 

        #Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        #Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        #el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 790, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 780, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 770, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 760, u"UNIDAD DE PROYECCION SOCIAL")       

    def get_queryset(self, pdf, **kwargs):
        codigo_alumno = self.kwargs.get('codigo_alumno')
        queryset = Alumno.objects.filter(codigo_alumno = codigo_alumno)

        numero = 1

        for i in Alumno.objects.filter(codigo_alumno = codigo_alumno):
            carnet = i.carnet_alumno
            nombre = i.nombre_alumno
            sexo = i.sexo_alumno
            telefono = i.telefono_alumno
            correo = i.correo_alumno
            direccion = i.direccion_alumno
            carrera = i.carrera_alumno
            porc_carrera = i.porc_carr_apro
            und_valor = i.unidades_valorativas
            experiencia = i.experiencias_alumno
            horas_sem = i.horas_semana
            dias_sem = i.dias_semana
            entidad = i.propuesta_entidad
            modalidad = i.propuesta_modalidad
            fecha_inicio = i.fecha_inicio
            aceptado = i.estado_expediente
            motivo = i.motivo
            observaciones = i.observaciones
            ciclo_lect = i.ciclo.ciclo_lectivo

        texto = 'No. Correlativo: %s' % numero
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(450, 720, texto)

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 730, u"F1")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(235, 710, u"SOLICITUD DE SERVICIO SOCIAL")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 690, u"DATOS PERSONALES")

        texto = 'Nombre Completo: %s' % nombre
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 675, texto)

        texto = 'Sexo: %s' % sexo
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 660, texto)

        texto = 'Telefono: %s' % telefono
        pdf.setFont("Helvetica", 10)
        pdf.drawString(150, 660, texto)

        texto = 'Correo: %s' % correo
        pdf.setFont("Helvetica", 10)
        pdf.drawString(330, 660, texto)

        texto = 'Direccion Residencial: %s' % direccion
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 645, texto)

        #Agrega una linea horizontal como division
        pdf.line(60, 630, 560, 630)

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 610, u"ESTUDIO UNIVERSITARIO")

        texto = 'Carrera: %s' % carrera
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 595, texto)

        texto = 'Carnet No.: %s' % carnet
        pdf.setFont("Helvetica", 10)
        pdf.drawString(450, 595, texto)

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 575, u"Estado Academico:")

        texto = 'Porcentaje de la carrera aprobado: %s' % porc_carrera
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 560, texto)

        texto = 'Unidades Valorativas: %s' % und_valor
        pdf.setFont("Helvetica", 10)
        pdf.drawString(280, 560, texto)

        texto = 'Ciclo Lectivo: %s' % ciclo_lect
        pdf.setFont("Helvetica", 10)
        pdf.drawString(450, 560, texto)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 545, u"Experiencia en algunas areas de conocimiento de su carrera: ")

        texto = '%s' % experiencia
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 530, texto)

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 495, u"Tiempo disponible para su desarrollo social: ")

        texto = 'Horas por Semana: %s' % horas_sem
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 480, texto)

        texto = 'Dias por Semana: %s' % dias_sem
        pdf.setFont("Helvetica", 10)
        pdf.drawString(330, 480, texto)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 465, u"Propuesta de la entidad donde realizara su servicio social segun el ambito mencionado en el Manual de ")
        pdf.drawString(60, 450, u"procedimientos del Servicio Social: ")

        texto = '%s' % entidad
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 435, texto)

        #Agrega una linea horizontal como division
        pdf.line(60, 420, 560, 420)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 400, u"Propuesta de modalidad de servicio segun las mencionadas en el Manual de Procedimientos del Servicio ")

        texto = 'Social: %s' % modalidad
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 385, texto)

        texto = 'Fecha de Inicio posible: %s' % fecha_inicio
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 370, texto)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 335, u"Firma del solicitante: ")
        pdf.line(155, 335, 300, 335)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 305, u"Ciudad Universitaria, ")
        pdf.line(155, 305, 200, 305)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(210, 305, u"de")
        pdf.line(230, 305, 320, 305)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(330, 305, u"del ")
        pdf.line(350, 305, 410, 305)

        #Agrega una linea horizontal como division
        pdf.line(60, 285, 560, 285)

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 265, u"PARA USO EXCLUSIVO DE PROYECCION SOCIAL ")

        texto = 'Aceptado: %s' % aceptado
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 245, texto)

        texto = 'Motivo: %s' % motivo
        pdf.setFont("Helvetica", 10)
        pdf.drawString(200, 245, texto)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 225, u"Observaciones: ")

        texto = '%s' % observaciones
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 210, texto)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(generarpdf, self).get_context_data(**kwargs)
        codigo_alumno = self.kwargs.get('codigo_alumno')
        context['codigo_alumno'] = codigo_alumno
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "ListadoInstrumentos.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response