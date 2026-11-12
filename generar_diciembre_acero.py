import os
import sys
import json
import random
from datetime import datetime, timedelta

sys.path.append(r"D:\github\publicador_facebook")
from disenador_acero_v2 import (
    generar_imagen_despertador,
    generar_imagen_contraste,
    generar_imagen_estrategia,
    generar_imagen_auditoria
)

base_dir = r"D:\github\publicador_facebook"
img_out_dir = os.path.join(base_dir, "mentalidad_de_acero", "imagenes")
bg_dir = os.path.join(base_dir, "mentalidad_de_acero", "assets_diciembre")
os.makedirs(img_out_dir, exist_ok=True)

# Lista de fondos descargados
BGS_STATUE = [os.path.join(bg_dir, f) for f in ["bg_statue_1.jpg", "bg_statue_2.jpg", "bg_roman_1.jpg", "bg_roman_2.jpg"]]
BGS_WARRIOR = [os.path.join(bg_dir, f) for f in ["bg_warrior_1.jpg", "bg_warrior_2.jpg", "bg_boxing_1.jpg", "bg_boxing_2.jpg"]]
BGS_NATURE = [os.path.join(bg_dir, f) for f in ["bg_mountain_1.jpg", "bg_mountain_2.jpg", "bg_stormy_1.jpg", "bg_stormy_2.jpg"]]
BGS_BEAST = [os.path.join(bg_dir, f) for f in ["bg_lion_1.jpg", "bg_lion_2.jpg", "bg_wolf_1.jpg", "bg_wolf_2.jpg"]]

# 31 REGLAS INQUEBRANTABLES (07:00 AM)
REGLAS_MATUTINAS = [
    ("Gana la primera hora y conquistarás el día entero", "Tu cama no es un refugio, es una trampa si te quedas en ella."),
    ("La disciplina es el puente entre tus metas y tus logros", "Sin constancia, el talento más brillante es solo basura."),
    ("Nadie te debe nada, el mundo no tiene deudas contigo", "Si quieres respeto, conquista tu lugar con resultados."),
    ("El dolor del esfuerzo dura minutos, el del arrepentimiento dura toda la vida", "Paga el precio temprano y sonríe al final."),
    ("No negocies con la mediocridad en tu cabeza", "Al primer segundo de duda, actúa con violencia positiva."),
    ("El hombre disciplinado es el único verdaderamente libre", "Quien no se domina a sí mismo será dominado por otros."),
    ("La motivación es una chispa, el hábito es un incendio", "No busques inspiración; forja una rutina de hierro."),
    ("Si te rindes hoy, todo el sacrificio anterior habrá sido en vano", "El fracaso solo existe cuando decides no levantarte."),
    ("El silencio es el mejor escudo del que está construyendo", "No le cuentes al mundo lo que vas a hacer; muéstralo."),
    ("Tus excusas no pagan las cuentas ni construyen imperios", "A nadie le importa por qué fallaste, solo si lo lograste."),
    ("El estándar que aceptas es el estándar que mereces", "Deja de tolerar tu propia pereza y tus quejas internas."),
    ("La incomodidad es el precio de la transformación", "Si todo es fácil en tu día, estás yendo en reversa."),
    ("Sé implacable con tus debilidades y compasivo con tu progreso", "No te mientas al mirarte al espejo por la mañana."),
    ("La consistencia mediocre supera a la intensidad esporádica", "Hacer lo básico todos los días te hace imparable."),
    ("El respeto no se mendiga en redes, se forja en soledad", "Lo que haces cuando nadie te mira define tu grandeza."),
    ("El miedo es una brújula: camina hacia donde más te asusta", "Del otro lado del pánico está tu mejor versión."),
    ("No bajes la meta, sube el esfuerzo y la disciplina", "Si la cima parece lejana, aprieta los dientes y acelera."),
    ("Tus hábitos diarios son los votos por tu destino futuro", "Cada decisión matutina te acerca a la cima o al barro."),
    ("La suerte favorece a la mente preparada y obstinada", "Cuanto más trabajo en silencio, más 'suerte' tengo."),
    ("El tiempo es el único recurso que nunca recuperarás", "No regales tus horas a personas o pantallas vacías."),
    ("Sé el arquitecto de tu vida o serás el peón de otros", "Si no tienes un plan propio, trabajarás en el de alguien más."),
    ("La presión no te rompe, la presión revela de qué estás hecho", "El carbón bajo fuego y presión se convierte en diamante."),
    ("Aprende a amar el aburrimiento del trabajo repetitivo", "Los maestros repiten lo básico miles de veces sin quejarse."),
    ("Tu palabra debe valer más que cualquier contrato legal", "Si prometiste hacer algo, cúmplelo aunque te cueste sangre."),
    ("El verdadero poder es la serenidad ante la tormenta", "No reacciones con rabia; responde con fría estrategia."),
    ("El conformismo es un veneno con sabor a tranquilidad", "Nunca te sientas cómodo con ser simplemente promedio."),
    ("Entrena tu mente para encontrar soluciones, no culpables", "El hombre débil señala afuera; el fuerte asume el mando."),
    ("Tu competencia no duerme mientras tú buscas atajos", "Cada hora desperdiciada es ventaja para tu rival."),
    ("La humildad para aprender y la soberbia para ejecutar", "Escucha al sabio en silencio y arrasa en el campo."),
    ("La vida no se vuelve más fácil, tú te vuelves más fuerte", "No pidas cargas livianas, pide espaldas anchas."),
    ("Termina el año como un guerrero, no como un espectador", "Diciembre no es para aflojar; es para tomar ventaja.")
]

# 31 ARQUETIPOS DE CONTRASTE (12:30 PM)
BATALLAS_CONTRASTE = [
    {
        "arquetipo": "El Adicto a la Comodidad",
        "debil": ["Huye del esfuerzo", "Pide atajos fáciles", "Se rinde al primer dolor", "Culpa a la economía", "Perezoso crónico", "Sueña sin actuar"],
        "acero": ["Abraza la fricción", "Paga el precio diario", "Persiste hasta vencer", "Dueño de su destino", "Hábitos inquebrantables", "Ejecuta en silencio"],
        "sentencia": "La comodidad es la tumba donde mueren los hombres sin propósito."
    },
    {
        "arquetipo": "El Crítico de Sillón",
        "debil": ["Opina de vidas ajenas", "Juzga desde el sofá", "Envidioso pasivo", "Nunca arriesga nada", "Experto en quejarse", "Cero resultados"],
        "acero": ["Enfocado en su obra", "Ignora el ruido externo", "Aplaude al que lucha", "Arriesga y construye", "Resuelve en silencio", "Resultados masivos"],
        "sentencia": "El crítico nunca tiene un monumento; el que construye la historia es quien sangra en la arena."
    },
    {
        "arquetipo": "El Negociador de Principios",
        "debil": ["Se vende por poco", "Cambia de valores por dinero", "Falso con sus amigos", "Traidor en silencio", "Justifica su bajeza", "Sin honor propio"],
        "acero": ["Valores innegociables", "El honor sobre el oro", "Leal hasta la muerte", "Firme en la tormenta", "Verdad ante todo", "Código de hierro"],
        "sentencia": "Un hombre sin código es una cáscara vacía que cualquier viento derrumba."
    },
    {
        "arquetipo": "El Prisionero del Qué Dirán",
        "debil": ["Teme al juicio ajeno", "Viste para agradar", "Censura sus sueños", "Paralizado por burlas", "Depende de la aprobación", "Vive encadenado"],
        "acero": ["Indiferente a la opinión", "Auténtico y firme", "Persigue su visión", "Usa la burla como nafta", "Autoestima blindada", "Libre y soberano"],
        "sentencia": "Quien teme al qué dirán ya cavó su propia tumba en vida."
    },
    {
        "arquetipo": "El Aplazador Serial",
        "debil": ["'El lunes empiezo'", "Espera la fecha perfecta", "Colecciona excusas", "Mente en el mañana", "Miedo al compromiso", "Vida postergada"],
        "acero": ["'Empiezo ahora mismo'", "Crea su propio momento", "Destruye excusas", "Mente en el presente", "Compromiso al 100%", "Vida conquistada"],
        "sentencia": "El cementerio está repleto de personas que iban a empezar 'mañana'."
    },
    {
        "arquetipo": "El Frágil por Afecto",
        "debil": ["Mendiga atención", "Pierde el rumbo por desamor", "Dependiente emocional", "Se destruye en soledad", "Sin propósito mayor", "Esclavo del cariño"],
        "acero": ["Completo en soledad", "El amor es compañía, no ancla", "Propósito inamovible", "Crece en el silencio", "Dignidad blindada", "Dueño de sus emociones"],
        "sentencia": "Primero sé un hombre completo; nadie puede rescatarte de ti mismo."
    },
    {
        "arquetipo": "El Coleccionista de Culpables",
        "debil": ["Culpa a sus padres", "Culpa al gobierno", "Culpa a su expareja", "Eterna víctima del mundo", "Sin poder de cambio", "Amargura constante"],
        "acero": ["100% responsable", "Acepta las cartas dadas", "Juega para ganar", "Transforma el dolor", "Poder absoluto de acción", "Gratitud y conquista"],
        "sentencia": "En el momento en que culpas a otro, le entregas las llaves de tu libertad."
    },
    {
        "arquetipo": "El Adicto a la Dopamina Rápida",
        "debil": ["Horas en TikTok", "Pornografía y placer fácil", "Cerebro frito y sin foco", "Impaciente y ansioso", "Cero capacidad de espera", "Ruina invisible"],
        "acero": ["Ayuno de distracciones", "Gratificación aplazada", "Enfoque láser profundo", "Paciencia estratégica", "Construye a largo plazo", "Mente afilada"],
        "sentencia": "El placer barato de hoy es la condena de esclavitud de mañana."
    },
    {
        "arquetipo": "El Reclamador sin Aporte",
        "debil": ["Exige derechos", "Pide aumento sin mérito", "Se cree merecedor de todo", "Da lo mínimo posible", "Se queja de la paga", "Mentalidad de escasez"],
        "acero": ["Aporta valor masivo", "Insuperable en rendimiento", "Se vuelve indispensable", "Entrega el 120%", "Crea su propia abundancia", "Mentalidad de conquista"],
        "sentencia": "No pidas que el fuego te caliente si antes no pusiste la leña."
    },
    {
        "arquetipo": "El Derrotista Prematuro",
        "debil": ["Al primer error frena", "Se autocompadece", "Busca consuelo en débiles", "Convierte tropiezos en fin", "Duda de su capacidad", "Abandona el barco"],
        "acero": ["El tropiezo es lección", "Se levanta de inmediato", "Busca consejos de titanes", "Convierte fallas en armas", "Confianza en su forja", "Capitán inquebrantable"],
        "sentencia": "Caerse está permitido; quedarse en el piso es una elección cobarde."
    },
    {
        "arquetipo": "El Simulador de Éxito",
        "debil": ["Apariencia sin sustento", "Deudas por mostrar estatus", "Foto de lujo, cuenta en cero", "Alardea de proyectos", "Vive en el teatro", "Vacío interior"],
        "acero": ["Riqueza en silencio", "Austero y disciplinado", "Patrimonio real y seguro", "Ejecuta sin alardear", "Realidad sin filtros", "Poder verdadero"],
        "sentencia": "El que de verdad tiene poder no necesita gritarlo; su presencia lo dice todo."
    },
    {
        "arquetipo": "El Indeciso Crónico",
        "debil": ["Parálisis por análisis", "Pide mil opiniones", "Teme al compromiso", "Pierde oportunidades", "Flota sin rumbo", "Miedo a errar"],
        "acero": ["Decisiones rápidas y firmes", "Confía en su criterio", "Asume el riesgo", "Crea oportunidades", "Rumbo fijo a la meta", "Aprende y corrige"],
        "sentencia": "Una mala decisión ejecutada con fuerza es mejor que la parálisis eterna."
    },
    {
        "arquetipo": "El Esclavo del Clima Emocional",
        "debil": ["Trabaja si amaneció bien", "Se nubla y se deprime", "Inestable como veleta", "Sin control de impulsos", "Depende de motivación", "Vida montaña rusa"],
        "acero": ["Trabaja llueva o truene", "Su sol interior no depende del cielo", "Estable como roca", "Dominio absoluto mental", "Disciplinado sin excusa", "Vida en ascenso constante"],
        "sentencia": "El clima no manda en tu vida; en tu reino interior, tú eres la ley."
    },
    {
        "arquetipo": "El Rencoroso Amargado",
        "debil": ["Guarda odio del pasado", "Gasta energía en venganza", "Veneno en el corazón", "Se desgasta en rencores", "Revive viejas heridas", "Prisionero del ayer"],
        "acero": ["Perdona por su propia paz", "Usa la energía en crear", "Corazón libre de veneno", "Avanza hacia el futuro", "Cierra ciclos con poder", "Dueño del presente"],
        "sentencia": "El rencor es tomar veneno y esperar que muera el otro. Suelta la basura."
    },
    {
        "arquetipo": "El Hablador de Sueños",
        "debil": ["Promete a todo el mundo", "Grandes discursos en fiestas", "Mucha espuma, poco chocolate", "Planes que nunca arrancan", "Se cree sus mentiras", "Cero ejecuciones"],
        "acero": ["Boca cerrada, puños listos", "Silencio en las fiestas", "Hechos contundentes", "Planes ejecutados a sangre", "Verdad insobornable", "Obras completas"],
        "sentencia": "El mundo no premia tus intenciones; el mundo se inclina ante tus resultados."
    },
    {
        "arquetipo": "El Cobarde ante el Conflicto",
        "debil": ["Sonríe por compromiso", "Teme decir 'no'", "Acepta faltas de respeto", "Traga rabia en silencio", "Se minimiza para encajar", "Pierde el respeto propio"],
        "acero": ["Límites claros y firmes", "Dice 'no' con seguridad", "Corta la falta de respeto ya", "Sereno pero contundente", "Orgulloso de su postura", "Respetado por amigos y rivales"],
        "sentencia": "Aprender a decir 'NO' con firmeza es el primer paso para ganar el respeto del mundo."
    },
    {
        "arquetipo": "El Cazador de Atajos Financieros",
        "debil": ["Cae en estafas piramidales", "Quiere dinero sin trabajar", "Cero educación financiera", "Gasta antes de ganar", "Eterno endeudado", "Pánico a la pobreza"],
        "acero": ["Construye habilidades reales", "Trabajo honesto y pesado", "Educación financiera diaria", "Invierte y multiplica", "Libertad financiera real", "Certeza de abundancia"],
        "sentencia": "No busques el billete rápido; conviértete en una persona tan valiosa que el dinero te persiga."
    },
    {
        "arquetipo": "El Envidioso del Éxito Ajeno",
        "debil": ["Minimiza los logros de otros", "Dice 'tuvo suerte'", "Le duele ver ganar al vecino", "Se alegra del fracaso ajeno", "Venenoso y tóxico", "Miserable por dentro"],
        "acero": ["Aplaude al que triunfa", "Estudia al que ganó", "Aprende de los mejores", "Se enfoca en su propia carrera", "Inspirado por gigantes", "Grande por dentro"],
        "sentencia": "La envidia es el tributo que la mediocridad le rinde al talento."
    },
    {
        "arquetipo": "El Amante de la Rutina Cómoda",
        "debil": ["Diez años en el mismo empleo mediocre", "Miedo al cambio", "Sin aspiración de mejora", "Acepta migajas", "Cero riesgo", "Muerte en vida"],
        "acero": ["Evolución constante", "Abraza el cambio como forja", "Aspiración a la excelencia", "Construye su legado", "Riesgo calculado", "Vida con propósito"],
        "sentencia": "La zona de confort es un ataúd acolchado donde te entierras vivo."
    },
    {
        "arquetipo": "El Quebrado por la Presión",
        "debil": ["Grita ante el caos", "Pierde la cabeza en crisis", "Contagia pánico", "Toma pésimas decisiones", "Se desmorona ante retos", "Cero templanza"],
        "acero": ["Respira hondo en la crisis", "Mente fría y calculadora", "Transmite calma y mando", "Decide con precisión quirúrgica", "Crece en la adversidad", "Templanza de acero"],
        "sentencia": "Cualquiera sabe gobernar en mar calmo; el verdadero capitán se demuestra en la tempestad."
    },
    {
        "arquetipo": "El Ego Inflado sin Base",
        "debil": ["Se cree Dios sin haber ganado nada", "No acepta consejos", "Cierra su mente al aprendizaje", "Arrogante con los débiles", "Sumiso ante los fuertes", "Ignorante con corona de cartón"],
        "acero": ["Humilde alumno de la vida", "Aprende de cualquiera", "Mente de aprendiz eterno", "Respetuoso con todos", "Firme ante tiranos", "Sabio con armadura real"],
        "sentencia": "El ego es el anestésico que embrutece el dolor de tu propia estupidez."
    },
    {
        "arquetipo": "El Rebelde sin Causa",
        "debil": ["Rompe reglas por llamar la atención", "Lucha contra todo sin plan", "Rebelde de teclado", "Cero impacto real", "Victimismo disfrazado de rebeldía", "Ruido sin fruto"],
        "acero": ["Domina el sistema desde adentro", "Lucha por una visión clara", "Guerrero de trinchera", "Impacto masivo real", "Poder forjado con disciplina", "Victoria contundente"],
        "sentencia": "Quejarte de las reglas te hace débil; aprenderlas, dominarlas y cambiarlas te hace inmortal."
    },
    {
        "arquetipo": "El Perezoso del Fin de Semana",
        "debil": ["Vive esperando el viernes", "Lunes con cara de velorio", "Cinco días sufriendo, dos ebrio", "Desperdicia 104 días al año", "Vida hipotecada", "Eterno prisionero"],
        "acero": ["Ama sus lunes de conquista", "Usa el fin de semana para ganar ventaja", "Entrena y crea todos los días", "No necesita escapar de su vida", "Vida elegida con pasión", "Eternamente libre"],
        "sentencia": "Si odias tus lunes y vives para el viernes, no tienes una vida: tienes una sentencia."
    },
    {
        "arquetipo": "El Maldecidor del Destino",
        "debil": ["'¿Por qué a mí?'", "Se queja de la mala suerte", "Maldice su origen", "Espera un milagro ajeno", "Resignado a la mediocridad", "Espíritu vencido"],
        "acero": ["'Ponme a prueba de nuevo'", "Usa la mala suerte como combustible", "Honra su origen superándolo", "Él es su propio milagro", "Hambre voraz de gloria", "Espíritu indomable"],
        "sentencia": "No le pidas al destino un camino fácil; pídele el coraje para destrozar cualquier obstáculo."
    },
    {
        "arquetipo": "El Falso Amigo en las Buenas",
        "debil": ["Aparece en la fiesta", "Desaparece en el hospital", "Te envidia en silencio", "Habla a tus espaldas", "Chupa tu energía", "Parásito social"],
        "acero": ["Filtro de hierro en su círculo", "Pocos hermanos leales", "Apoya en la trinchera", "Habla de frente con verdad", "Suma y multiplica valor", "Hermandad de honor"],
        "sentencia": "Mejor un león solitario que caminar rodeado de hienas que esperan tu caída."
    },
    {
        "arquetipo": "El Exigente con Otros, Flojo Consigo",
        "debil": ["Pide puntualidad y llega tarde", "Pide honestidad y miente", "Exige esfuerzo y hace nada", "Juez implacable ajeno", "Cómplice de sus faltas", "Hipocresía pura"],
        "acero": ["Predica con el ejemplo", "Llega antes que todos", "Verdad absoluta en sus actos", "Se exige 10 veces más que a otros", "Juez severo de sí mismo", "Integridad intachable"],
        "sentencia": "El liderazgo no se impone con gritos; el liderazgo se gana siendo el primero en la línea de fuego."
    },
    {
        "arquetipo": "El Resentido con el Dinero",
        "debil": ["'Los ricos son malos'", "Justifica su quiebra con moral", "Teme al éxito financiero", "Ataca al que prospera", "Eterno quebrado mental", "Cadenas de escasez"],
        "acero": ["El dinero es un amplificador", "Crea riqueza para servir y blindar", "Aprende las leyes del capital", "Honra el fruto del esfuerzo", "Mente de abundancia", "Libertad financiera"],
        "sentencia": "La pobreza material se supera trabajando; la pobreza mental de odiar al próspero es una condena eterna."
    },
    {
        "arquetipo": "El Temeroso al Sacrificio",
        "debil": ["Quiere músculos sin sudar", "Quiere dinero sin ahorrar", "Quiere paz sin dominar la mente", "Paga con excusas", "Mendigo de triunfos", "Fracaso seguro"],
        "acero": ["Paga la cuota completa", "Suda en silencio cada día", "Renuncia al placer inmediato", "Paga con disciplina", "Conquistador de cimas", "Triunfo inevitable"],
        "sentencia": "Todo lo que vale la pena en esta vida tiene una etiqueta de precio llamada sacrificio."
    },
    {
        "arquetipo": "El Adicto a la Tragedia",
        "debil": ["Ama el drama y el chisme", "Crea problemas donde no hay", "Adicto al conflicto tóxico", "Atrae ruina a su entorno", "Amigo de la queja", "Energía destructiva"],
        "acero": ["Cero tolerancia al drama", "Mente orientada a la solución", "Ambiente de paz y trabajo", "Atrae victoria y orden", "Amigo de la serenidad", "Energía constructiva"],
        "sentencia": "Corta de raíz a la gente dramática; tu paz mental es demasiado costosa para regalarla a la histeria."
    },
    {
        "arquetipo": "El Conformista del 'Así Soy Yo'",
        "debil": ["'Yo nací así y no voy a cambiar'", "Justifica su toxicidad", "Cierra las puertas al crecimiento", "Se aferra a sus defectos", "Orgulloso de su ignorancia", "Evolución cero"],
        "acero": ["'Hoy seré mejor que ayer'", "Destruye sus defectos viejos", "Abre su mente a la evolución", "Se reinventa en el fuego", "Humilde ante la sabiduría", "Evolución infinita"],
        "sentencia": "Decir 'así soy yo' es la confesión más cobarde de un hombre que se rindió consigo mismo."
    },
    {
        "arquetipo": "El Hombre sin Misión",
        "debil": ["Flota como hoja al viento", "Vive para comer y dormir", "Sin metas a 5 años", "Sin fuego en los ojos", "Cualquier camino le da igual", "Espectador de la historia"],
        "acero": ["Misión grabada en piedra", "Vive para dejar un legado", "Visión clara y obsesiva", "Fuego inextinguible en el alma", "Camino forjado a golpes", "Protagonista de su era"],
        "sentencia": "Un hombre sin misión es presa fácil de cualquier trampa. Encuentra tu causa y muere por ella si es necesario."
    }
]

# 31 LEYES DE GUERRA & ESTRATEGIA (17:30 PM)
LEYES_ESTRATEGIA = [
    ("Ley del Silencio y Enfoque", "Nunca reveles tus planes hasta que tus resultados hagan ruido", [
        ("Silencio Absoluto", "No regales tu energía explicando tus metas a mediocres."),
        ("Acción Implacable", "El trabajo diario habla más alto que mil palabras vacías."),
        ("Impacto Inesperado", "Golpea con resultados cuando nadie lo esté esperando.")
    ]),
    ("Ley del Dominio Emocional", "Quien pierde la calma entrega el poder de la batalla", [
        ("Mente de Hielo", "No tomes decisiones cuando estés furioso o eufórico."),
        ("Respuesta Fría", "El insulto ajeno solo tiene poder si tú decides ofenderte."),
        ("Control Total", "Quien domina su propia respiración domina la situación.")
    ]),
    ("Ley de la Inversión en Uno Mismo", "Tu mejor activo no es un negocio, eres tú mismo", [
        ("Educación Diaria", "Lee libros que te hagan ganar ventaja mental."),
        ("Salud Blindada", "Un cuerpo débil alberga una mente cobarde. Entrena duro."),
        ("Habilidades Clave", "Aprende lo que pocos saben y serás insustituible.")
    ]),
    ("Ley de la Soledad Productiva", "Los grandes imperios se forjan en el aislamiento y la oscuridad", [
        ("Aprende a estar solo", "Quien teme a la soledad se conforma con cualquier compañía."),
        ("Forja en el Silencio", "Las horas nocturnas y matutinas son tu taller secreto."),
        ("Claridad Estratégica", "El ruido social no te deja escuchar tu propia intuición.")
    ]),
    ("Ley de la Adaptabilidad Implacable", "El roble rígido se quiebra; el agua toma la forma de la copa y arrasa", [
        ("Cero Quejas", "Si las reglas cambiaron, aprende a ganar con las nuevas reglas."),
        ("Pivota con Rapidez", "No te enamores de una idea fallida; enamórate de ganar."),
        ("Firme en la Meta", "Cambia el camino mil veces, pero jamás bajes la cumbre.")
    ]),
    ("Ley del Filtro de Hierro", "Dime con quién caminas y te diré qué tan lejos llegarás", [
        ("Elimina Parásitos", "Quien no te sume fuerza, te está robando energía."),
        ("Círculo de Titanes", "Rodéate de hombres que te obliguen a elevar tu nivel."),
        ("Lealtad Comprobada", "La amistad real se demuestra en el pozo, no en el podio.")
    ]),
    ("Ley del Sacrificio Voluntario", "El dolor que tú eliges te hace fuerte; el dolor que evitas te destruye", [
        ("Ducha Fría & Sudor", "Obliga a tu cuerpo a hacer lo que no quiere cada día."),
        ("Ayuno de Distracciones", "Aprende a decir 'no' a las fiestas que no construyen nada."),
        ("Forja del Carácter", "El hombre que busca la dificultad es imposible de quebrar.")
    ]),
    ("Ley del Largo Plazo", "La mayoría sobrestima lo que hace en un mes y subestima 5 años", [
        ("Paciencia Militar", "Construye ladrillo a ladrillo sin perder la fe."),
        ("Efecto Compuesto", "El 1% diario te hace 37 veces mejor en un año."),
        ("Visión de Águila", "No sacrifiques tu futuro por una noche de placer efímero.")
    ]),
    ("Ley de la Presencia Imponente", "Tu postura y tu mirada dicen quién eres antes de que hables", [
        ("Espalda Recta", "Camina con la frente en alto; eres dueño de tu espacio."),
        ("Mirada Directa", "No bajes los ojos ante nadie; sostén la mirada con respeto y poder."),
        ("Voz Calma y Segura", "El que grita es débil; el que habla pausado y seguro manda.")
    ]),
    ("Ley de la Propiedad Extrema", "Todo lo que pasa en tu reino es tu absoluta responsabilidad", [
        ("Cero Culpas", "Si alguien te falló, tú confiaste sin verificar. Aprende."),
        ("Control Total", "No puedes cambiar el viento, pero puedes ajustar las velas."),
        ("Liderazgo Real", "El verdadero líder se echa la culpa y comparte la gloria.")
    ]),
    ("Ley de la Gratitud de Combate", "Agradece la guerra porque es la que te sacó de la mediocridad", [
        ("Honra las Cicatrices", "Cada golpe recibido te enseñó a esquivar mejor."),
        ("El Fuego Purifica", "Sin dificultad seguirías siendo un niño consentido."),
        ("Agradece al Rival", "Tus enemigos te obligaron a ser más rápido y más fuerte.")
    ]),
    ("Ley del Enfoque Singular", "Quien persigue dos conejos a la vez regresa con las manos vacías", [
        ("Una Batalla a la Vez", "Identifica tu meta número 1 y pon toda tu pólvora en ella."),
        ("Di 'NO' a lo Bueno", "Para alcanzar lo extraordinario debes renunciar a lo aceptable."),
        ("Concentración Brutal", "4 horas de enfoque profundo valen más que 12 de distracción.")
    ]),
    ("Ley del Desapego Material", "Ten todo lo que quieras, pero que nada te tenga a ti", [
        ("Señor de tus Cosas", "Si perder un objeto te quita la paz, eres su esclavo."),
        ("Austero por Elección", "Saber vivir con poco te hace invencible ante la crisis."),
        ("Riqueza Real", "Rico no es quien más tiene, sino quien menos necesita para ser libre.")
    ]),
    ("Ley de la Acción Inmediata", "El plan perfecto ejecutado tarde no vale nada frente a la acción rápida", [
        ("Regla de los 3 Segundos", "Cuando sabes lo que debes hacer, cuenta 3 y arranca."),
        ("La Inercia es Poder", "Un tren en movimiento destruye paredes; parado no mueve una piedra."),
        ("Ajusta en Marcha", "Es más fácil corregir un auto en movimiento que empujar uno frenado.")
    ]),
    ("Ley del Cierre de Ciclos", "No puedes conquistar tierras nuevas con anclas en el puerto viejo", [
        ("Corta el Pasado", "Deja de mirar fotos viejas y conversaciones muertas."),
        ("Quema las Naves", "Si quieres conquistar la isla, no dejes barcos para huir."),
        ("Mira al Frente", "Tus mejores días no están en tus recuerdos, están en tu futuro.")
    ]),
    ("Ley de la Fortaleza en la Calumnia", "El león no pierde el sueño por la opinión de las ovejas", [
        ("La Bajeza es de Ellos", "Quien te critica por la espalda está exactamente donde pertenece."),
        ("Responde con Crecimiento", "La mejor bofetada al envidioso es verte diez veces más exitoso."),
        ("Cero Respuestas", "Discutir con un tonto te rebaja a su nivel. Sigue caminando.")
    ]),
    ("Ley del Valor Real en el Mercado", "No te pagan por tu tiempo, te pagan por el valor que aportas al tiempo", [
        ("Vuélvete Raro & Valioso", "Aprende habilidades escasas que resuelvan problemas gigantes."),
        ("No Cobres por Hora", "Cobra por la solución y el impacto que generas."),
        ("Estudio Obsesivo", "Domina tu oficio hasta que sea imposible ignorarte.")
    ]),
    ("Ley de la Energía Sagrada", "Tu atención es tu activo más costoso; protégela como a un cofre de oro", [
        ("Cero Noticias Basura", "No intoxiques tu mente con tragedias que no puedes cambiar."),
        ("Dile adiós a los Vampiros", "Gente que solo llama para quejarse debe quedar bloqueada."),
        ("Recarga en la Naturaleza", "Camina al sol, respira aire limpio y reconecta con tu fuerza.")
    ]),
    ("Ley de la Lealtad al Código", "Es mejor perder una batalla manteniendo tu honor que ganar una con traición", [
        ("Tu Nombre es tu Herencia", "El dinero se hace y se pierde; el honor manchado no se lava fácil."),
        ("Firmeza Insobornable", "Todo hombre tiene un precio hasta que conoce a un Hombre de Acero."),
        ("Duerme con Conciencia Limpia", "La almohada más suave es saber que fuiste un hombre recto.")
    ]),
    ("Ley de la Preparación para la Guerra", "Si quieres paz, entrena para la batalla más sangrienta", [
        ("Fondo de Emergencia", "Ten reservas para soportar meses de tormenta sin arrodillarte."),
        ("Cuerpo en Forma", "Mantén tu físico listo para correr, cargar o defender a los tuyos."),
        ("Mente Imperturbable", "Visualiza lo peor para que nada en el mundo te tome por sorpresa.")
    ]),
    ("Ley de la Generosidad del Fuerte", "El poder verdadero se demuestra levantando a otros, no aplastándolos", [
        ("Protege al Débil", "Usa tu fuerza para ser escudo de tu familia y de quien lo necesite."),
        ("Enseña lo que Sabes", "Un verdadero maestro crea líderes, no seguidores ciegos."),
        ("Mano Firme y Corazón Noble", "Sé un monstruo peligroso que decide ser compasivo.")
    ]),
    ("Ley del Ritmo Biológico", "Duerme como un rey, come como un atleta, trabaja como un esclavo", [
        ("El Sueño es Sagrado", "7 a 8 horas de sueño profundo para reparar hormonas y mente."),
        ("Comida de Guerrero", "Si entra basura a tu cuerpo, saldrá basura de tu mente. Come limpio."),
        ("Hidratación Constante", "El cerebro deshidratado rinde la mitad. Toma agua pura.")
    ]),
    ("Ley del Control de la Ira", "La furia ciega al guerrero; la frialdad le da puntería", [
        ("No Alces la Voz", "Cuanto más tenso el momento, más pausadas deben ser tus palabras."),
        ("Canaliza la Rabia", "Usa la bronca no para romper platos, sino para romper récords en el gym."),
        ("El Silencio Atemoriza", "El enemigo no sabe cómo reaccionar ante quien sonríe en el caos.")
    ]),
    ("Ley de la Obsesión Positiva", "El talento está sobrevalorado; la obsesión imparable gana siempre", [
        ("Hambre que no se Apaga", "No pares cuando estés cansado; para cuando hayas ganado."),
        ("Pensamiento Monotemático", "Sueña, respira y vive para tu misión principal."),
        ("El Precio de la Gloria", "Nadie que haya hecho historia fue una persona 'moderada'.")
    ]),
    ("Ley de la Victoria en el Barro", "Cuando todo se caiga a pedazos, es cuando empieza tu verdadera prueba", [
        ("Naciste para Esto", "Cualquiera sonríe cuando todo marcha bien; aquí se ven los hombres."),
        ("Mira el Desastre de Frente", "Acepta la realidad y busca el primer paso de reconstrucción."),
        ("Resurge con Fuerza", "Las cenizas son el abono para tu victoria más legendaria.")
    ]),
    ("Ley de la Inteligencia Silenciosa", "Habla menos de lo necesario y sabrás todo lo que los demás callan", [
        ("Escucha el Doble", "Dios te dio dos orejas y una boca por una razón lógica."),
        ("Deja que Hablen", "El tonto se desahoga y muestra sus cartas; el sabio toma nota."),
        ("Misterio Estratégico", "Que nadie sepa nunca tu próximo movimiento.")
    ]),
    ("Ley del Respeto a los Maestros", "Párate sobre los hombros de gigantes para ver más lejos", [
        ("Lee a los Antiguos", "Marco Aurelio, Séneca y Sun Tzu ya resolvieron tus problemas."),
        ("Busca Mentores", "Paga por el consejo de quien ya recorrió el camino que tú deseas."),
        ("Humildad de Alumno", "En el momento en que crees que lo sabes todo, empezaste a morir.")
    ]),
    ("Ley de la Inmunidad al Halago", "El veneno del halago falso mata más hombres que la espada del enemigo", [
        ("No te Creas el Cuento", "Si te aplauden, agradece y vuelve de inmediato a entrenar."),
        ("Cuidado con los Aduladores", "Quien te alaba demasiado en público te envidia en privado."),
        ("Tu Juez es el Espejo", "Solo tú sabes si diste tu máximo o si te guardaste algo.")
    ]),
    ("Ley de la Coherencia Total", "Que tus pensamientos, tus palabras y tus acciones sean una sola línea recta", [
        ("Cero Hipocresía", "No exijas lo que no das; no critiques lo que practicas."),
        ("Poder de Integridad", "Un hombre coherente tiene una fuerza espiritual inquebrantable."),
        ("Paz Mental Suprema", "No hay nada que ocultar cuando vives en absoluta verdad.")
    ]),
    ("Ley de la Resurrección Diaria", "Cada amanecer es una hoja en blanco para corregir cualquier pasado", [
        ("Ayer ya Murió", "Tus errores del pasado no tienen poder sobre el segundo presente."),
        ("Levántate y Pelea", "Mientras respires, la guerra sigue y puedes remontar el marcador."),
        ("Hoy es el Día", "No esperes a Año Nuevo; tu renacimiento empieza en este minuto.")
    ]),
    ("Ley del Cierre de Año Implacable", "Termina Diciembre con el acelerador a fondo y el nuevo año será un paseo militar", [
        ("Mientras Otros Duermen", "Aprovecha que el mundo se distrae en diciembre para tomar ventaja."),
        ("Llega con Impulso", "No arranques enero de cero; llega a enero a 200 kilómetros por hora."),
        ("El Año es Tuyo", "Mírale la cara al destino y dile: 'Esto apenas comienza'.")
    ])
]

# 31 AUDITORÍAS NOCTURNAS (21:30 PM)
AUDITORIAS_NOCHE = [
    ("¿Hoy fuiste el arquitecto de tu futuro o solo perdiste otro día en la mediocridad?", "Sé honesto contigo mismo en los comentarios. 👇"),
    ("Si tus hijos o tus padres hubieran visto todo lo que hiciste hoy, ¿estarían orgullosos de tu esfuerzo?", "No busques excusas. Responde con la verdad. 👇"),
    ("¿Avanzaste hacia tu meta más grande o te distrajiste con placeres baratos que mañana olvidarás?", "Tu conciencia sabe la respuesta. Comenta abajo. 👇"),
    ("¿Dominaste tus emociones cuando las cosas salieron mal o volviste a actuar como un niño indefenso?", "El hombre de acero responde por sus actos. 👇"),
    ("¿Cumpliste cada promesa que te hiciste al despertar o volviste a traicionar tu propia palabra?", "El respeto se gana frente al espejo. Responde aquí. 👇"),
    ("¿Dejaste que el miedo te frenara en alguna decisión hoy o diste el paso a pesar del temblor?", "Comenta con un ⚔️ si venciste al miedo hoy. 👇"),
    ("¿Fuiste el líder que tu familia necesita o una carga más llena de quejas y lamentos?", "La verdad duele, pero transforma. Escríbelo abajo. 👇"),
    ("¿Le regalaste horas valiosas a las pantallas ajenas en lugar de construir tu propio imperio?", "Confiesa tu fallo y promete corregirlo mañana. 👇"),
    ("¿Hablaste más de lo que hiciste o tus resultados hablaron con tanta fuerza que callaron al resto?", "Comenta tu mayor victoria del día. 👇"),
    ("¿Te quejaste de algo que estaba 100% bajo tu control solucionar?", "El quejoso no construye nada. ¿Venciste la queja hoy? 👇"),
    ("¿Cuidaste tu cuerpo con comida real y esfuerzo físico o lo intoxicaste con pereza y basura?", "El templo de un guerrero no acepta porquerías. Responde abajo. 👇"),
    ("¿Hiciste lo difícil y necesario primero o postergaste lo importante por comodidad cobarde?", "Sé implacable con tu autocrítica. Comenta aquí. 👇"),
    ("Si hoy fuera el último día de tu vida, ¿te irías a dormir en paz con lo que entregaste al mundo?", "La vida es corta; no la desperdicies. Responde abajo. 👇"),
    ("¿Trataste con respeto y honor a los tuyos o descargaste tu frustración con quien no la merecía?", "El verdadero poder es la serenidad con los seres queridos. 👇"),
    ("¿Leíste y aprendiste algo que te haga más sabio o tu mente se fue a dormir igual de vacía?", "El músculo mental se entrena a diario. ¿Qué aprendiste hoy? 👇"),
    ("¿Te sentiste víctima de las circunstancias en algún momento del día?", "La mentalidad de víctima es una cárcel voluntaria. Responde abajo. 👇"),
    ("¿Diste tu 100% en tu trabajo o simplemente hiciste lo mínimo para que no te despidan?", "El hombre del 1% entrega excelencia siempre. Comenta tu estándar. 👇"),
    ("¿Le dijiste 'NO' a alguna tentación que intentó apartarte de tu camino hoy?", "Cada 'no' a la mediocridad es un 'sí' a tu grandeza. 👇"),
    ("¿Guardas resentimiento contra alguien en este momento o limpiaste tu mente antes de acostarte?", "No te duermas con veneno en el pecho. Suéltalo aquí. 👇"),
    ("¿Fuiste leal a tus principios cuando nadie te estaba vigilando?", "La integridad es lo que haces en la más absoluta soledad. 👇"),
    ("¿Te conformaste con lo aceptable o buscaste la excelencia en cada detalle de tu jornada?", "La mediocridad es contagiosa; la excelencia es una elección. 👇"),
    ("¿Ayudaste a levantar a otro hombre o solo pensaste en tus propios problemas egoístas?", "El hombre fuerte tiene espaldas para sostener a los suyos. 👇"),
    ("¿Dejaste que una crítica mediocre te arruinara el día o la usaste como gasolina para acelerar?", "Comenta si tus críticos te hicieron más fuerte hoy. 👇"),
    ("¿Terminaste todo lo que te propusiste hacer hoy o dejaste tareas pendientes bajo la alfombra?", "La procrastinación es un cáncer silencioso. ¿Fuiste impecable? 👇"),
    ("¿Agradeciste por el techo, la comida y la oportunidad de seguir respirando y luchando?", "La gratitud del guerrero es su blindaje espiritual. Comenta abajo. 👇"),
    ("¿Controlaste tus gastos hoy o caíste en compras absurdas por aparentar estatus vacío?", "El rico en silencio vive en paz; el que aparenta vive quebrado. 👇"),
    ("¿Fuiste un ejemplo de disciplina para quienes te rodean hoy?", "Las palabras conmueven, pero el ejemplo arrasa. ¿Fuiste ejemplo? 👇"),
    ("¿Enfrentaste la conversación difícil que llevabas días evitando?", "La libertad está del otro lado de las conversaciones incómodas. 👇"),
    ("¿Tu entrenamiento físico de hoy fue un verdadero combate o solo fuiste a pasear al gimnasio?", "El dolor del hierro forja voluntades inquebrantables. 👇"),
    ("¿Estás más cerca de tu visión de vida hoy que cuando empezó la semana?", "Si no estás avanzando, estás retrocediendo. Sé honesto aquí. 👇"),
    ("El año está por terminar: ¿Vas a cruzar la meta como un conquistador o como un espectador cansado?", "Deja tu juramento de acero para cerrar el año con gloria. 👇")
]

def main():
    print("=" * 70)
    print("🔥 GENERADOR DE CONTENIDO DICIEMBRE 2026 — METALIDAD DE ACERO 🔥")
    print("   Estrategia: 4 Publicaciones Diarias (124 posts en total)")
    print("   Slot 1: 07:00 AM (El Despertador de Acero - Regla Inquebrantable)")
    print("   Slot 2: 12:30 PM (La Batalla de Contraste - 2 Columnas Glassmorphism)")
    print("   Slot 3: 17:30 PM (Leyes de Guerra & Estrategia - 3 Principios)")
    print("   Slot 4: 21:30 PM (Auditoría Nocturna - Juicio frente al Espejo)")
    print("=" * 70)

    start_date = datetime(2026, 12, 1)
    posts = []
    
    # Cargamos el archivo existente para continuar desde el id #53
    json_path = os.path.join(base_dir, "mentalidad_de_acero", "publicaciones.json")
    with open(json_path, "r", encoding="utf-8") as f:
        existing_posts = json.load(f)

    # Identificamos el último id
    last_id = max([p["id"] for p in existing_posts]) if existing_posts else 52
    post_id = last_id + 1

    dias_semana_es = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    for d in range(31):
        cur_date = start_date + timedelta(days=d)
        fecha_str = cur_date.strftime("%Y-%m-%d")
        dia_sem = dias_semana_es[cur_date.weekday()]
        idx_dia = d # 0 to 30

        # -------------------------------------------------------------
        # SLOT 1: 07:00 AM — EL DESPERTADOR DE ACERO
        # -------------------------------------------------------------
        frase_p, frase_s = REGLAS_MATUTINAS[idx_dia]
        bg_1 = BGS_STATUE[idx_dia % len(BGS_STATUE)]
        img_fn_1 = f"post_{post_id:03d}_{fecha_str}_despertador.jpg"
        img_fp_1 = os.path.join(img_out_dir, img_fn_1)
        
        generar_imagen_despertador(bg_1, idx_dia + 1, frase_p, frase_s, img_fp_1)

        copy_1 = f"""⚔️ REGLA INQUEBRANTABLE #{idx_dia + 1:02d}: "{frase_p.upper()}" ⚔️

¡DESPIERTA! Tu cama no es un refugio, es una trampa si te quedas en ella negociando con la pereza.

El mundo no te debe nada. A nadie le importa si tienes ganas, si hace frío o si amaneciste desanimado. El éxito no negocia con tus sentimientos; el éxito exige disciplina implacable cada mañana.

4 MANDAMIENTOS DE HOY:
🔥 1. Levántate al primer sonido; no regales ventaja a tu rival.
🔥 2. Conquista la primera hora con esfuerzo real y mente en silencio.
🔥 3. Las excusas no pagan cuentas ni forjan imperios.
🔥 4. Sé el hombre que tu familia respeta y tus enemigos temen.

Sal ahí afuera y conquista tus horas. Si estás listo para ganar el día, comenta un ⚔️.

#MentalidadDeAcero #Disciplina #SinExcusas #Enfoque #HombresDeAcero #MotivacionDiaria"""

        posts.append({
            "id": post_id,
            "fecha": fecha_str,
            "hora": "07:00",
            "dia_semana": dia_sem,
            "slot": "despertador_matutino",
            "titulo": f"Regla Inquebrantable #{idx_dia + 1:02d}: {frase_p[:35]}...",
            "texto": copy_1,
            "imagen": f"mentalidad_de_acero/imagenes/{img_fn_1}",
            "estado": "pendiente",
            "meta_post_id": None
        })
        post_id += 1

        # -------------------------------------------------------------
        # SLOT 2: 12:30 PM — LA BATALLA DE CONTRASTE
        # -------------------------------------------------------------
        batalla = BATALLAS_CONTRASTE[idx_dia]
        bg_2 = BGS_WARRIOR[idx_dia % len(BGS_WARRIOR)]
        img_fn_2 = f"post_{post_id:03d}_{fecha_str}_contraste.jpg"
        img_fp_2 = os.path.join(img_out_dir, img_fn_2)

        generar_imagen_contraste(bg_2, batalla["arquetipo"], batalla["debil"], batalla["acero"], batalla["sentencia"], img_fp_2)

        puntos_debil = "\n".join([f"  ✕ {r}" for r in batalla["debil"]])
        puntos_acero = "\n".join([f"  ✓ {r}" for r in batalla["acero"]])

        copy_2 = f"""⚔️ MENTALIDAD ERRÓNEA: {batalla['arquetipo'].upper()} vs MENTALIDAD DE ACERO ⚔️

"{batalla['sentencia'].upper()}"

¡ABRE LOS OJOS! La mediocridad no es una condena del destino, es una serie de microdecisiones cobardes que tomas todos los días. 

COMPÁRATE CON HONESTIDAD FRENTE AL ESPEJO:

❌ MENTALIDAD DÉBIL:
{puntos_debil}

🛡️ HOMBRE DE ACERO:
{puntos_acero}

El 99% de las personas viven en la queja y el conformismo. El 1% abraza el proceso, asume el 100% de responsabilidad y construye su propio destino a puño limpio.

¿De qué lado de la línea vas a pararte hoy? Guarda este post y comenta un 🛡️ si eliges el camino del acero.

#MentalidadDeAcero #ContrasteDePoder #Superacion #CrecimientoPersonal #FuerzaMental #SinVictimismo"""

        posts.append({
            "id": post_id,
            "fecha": fecha_str,
            "hora": "12:30",
            "dia_semana": dia_sem,
            "slot": "batalla_contraste",
            "titulo": f"Contraste: {batalla['arquetipo']} vs Mentalidad de Acero",
            "texto": copy_2,
            "imagen": f"mentalidad_de_acero/imagenes/{img_fn_2}",
            "estado": "pendiente",
            "meta_post_id": None
        })
        post_id += 1

        # -------------------------------------------------------------
        # SLOT 3: 17:30 PM — LEYES DE GUERRA & ESTRATEGIA
        # -------------------------------------------------------------
        ley_tit, ley_regla, ley_principios = LEYES_ESTRATEGIA[idx_dia]
        bg_3 = BGS_NATURE[idx_dia % len(BGS_NATURE)]
        img_fn_3 = f"post_{post_id:03d}_{fecha_str}_estrategia.jpg"
        img_fp_3 = os.path.join(img_out_dir, img_fn_3)

        generar_imagen_estrategia(bg_3, ley_tit, ley_regla, ley_principios, img_fp_3)

        desc_principios = "\n\n".join([f"🏛️ {i+1}. {p_t.upper()}:\n{p_d}" for i, (p_t, p_d) in enumerate(ley_principios)])

        copy_3 = f"""🏛️ {ley_tit.upper()} 🏛️
"{ley_regla.upper()}"

En un mundo lleno de charlatanes y personas que buscan atención desesperada, el verdadero poder pertenece a los que saben operar en silencio y con precisión quirúrgica.

3 PRINCIPIOS DE PODER QUE DEBES GRABARTE A FUEGO:

{desc_principios}

El hombre sabio no necesita convencer a nadie de su valor; sus obras, su presencia y sus resultados son su único testimonio.

Comparte este conocimiento con un hermano que necesite forjar su mente y comenta un 🏛️.

#EstrategiaMilitar #LeyesDePoder #MentalidadDeAcero #SabiduriaEstoica #EnfoqueLáser #PoderPersonal"""

        posts.append({
            "id": post_id,
            "fecha": fecha_str,
            "hora": "17:30",
            "dia_semana": dia_sem,
            "slot": "estrategia_poder",
            "titulo": f"Estrategia: {ley_tit} - {ley_regla[:30]}...",
            "texto": copy_3,
            "imagen": f"mentalidad_de_acero/imagenes/{img_fn_3}",
            "estado": "pendiente",
            "meta_post_id": None
        })
        post_id += 1

        # -------------------------------------------------------------
        # SLOT 4: 21:30 PM — AUDITORÍA NOCTURNA
        # -------------------------------------------------------------
        aud_preg, aud_desafio = AUDITORIAS_NOCHE[idx_dia]
        bg_4 = BGS_BEAST[idx_dia % len(BGS_BEAST)]
        img_fn_4 = f"post_{post_id:03d}_{fecha_str}_auditoria.jpg"
        img_fp_4 = os.path.join(img_out_dir, img_fn_4)

        generar_imagen_auditoria(bg_4, aud_preg, aud_desafio, img_fp_4)

        copy_4 = f"""🌙 AUDITORÍA DE CIERRE DE DÍA 🌙

"{aud_preg.upper()}"

Llegó la noche. Las luces se apagan y las excusas desaparecen. En la soledad de tu habitación solo quedan tú y el reflejo de tus acciones.

Respóndete con la verdad más cruda y sin filtros:
¿Hoy te acercaste un metro más a la cima de tus sueños, o volviste a ser cómplice de la pereza y el teléfono?

El hombre promedio se engaña para dormir tranquilo. El Hombre de Acero se audita con frialdad para levantarse mañana a destruir cualquier debilidad.

Sé honesto contigo mismo y déjame tu respuesta en los comentarios. Mañana la guerra vuelve a empezar. 👇

#AuditoriaNocturna #MentalidadDeAcero #HonestidadBrutal #EspejoDeLaVerdad #Autocontrol #Superacion"""

        posts.append({
            "id": post_id,
            "fecha": fecha_str,
            "hora": "21:30",
            "dia_semana": dia_sem,
            "slot": "auditoria_nocturna",
            "titulo": f"Auditoría: {aud_preg[:40]}...",
            "texto": copy_4,
            "imagen": f"mentalidad_de_acero/imagenes/{img_fn_4}",
            "estado": "pendiente",
            "meta_post_id": None
        })
        post_id += 1

        print(f"[{d+1:02d}/31] Generadas 4 publicaciones para {fecha_str} ({dia_sem})")

    # Guardamos todo en publicaciones.json
    all_posts = existing_posts + posts
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 70)
    print(f"✅ ¡ÉXITO TOTAL!")
    print(f"   Generadas {len(posts)} publicaciones premium para Diciembre 2026.")
    print(f"   Total en publicaciones.json: {len(all_posts)} posts.")
    print("=" * 70)

if __name__ == "__main__":
    main()
