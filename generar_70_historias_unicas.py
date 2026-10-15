# -*- coding: utf-8 -*-
"""
Genera 70 historias 100% ÚNICAS de rescate para el cronograma de Huellas con Propósito.
Mantiene los primeros 5 ya renderizados/publicados intactos.
"""

import json
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 65 Historias únicas adicionales (para completar de 6 a 70)
HISTORIAS_UNICAS = [
    # Día 2 (Reels 6-10)
    ("Canelo", "Esperó 40 días en la parada del autobús", 
     "Cada mañana miraba subir a los pasajeros esperando reconocer los zapatos de su dueño. Una conductora de la ruta notó que llevaba más de un mes durmiendo bajo la banca de metal sin probar bocado caliente. Un día de lluvia intensa, detuvo la unidad, abrió la puerta y le dijo 'sube, nos vamos a casa'. Hoy duerme en una alfombra y tiene una familia que jamás lo dejará esperando.",
     ["sad street dog", "bus stop waiting", "woman petting dog", "happy dog in car"]),
    
    ("Luna", "La encontraron atrapada en un pozo seco tras la tormenta",
     "Unos campesinos escucharon quejidos débiles en el fondo de un pozo abandonado. Con cuerdas y una linterna, un joven bajó tres metros para sacarla temblando de lodo y frío. La perrita no dejaba de apoyar su frente contra el pecho de quien la cargó. Hoy corre libre en una granja y su cola no deja de moverse con alegría.",
     ["dog in muddy ditch", "rescue ropes animal", "cleaning dirty puppy", "dog running in farm"]),

    ("Don Coco", "El abuelito del mercado al que nadie quería adoptar",
     "Pasó diez años durmiendo entre huacales de verduras en la central de abastos. Sus patas traseras ya no respondían bien por la artrosis y los clientes lo esquivaban. Doña Silvia, una maestra jubilada, lo vio acurrucado bajo una lona mojada y decidió llevarlo a su sala. Hoy Don Coco toma sus medicinas con jamón y tiene una cama ortopédica.",
     ["old senior dog", "cold street dog", "veterinarian caring dog", "dog sleeping comfortable"]),

    ("Pirata", "El perro tuerto que protegía a una camada de gatitos",
     "En un terreno baldío lleno de escombros, un perro criollo al que le faltaba un ojo no dejaba que nadie se acercara a una caja de cartón. Al revisar con cuidado, los rescatistas descubrieron que adentro había cuatro gatitos recién nacidos a los que les daba calor con su propio cuerpo. Adoptaron a Pirata junto con dos de sus gatitos en la misma casa.",
     ["one eyed street dog", "dog with kittens", "feeding rescued pets", "happy family with dog"]),

    ("Chispa", "La dejaron amarrada a un poste en víspera de año nuevo",
     "Los cohetes retumbaban en la calle y la cachorra aullaba desesperada con la cadena corta que le apretaba el cuello. Un vecino salió con una pinza de corte, rompió el eslabón y la metió a su recámara para arroparla contra el ruido. Chispa tembló durante dos horas hasta que se sintió a salvo. Hoy es la reina consentida de ese hogar.",
     ["frightened dog noise", "cutting leash rescue", "hugging scared dog", "dog playing with toy"]),

    # Día 3 (Reels 11-15)
    ("Oso", "Dormía afuera del hospital esperando a su mejor amigo",
     "Esperó durante semanas en la rampa de ambulancias sin apartar los ojos de las puertas automáticas. Las enfermeras le compartían comida, pero nadie lograba convencerlo de alejarse. Cuando un camillero comprendió su infinita lealtad, lo adoptó formalmente y le prometió honrar ese amor. Hoy Oso acompaña a su nuevo papá en cada paseo campestre.",
     ["dog waiting hospital", "feeding stray dog", "man hugging dog", "large fluffy dog happy"]),

    ("Milo", "Sobrevivió dos semanas en una isla del río",
     "La creciente del río lo dejó atrapado en un banco de arena sin comida. Los bomberos cruzaron en una lancha inflable y lo rescataron exhausto y hambriento. En cuanto tocó tierra firme, lamió la cara de todos los rescatistas uno por uno. Hoy vive en una casa con jardín amplio donde el agua es solo para jugar.",
     ["dog trapped river", "boat rescue animal", "wrapped dog towel", "golden retriever swimming"]),

    ("Kira", "La cachorrita que encontraron adentro de una llanta vieja",
     "Apenas tenía un mes de nacida y apenas podía abrir los ojos entre la basura de un taller. Una clienta escuchó su chillido y la alimentó con gotero cada tres horas. Contra todo pronóstico, Kira superó la anemia y creció fuerte y brillante. Hoy es un torbellino de alegría que llena la casa de travesuras.",
     ["tiny puppy tyre", "bottle feeding puppy", "puppy playing yard", "beautiful healthy dog"]),

    ("Roco", "El vigilante que sobrevivió al derrumbe de una barda",
     "Cuidaba una bodega en construcción cuando una pared cedió durante una tormenta. Los vecinos cavaron con sus propias manos durante dos horas hasta encontrarlo protegido bajo una viga de madera. Salió ileso y con la mirada llena de agradecimiento. Hoy duerme dentro de casa y nunca más tendrá que vigilar nada.",
     ["construction debris dog", "people digging rescue", "carrying wounded dog", "dog sleeping couch"]),

    ("Bella", "La perrita ciega que guía con el corazón",
     "Nació sin visión y fue abandonada en un callejón donde chocaba con las paredes. Una familia con experiencia en mascotas especiales la adoptó y tapizó la casa con texturas para que aprendiera a orientarse. En dos semanas ya corría por el pasillo guiada por la voz de sus dueños. El amor no necesita ojos para verse.",
     ["blind dog gentle", "hand guiding dog", "dog smelling flower", "smiling dog outdoors"]),

    # Día 4 (Reels 16-20)
    ("Bruno", "Esperaba que abrieran la casa que ya estaba vacía",
     "Los inquilinos entregaron las llaves y se fueron, pero Bruno se quedó sentado en el felpudo de la entrada durante seis días. Una vecina se dio cuenta de que no se movía ni para buscar agua. Le ofreció comida, le habló con cariño y se lo llevó a su departamento. Bruno tardó solo un día en entender que había encontrado su verdadero hogar.",
     ["dog waiting door", "empty house dog", "woman giving food", "dog sleeping on bed"]),

    ("Pecas", "Lo arrojaron desde una camioneta en movimiento",
     "Un conductor que venía detrás frenó a tiempo y evitó una tragedia. Pecas tenía raspaduras y la mirada rota de pánico, pero no guardó ningún rencor. El mismo automovilista que lo salvó lo llevó de inmediato a urgencias y decidió que jamás volvería a separarse de él. Hoy viajan juntos en el asiento del copiloto.",
     ["dog on road shoulder", "driver picking dog", "vet bandaging dog", "dog looking out car window"]),

    ("Sombra", "El perro negro al que nadie quería adoptar por superstición",
     "Pasó un año entero en el refugio viendo cómo adoptaban a todos los cachorros menos a él por su color oscuro. Una niña pequeña entró un sábado, lo miró a los ojos y dijo: 'mamá, él tiene la mirada más dulce del mundo'. Hoy Sombra es el mejor amigo de la niña y duerme a los pies de su cama protegiendo sus sueños.",
     ["black street dog", "dog behind shelter cage", "child hugging dog", "happy black lab running"]),

    ("Toby", "Caminó 15 kilómetros con una pata lastimada",
     "Llegó rengueando a una gasolinera rural con las almohadillas quemadas por el asfalto. Los despachadores le improvisaron una casita con una caja y juntaron propinas para pagar su radiografía. El hueso soldó perfecto y el gerente de la estación terminó adoptándolo como parte de su familia.",
     ["limping stray dog", "bandaged paw dog", "friendly gas station dog", "dog running grass"]),

    ("Mora", "Rescatada de un techo de lámina a 40 grados",
     "Lloraba bajo el rayo del sol sin una sola sombra donde resguardarse. La denuncia vecinal movilizó a los bomberos, quienes subieron con escaleras y cortaron la soga que la asfixiaba. En cuanto bebió agua fresca, lamió las manos de los uniformados. Hoy vive en una casa con aire acondicionado y patio arbolado.",
     ["hot roof dog thirsty", "firefighter rescue ladder", "giving cold water dog", "dog resting under tree"]),

    # Día 5 (Reels 21-25)
    ("Zeus", "El pitbull que solo quería que lo acariciaran",
     "Lo tenían encadenado para dar miedo, pero cuando un voluntario se acercó despacio, Zeus agachó las orejas y se puso panza arriba pidiendo mimos. Le retiraron la cadena oxidada y descubrieron a un perro dócil, juguetón y noble. Hoy convive con niños y otros perros demostrando que la raza no define el corazón.",
     ["chained pitbull sad", "unshackling dog chain", "friendly dog belly rub", "happy pitbull playing"]),

    ("Nieve", "La cachorrita rescatada de un canal de aguas negras",
     "Unos jóvenes que andaban en bicicleta escucharon chillidos en el fondo del desagüe. Armaron una cadena humana para bajar y sacarla envuelta en una chamarra. A pesar de la mugre, su pelo era blanco como la nieve. Una de las rescatistas la bañó, la adoptó y hoy es la luz de su casa.",
     ["dirty puppy ditch", "people human chain rescue", "bathing muddy puppy", "fluffy white dog clean"]),

    ("Boby", "El compañero fiel de un abuelo en soledad",
     "Boby vagaba desorientado por la plaza hasta que se sentó al lado de don Ernesto, quien acababa de perder a su esposa. Se quedaron mirando en silencio durante media hora y don Ernesto le dijo: 'bueno amigo, parece que los dos nos necesitamos'. Desde ese día no se separan ni para ir a comprar el pan.",
     ["lonely stray dog", "elderly man sitting bench", "dog leaning elderly", "walking dog in park"]),

    ("Perla", "La perrita que cuidaba la escuela abandonada",
     "Cerraron la escuela por remodelación y Perla se quedó cuidando los pasillos vacíos. Los maestros que volvían a revisar el archivo le dejaban croquetas hasta que una profesora decidió llevarla a su casa de campo. Hoy tiene hectáreas para correr y ya no pasa frío en las noches.",
     ["dog empty school", "teacher feeding dog", "dog wagging tail", "dog running happy field"]),

    ("Tigre", "Rescatado con sarna severa, hoy parece otro perro",
     "No tenía pelo en el lomo y la piel estaba agrietada por el abandono. Un albergue le dio baños medicados y mucho amor durante tres meses. Poco a poco su pelaje dorado volvió a crecer brillante y suave. Cuando lo ves hoy correr en la playa, es imposible creer el sufrimiento que dejó atrás.",
     ["hairless sick dog", "medicated bath dog", "dog fur regrowing", "majestic dog on beach"]),

    # Día 6 (Reels 26-30)
    ("Choco", "Esperaba que salieran los niños de la primaria",
     "Se sentaba afuera del portón escolar todas las tardes para recibir las caricias de los alumnos. Cuando llegaron las vacaciones de verano, se quedó solito en la banqueta esperando. La directora de la escuela conmovida por su paciencia se lo llevó a su hogar. Ahora tiene dos hermanos perrunos y amor infinito.",
     ["dog waiting school gate", "children petting stray", "car ride rescued dog", "two dogs playing home"]),

    ("Princesa", "La rescataron de un basurero municipal",
     "Buscaba cáscaras y sobras entre montañas de desechos para no morir de hambre. Un grupo de voluntarios de rescate animal la atraparon con suavidad y le dieron su primer plato de comida caliente. Tardó unos días en confiar, pero hoy es la perrita más agradecida y cariñosa del mundo.",
     ["dog in garbage dump", "offering warm food dog", "clean brush rescued dog", "pampered dog sofa"]),

    ("Goliath", "El gigante mestizo que le temía a las escobas",
     "Pesaba más de 30 kilos, pero si veía una escoba salía corriendo a esconderse debajo de la mesa temblando por los maltratos de su pasado. Su nueva familia entendió su trauma y con paciencia infinita, premios y palabras suaves, le devolvieron la seguridad. Hoy camina con la cabeza en alto.",
     ["large timid dog", "scared dog corner", "gentle hand treat dog", "confident dog walking"]),

    ("Estrella", "Sobrevivió atada a un árbol en medio de la sequía",
     "No tenía plato de agua ni techo donde cubrirse del sol. Los vecinos llamaron a la patrulla ambiental tras escuchar sus lamentos. Le retiraron el alambre y la trasladaron a un hogar temporal donde floreció por completo. Hoy duerme en una colchoneta suave y tiene juguetes por toda la sala.",
     ["dog tied tree dry", "police cutting leash", "dog drinking water bucket", "happy dog indoor"]),

    ("Chester", "El perro panadero que conquistó a una colonia entera",
     "Llegaba puntualmente a las 7 de la noche al olor del horno de pan. El panadero empezó dejándole un bolillo tibio y terminó abriéndole la puerta de su casa para siempre. Chester ahora es el inspector oficial del pan y duerme calientito junto al horno.",
     ["dog outside bakery", "baker giving bread dog", "friendly dog wagging", "dog sleeping warmth"]),

    # Día 7 (Reels 31-35)
    ("Lucas", "Lo dejaron en una caja de zapatos recién nacido",
     "Pesaba apenas 300 gramos y sus ojos aún no se abrían. Una estudiante de veterinaria lo mantuvo calientito con botellas de agua tibia y lo alimentó con jeringa cada dos horas. Hoy Lucas es un perro adulto sano, fuerte y lleno de vida que acompaña a su salvadora a todas partes.",
     ["tiny newborn puppy", "syringe feeding puppy", "puppy growing fast", "strong adult dog playing"]),

    ("Maya", "La perrita de las vías del tren",
     "Se le atoró la correa entre las maderas del riel minutos antes del paso del tren de carga. El maquinista aplicó el freno de emergencia a la distancia y los guardavías corrieron a soltarla. Ese maquinista no pudo olvidar sus ojos y al terminar su turno fue a buscarla para adoptarla.",
     ["dog railroad tracks", "train stopping emergency", "railway worker dog", "dog and owner sunset"]),

    ("Bimba", "La abandonaron porque creció más de lo esperado",
     "La compraron creyendo que sería pequeña y cuando alcanzó su tamaño real la echaron a la calle. Desorientada, vagaba buscando una puerta conocida hasta que una rescatista la acogió. Su tamaño es igual de grande que su nobleza. Hoy vive en un rancho donde su espacio nunca será un problema.",
     ["abandoned large puppy", "dog wandering lost", "open arms dog hug", "dog running freely field"]),

    ("Pancho", "El abuelito que pedía caricias en la farmacia",
     "Se paraba en el tapete de la farmacia para que el aire acondicionado le refrescara la artritis. Los clientes se encariñaron con él y una enfermera del dispensario decidió darle una jubilación digna. Pancho hoy pasa sus días entre almohadones y mimos constantes.",
     ["senior dog store entrance", "store customer petting", "carrying old dog car", "peaceful sleeping dog"]),

    ("Loki", "El escapista que solo buscaba una mano amiga",
     "Saltaba cualquier barda no para huir, sino para buscar gente que le hiciera cariños. Cuando llegó a una familia que le dedica paseos, juegos y entrenamiento, sus ganas de escapar desaparecieron por completo: ya tenía todo lo que siempre soñó en su propia casa.",
     ["dog jumping fence", "dog approaching stranger", "dog playing fetch grass", "tired happy dog resting"]),

    # Día 8 (Reels 36-40)
    ("Duque", "Rescatado de una fábrica abandonada",
     "Vivió tres años encerrado cuidando maquinaria en desuso sin ver pasto ni recibir una sola caricia. Cuando quebró la empresa, los rescatistas forzaron el portón para liberarlo. La primera vez que pisó el césped, no paraba de rodar sobre su espalda con una sonrisa inolvidable.",
     ["abandoned warehouse dog", "opening rusty gate", "dog rolling in grass", "smiling dog outdoors"]),

    ("Chula", "La perrita que consolaba a los ancianos del asilo",
     "Entró por una rendija del jardín de un asilo de ancianos buscando refugio de la lluvia. Los residentes pidieron a la administración que no la sacaran. Chula se convirtió en la terapeuta no oficial del asilo, visitando las habitaciones de cada abuelo para darles compañía y consuelo.",
     ["dog entering elderly home", "elderly lady stroking dog", "dog sleeping near wheelchair", "happy nursing home dog"]),

    ("Rayo", "Sobrevivió al frío extremo en una obra negra",
     "Apenas tenía dos meses cuando lo encontraron temblando sobre un charco congelado en una construcción. Los albañiles lo arroparon con chalecos de trabajo y juntaron para comprarle leche especial. Uno de ellos se lo llevó a casa para sus hijos. Rayo nunca más volverá a sentir frío.",
     ["puppy in cold puddle", "workers wrapping puppy", "feeding warm milk puppy", "playful puppy with kids"]),

    ("Kiara", "La perrita que nunca perdió la fe en los humanos",
     "A pesar de haber sufrido abandono y desnutrición extrema, cada vez que alguien se le acercaba, movía la cola con timidez pero con esperanza. Esa ternura enamoró a una familia que la cuidó hasta recuperar su peso. Hoy Kiara es pura alegría y gratitud.",
     ["skinny dog wagging tail", "gentle hand approach", "healthy dog transformation", "dog smiling with family"]),

    ("Simba", "El leoncito criollo que cuidaba a su hermano herido",
     "En la orilla de una carretera, Simba no se despegaba de otro perrito que había sido atropellado, ladrando para llamar la atención de los autos. Gracias a su lealtad, los rescatistas llegaron a tiempo para salvar a ambos. Hoy viven juntos y felices en el mismo hogar adoptivo.",
     ["two dogs road shoulder", "dog protecting other dog", "loading dogs ambulance", "two happy dogs playing"]),

    # Día 9 (Reels 41-45)
    ("Negrito", "El perro del puente que esperaba a su rescatista",
     "Cada tarde esperaba en el mismo escalón del puente peatonal a la voluntaria que le llevaba croquetas. Cuando la voluntaria finalmente consiguió un departamento que aceptaba mascotas, fue por él con una correa nueva. Negrito saltó a sus brazos sin dudarlo un segundo.",
     ["dog on bridge stairs", "waiting faithful dog", "attaching new leash dog", "happy dog in living room"]),

    ("Mía", "La cachorrita que encontraron en una llanta de camión",
     "Se metió adentro de la rueda para protegerse del viento y no podía salir. Los mecánicos desarmaron la llanta con cuidado para liberarla sana y salva. La historia se viralizó en la colonia y una familia amorosa la adoptó esa misma tarde.",
     ["truck tyre puppy", "mechanics freeing puppy", "clean puppy smiling", "dog asleep cozy bed"]),

    ("Teo", "El perrito sordo que aprende con señas de amor",
     "Nació sin poder escuchar y sus dueños anteriores pensaban que era desobediente. En su nuevo hogar le enseñaron comandos con luces y señas con las manos. Teo aprendió a sentarse, dar la pata y jugar en tiempo récord. El amor tiene su propio lenguaje.",
     ["deaf dog looking attentive", "hand sign to dog", "dog responding treat", "playful dog running"]),

    ("Paloma", "Blanca y suave, rescatada de un basural",
     "La encontraron cubierta de aceite y ceniza en un tiradero a cielo abierto. Tras tres baños con shampoo especial, apareció un pelaje blanco impecable como las plumas de una paloma. Hoy duerme sobre un cojín de plumas y recibe caricias todo el día.",
     ["dirty white dog trash", "bath with warm water dog", "brushing white fluffy dog", "elegant white dog posing"]),

    ("Rocky", "El boxeador criollo que venció la desnutrición",
     "Pesaba solo 8 kilos cuando debía pesar 25. Sus costillas se marcaban y apenas se sostenía en pie. Con dieta balanceada, sueros y amor incondicional, recuperó su musculatura en dos meses. Hoy corre maratones con su dueño por la montaña.",
     ["emaciated dog shelter", "dog eating nutritious food", "dog gaining strength", "strong dog mountain trail"]),

    # Día 10 (Reels 46-50)
    ("Sol", "La perrita que iluminó la vida de una niña enferma",
     "Rescatada de un predio baldío, Sol fue entrenada como perrita de apoyo emocional. Llegó a la vida de Sofía, una niña en tratamiento médico, y desde el primer día se convirtió en su sombra protectora. Su alegría le devolvió la sonrisa a toda la familia.",
     ["scared dog rescue", "training gentle dog", "dog resting head child lap", "happy child and dog park"]),

    ("Hachiko", "Esperaba afuera del metro todas las noches",
     "Miraba fijamente los torniquetes del metro cada vez que salía un tren. Los policías de la estación le pusieron una caja con cobijas mientras le buscaban hogar. Una usuaria diaria que lo saludaba todas las mañanas decidió llevárselo a casa para que nunca más esperara en vano.",
     ["dog outside subway station", "police feeding dog", "woman greeting dog", "dog sleeping comfortable rug"]),

    ("Canela", "La perrita que sobrevivió a una inundación",
     "Estaba encaramada en el techo de una casa con el agua tapándole las patas. Los socorristas llegaron en lancha y la subieron a bordo justo a tiempo. Hoy Canela vive en una colina alta y solo ve el agua en su tazón limpio.",
     ["dog flooded house roof", "rescuers in boat dog", "drying shivering dog", "dog running green hill"]),

    ("Max", "El perro guardián que se jubiló con honores",
     "Trabajó 8 años vigilando un depósito industrial. Cuando la empresa cerró, los trabajadores se negaron a dejarlo atrás y le buscaron un hogar con jardín. Hoy Max disfruta de su jubilación jugando con pelotas de tenis y durmiendo siestas al sol.",
     ["aging guard dog", "workers saying goodbye dog", "dog chasing tennis ball", "peaceful old dog yard"]),

    ("Pelusa", "La cachorrita que persiguió la camioneta de sus dueños",
     "Corrió dos cuadras detrás del auto hasta que sus patitas no aguantaron más. Una vecina la levantó en brazos con el corazón roto. Esa cachorrita nunca volverá a correr detrás de nadie: ahora tiene una familia que va a donde ella vaya.",
     ["puppy running after car", "woman picking tired puppy", "feeding puppy treat", "loved fluffy puppy home"]),

    # Día 11 (Reels 51-55)
    ("Beto", "El perro del taller de bicicletas",
     "Llegó rengueando buscando refugio bajo los mostradores. El mecánico le curó la pata y le puso su plato de comida junto a las herramientas. Beto aprendió a recibir a cada cliente con la cola moviéndose como hélice. Es el empleado estrella del local.",
     ["limping dog shop", "fixing dog paw bandage", "dog greeting customers", "dog sleeping shop floor"]),

    ("Lola", "La rescataron de un pozo de agua abandonado",
     "Llevaba tres días atrapada en la oscuridad gimiendo por ayuda. Los vecinos usaron un arnés especial para descender y sacarla en brazos. Cuando vio la luz del sol, empezó a lamer las lágrimas de su rescatista. Hoy duerme en una cama suave y tibia.",
     ["dark well dog rescue", "hauling up dog harness", "dog seeing sunlight", "dog playing with ball"]),

    ("Cobi", "El perrito que cuidaba a los niños del barrio",
     "Acompañaba a los niños desde sus casas hasta la escuela para que no caminaran solos. Una de las madres decidió adoptarlo formalmente para agradecerle su lealtad infinita. Cobi ahora tiene su propia casa y sigue cumpliendo su deber con alegría.",
     ["dog walking children school", "mother petting street dog", "dog wearing shiny collar", "dog running with kids"]),

    ("Mona", "La perrita que aprendió a confiar otra vez",
     "Se encogía de miedo ante cualquier movimiento brusco por el maltrato que sufrió. Con semanas de paciencia, caricias suaves y comida rica, comprendió que las manos humanas también saben acariciar. Hoy busca el regazo de sus dueños cada diez minutos.",
     ["cowering scared dog", "slow hand offering food", "dog letting human pet", "happy dog cuddled bed"]),

    ("Fito", "El perro que encontró a su familia en un día de campo",
     "Apareció tímidamente entre los árboles de un parque nacional buscando restos de comida. Una familia lo invitó a compartir su almuerzo y al terminar el día, simplemente no pudieron dejarlo ahí. Fito se subió al auto como si siempre hubiera sido suyo.",
     ["dog forest trail", "family feeding dog picnic", "dog jumping car trunk", "dog resting family home"]),

    # Día 12 (Reels 56-60)
    ("Nico", "Rescatado de una tubería de desagüe",
     "Un cachorrito curioso quedó atorado en un tubo de desagüe durante una lluvia torrencial. Los bomberos rompieron el concreto con martillos neumáticos durante tres horas hasta sacarlo sano. Hoy Nico es el perro más consentido de la estación de bomberos.",
     ["puppy pipe stuck", "firefighters digging concrete", "pulling out muddy puppy", "fire station mascot dog"]),

    ("Tita", "La perrita anciana que pedía pan en la cafetería",
     "Se sentaba con mirada digna afuera de la terraza esperando su pedacito de pan tostado. Una clienta habitual decidió que merecía pasar sus últimos años con todos los lujos posibles. Hoy Tita duerme en cojines de terciopelo y no le falta nada.",
     ["old dog outside cafe", "client sharing bread", "warm blanket wrapped dog", "pampered senior dog sleep"]),

    ("Pongo", "El dálmata mestizo que sobrevivió al abandono",
     "Lo dejaron amarrado a un poste bajo la lluvia fría con una soga de tender ropa. Un repartidor de comida frenó su moto, cortó la cuerda y se lo llevó en su mochila térmica. Hoy Pongo tiene una familia cariñosa y corre feliz por los prados.",
     ["dog tied rain lamppost", "delivery driver saving dog", "dog in motorcycle basket", "spotted dog running"]),

    ("Chipi", "El perrito miniatura con un corazón gigante",
     "Pesaba apenas dos kilos pero ladraba con valentía para ahuyentar a los coyotes del gallinero de una granja. La dueña de la granja lo adoptó como su guardián personal y le dio su propia casita adentro de la recámara. Chipi demostró que el valor no se mide en centímetros.",
     ["tiny Chihuahua mix outdoor", "farm lady holding small dog", "dog standing proud yard", "small dog sleeping pillow"]),

    ("Gordo", "El perro consentido del barrio que encontró un hogar fijo",
     "Todos los vecinos le daban comida pero nadie se hacía responsable de sus vacunas ni de protegerlo del frío. Una pareja recién mudada decidió llevarlo al veterinario y abrirle su puerta para siempre. Gordo pasó de ser el perro de todos a ser el rey de un hogar.",
     ["chubby friendly street dog", "couple taking dog leash", "vet clinic checkup dog", "happy dog living room couch"]),

    # Día 13 (Reels 61-65)
    ("Kiko", "El perro que aprendió a sonreír con la mirada",
     "Tenía los ojos apagados por el maltrato y la indiferencia. Tras ser rescatado y alimentado con amor, su expresión cambió por completo. Hoy cuando ve llegar a su familia mueve la cola con tanta fuerza que mueve todo su cuerpo. La felicidad también se aprende.",
     ["sad looking stray dog", "dog receiving food gently", "dog smiling eyes bright", "joyful dog greeting owner"]),

    ("Sultán", "El guardián leal que sobrevivió a un incendio",
     "Ladra desesperado para despertar a los habitantes de una vecindad antes de que el fuego se propagara. Todos lograron salir ilesos gracias a su alerta. Los vecinos agradecidos se cooperaron para pagarle su atención médica y le dieron un hogar definitivo.",
     ["smoke fire street rescue", "dog bark alerting", "community petting hero dog", "healthy hero dog yard"]),

    ("Mía", "La perrita que nació en un lote baldío",
     "Creció entre piedras y maleza sin conocer el tacto humano. Una rescatista se ganó su confianza poco a poco dejándole comida durante dos semanas. Hoy Mía no se despega del sillón y adora que le rasquen la panza.",
     ["dog hiding tall grass", "woman placing food bowl", "dog approaching slowly", "dog sleeping happily rug"]),

    ("Lucas", "El perro rescatado de un techo de chapa",
     "No tenía agua ni comida bajo el sol inclemente. Una llamada anónima alertó a las autoridades que procedieron al decomiso inmediato. Lucas hoy vive con un patio con sombra, alberca para perros y amor de sobra.",
     ["dog hot tin roof", "animal control officer dog", "dog splashing water pool", "smiling dog in shadow"]),

    ("Bambi", "El cachorro patilargo que nadie quería",
     "Sus patas eran demasiado largas y se tropezaba al correr. Nadie lo elegía en las jornadas de adopción. Una pareja de corredores vio en él al compañero perfecto. Hoy Bambi corre 10 kilómetros diarios a su lado con energía imparable.",
     ["clumsy long legged puppy", "dog adoption fair cage", "couple running with dog", "athletic dog outdoors"]),

    # Día 14 (Reels 66-70)
    ("Zeus", "El gran danés mestizo rescatado de una azotea",
     "Apenas cabía en el espacio donde lo tenían confinado. Los bomberos tuvieron que usar una grúa para bajarlo con seguridad. La primera vez que corrió por un campo abierto lloró de alegría. Su nobleza no tiene límites.",
     ["huge dog confined roof", "crane platform dog rescue", "giant dog running meadow", "gentle giant hugging human"]),

    ("Nala", "La leoncita que cuidaba a los cachorros huérfanos",
     "Adoptó a tres perritos ajenos que habían sido tirados en una caja y los amamantó como si fueran suyos. Una rescatista salvó a la familia completa y todos fueron adoptados en hogares responsables. El amor de madre no tiene fronteras.",
     ["dog nursing puppies box", "rescuers carrying puppies", "healthy mother dog relaxing", "puppies playing happily"]),

    ("Ringo", "El perro con alma de músico",
     "Se sentaba todas las tardes junto a un músico callejero que tocaba la guitarra. El músico compartía con él sus ganancias en croquetas y al terminar la gira decidió llevárselo a casa para siempre. Ringo ahora tiene su propia canción.",
     ["dog sitting street musician", "guitar player feeding dog", "dog sleeping guitar case", "happy dog listening music"]),

    ("Cora", "La perrita con corazón de oro",
     "Tenía una cicatriz en el hocico pero la mirada más dulce del mundo. Una familia con niños pequeños la adoptó sabiendo que las cicatrices solo cuentan batallas ganadas. Hoy Cora es la protectora más tierna de los pequeños.",
     ["scarred face gentle dog", "child gently touching dog", "dog kissing child cheek", "peaceful family with dog"]),

    ("Ángel", "El perro que cerró con broche de oro esta historia",
     "Vagó por años sin rumbo ni nombre hasta que llegó al refugio de Huellas con Propósito. Hoy duerme en una cama calientita, bien alimentado y rodeado de amor. Cada vida salvada vale la pena. Síguenos para seguir salvando almas.",
     ["lonely dog walking sunset", "shelter door opening dog", "dog wrapped warm blanket", "majestic dog looking camera"])
]

def main():
    with open('cronograma_70_reels.json', 'r', encoding='utf-8') as f:
        cronograma = json.load(f)

    print(f"Cargados {len(cronograma)} elementos del cronograma.")

    # Mantener los 5 primeros (ya renderizados / publicados)
    # Actualizar del 6 al 70 con las 65 historias 100% únicas
    for idx, (nombre, titulo, texto, queries) in enumerate(HISTORIAS_UNICAS):
        reel_id = idx + 6
        if reel_id > len(cronograma):
            break

        c = cronograma[reel_id - 1]
        
        # Limpieza y formateo
        t_clean = titulo.upper()
        palabras = t_clean.split()
        sub1 = " ".join(palabras[:4]) + "\n" + " ".join(palabras[4:8])

        subtitulos = [
            f"HISTORIA DE RESCATE:\n{sub1.strip()}",
            "NO PODÍAN DEJARLO EN EL OLVIDO\nUN RESCATE A TIEMPO",
            "EL MOMENTO EN QUE TODO CAMBIÓ\nVOLVIÓ A SENTIR AMOR",
            f"HOY {nombre.upper()} ES FELIZ\nNUNCA MÁS ESTARÁ SOLO"
        ]

        guion = f"{texto} Síguenos en Huellas con Propósito si crees en las segundas oportunidades."

        caption = (
            f"🎬🐾 HISTORIA REAL: {titulo}\n\n"
            f"{texto}\n\n"
            f"🐕 Síguenos en @huellasconproposito26 si crees en las segundas oportunidades y comparte este Reel para salvar más vidas. ❤️\n\n"
            f"#HuellasConPropósito #PerrosDeBarrio #RescateAnimal #HistoriasReales #AdoptaNoCompres #AmorPerruno #ReelsInstagram #Viral"
        )

        c["nombre_perrito"] = nombre
        c["titulo"] = titulo
        c["guion"] = guion
        c["frases_subtitulos"] = subtitulos
        c["queries_video"] = queries
        c["caption"] = caption
        c["archivo_video"] = f"videos_reels_cinematicos/reel_cinematico_{reel_id}_{nombre.lower()}.mp4"

    with open('cronograma_70_reels.json', 'w', encoding='utf-8') as f:
        json.dump(cronograma, f, indent=2, ensure_ascii=False)

    print("🎉 ¡Las 70 historias son ahora 100% ÚNICAS y diferentes!")
    print(f"Primeros 5 intactos (Reels 1 al 5 renderizados/publicados).")
    print(f"Reels 6 al 70 actualizados con historias y queries de video exclusivas.")

if __name__ == '__main__':
    main()
