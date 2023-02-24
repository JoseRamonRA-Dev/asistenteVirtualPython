import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia


'''
engine = pyttsx3.init()
for voz in engine.getProperty('voices'):
    print(voz)
'''
#Para confirgurar el idioma, los ids se extrajeron del for anterior
#Opciones de voz
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


# Esuchar el microfono y devolver el audio como texto
def transfromar_audio_en_texto():
    #Almacenar el recognize en variable
    r = sr.Recognizer()
    #Configurar el micro
    with sr.Microphone() as origen:
        #Tiempo de espera
        r.pause_threshold = 0.8

        #Infromar que comenzo la grabación
        print("Ya púedes hablar")

        #Guardar el audio
        audio = r.listen(origen)

        try:
            #Buscar en google lo que ha escuchado
            pedido = r.recognize_google(audio,language="es-mx")

            #Preuba de que pudo ingrtesar
            print("Dijiste: " + pedido)

            #Devolver lo que tiene pedido
            return pedido
        #En caso de no reconocer el audio
        except sr.UnknownValueError:
            #Prueba de que no comprendio el audio
            print("No entendi lo que dijiste")
            return "Sigo esperando"
        #No puede transfromar el audio en string
        except sr.RequestError:
            print("No hay servicio")
            return "Sigo esperando"
        #Error inesperado
        except:
            print("Algo ha salido mal ")
            return "Sigo esperando"

#transfromar_audio_en_texto()

#Funcion para que el asistente pudea ser escuchado
def hablar(mensaje):

    #Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)
    #Pronuciar el texto
    engine.say(mensaje)
    engine.runAndWait()

#Funcion para infromar el dia de la semana
def dia_semana():
    dia = datetime.date.today()
    #Para extraer el dia de la semana
    dia_semana = dia.weekday()
    #DICCIONARIO PARA EL NOMBRE DE LOS DIAS
    calendario = {0:'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo',
                  }
    #Asistente pueda decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


def pedir_hora():
    #Variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las: {hora.hour} horas con {hora.minute} minutos con {hora.second}'
    hablar(hora)


#Para el saludo inicial
def saludo_inicial():
    #Crear variable con datos de la hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour>20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'

    hablar(f'{momento}, soy Reymontin, tu asistente personal. Dime en que te puedo ayudar')

#Funcion central del asistente
def pedir_cosas():
    saludo_inicial()

    #Variable para terminar el loop
    comenzar = True

    while comenzar:
        #Activar el micro y guardar el pedido
        pedido = transfromar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo youtube.')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Con gusto, estoy abriendo el navegador.')
            webbrowser.open('https://www.google.com.mx/')
            continue
        elif 'qué día es hoy' in pedido:
            dia_semana()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando en wikipedia')
            pedido = pedido.replace('busca en wikipedia','')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Estoy en eso')
            pedido = pedido.replace('busca en internet','')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')

        elif 'reproducir' in pedido:
            hablar('Vale, empiezo a reproducir')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma'  in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera ={'apple':'APPL',
                      'amazon':'AMZN',
                      'google':'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion}, es: {precio_actual}')
                continue
            except:
                hablar('Perdón pero aun no le he encontrado. ')
                continue
        elif 'adiós' in pedido:
            hablar('Me voy a descansar, cualquier cosa me avisas')
            break


pedir_cosas()