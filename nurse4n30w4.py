from ortools.sat.python import cp_model 
import pandas as pd
import numpy as np

# Seleccion de archivos para ser usados
#Scenario = input("Nombre del archivo de escenario: ")
historia = input("Número del archivo de historia: ")
semana = input("Número del archivo de semana: ")

"""Lectura de los Datos de Entrada """

# leer el fichero de datos generales del escenarios seleccionado
contador_nombres=0 # para tener control del indice de cada nombre
dic_nomb_enferm={} # diccionario para guardar los nombres de las enfermeras
contador_turnos=0 # para tener control del indice de cada nombre
dic_turnos={} # diccionario para guardar los nombres de las turnos

# vamos a leer el archivo del ESCENARIO linea por linea
with open("./n030w4/Sc-n030w4.txt") as archivo:
    for linea in archivo:
      # leer el escenario y el numero de enfermeras verificando palabras claves en el fichero
      if "SCENARIO =" in linea: escenario = linea [linea.find('=')+1:-1]
      if "NURSES =" in linea: 
        num_nurses=int(linea[linea.find('=')+1:linea.find('n')]) #se busca el texto que esta entre esos signos
        contador_nombres+=1 # contador para extraer los nombres que van debajo de la palabra NURSES
      # para filtrar los nombres de las enfermeras
      if contador_nombres>=1 and (linea.split())[0]!='NURSES': 
        nombre_enfermera=(linea.split())[0] # extraer el nombre que esta ubicado en la posicion inicial de esa lista
        dic_nomb_enferm[contador_nombres]=nombre_enfermera # se guarda el diccionario con cada nombre y su indice
        contador_nombres+=1
      if "SHIFT_TYPES =" in linea: # para identificar la palabra clave en la linea
        num_shifts=int(linea[linea.find('=')+1:linea.find('n')]) # se extrae la cantidad de turnos directamente 
        contador_turnos+=1 # se incrementa el contador de turnos
      # para filtrar los tipos de turnos y extraer los minimos y maximos numeros de asignaciones consecutivas permitidas
      if contador_turnos>=1 and contador_turnos<=num_shifts : # entra aqui cuando el contador de lineas de turnos dea menor o igual al num turnos       
        if len (linea.split())==2: # filtro que garantiza que la lista extraida de la linea tenga solo dos elementos
          tipo_turno=(linea.split())[0] # extraer el tipo de turno como el primer elemento de la lista
          min_max_turnos=(linea.split())[1]
          dic_turnos[contador_turnos]=[tipo_turno,min_max_turnos] # se guarda el diccionario con el identificador del turno y su indice
          contador_turnos+=1 # se incrementa el contador en cada linea que sigue
      # para extraer la cantidad de dias
      if "WEEKS =" in linea: num_days=7*int(linea[linea.find('=')+1:linea.find('n')]) 
  
      
      
# imprimir los datos principales
print('***  DATOS GENERALES DEL PROBLEMA ***')
print(' ')
print('El Escenario es:', escenario)
print('El numero de Enfermeras es:', num_nurses)
print('El numero de Turnos es:', num_shifts)
print('El numero de dias es:', num_days)
print('Los nombres de las enfermeras son:',dic_nomb_enferm)
print('Los tipos de turnos y sus rangos maximos y minimos son:',dic_turnos)

# Ahora procedemos a leer el fichero de datos Historico de cada enfermera
contador_historico=0 # para tener control del indice de cada historico de cada enfermera
# vamos a leer el archivo del record Historio linea por linea
with open("./n030w4/H0-n030w4-" + historia + ".txt") as archivo:
    for linea in archivo:
      if 'NURSE_HISTORY' in linea:
        contador_historico+=1
      # vamos a extraer el numero de dias consecutivos trabajados en la semana previa
      # vamos a extraer el numero de dias consecutivos No trabajados.   
      if contador_historico>=1 and (linea.split())[0]!='NURSE_HISTORY':
        num_dias_trabajados= (linea.split())[-2]
        num_dias_NO_trabajados= (linea.split())[-1]
        dic_nomb_enferm[contador_historico]=[dic_nomb_enferm[contador_historico],num_dias_trabajados,num_dias_NO_trabajados]
        contador_historico+=1

for enf in dic_nomb_enferm.values():
  print('La cantidad de dias consecutivos trabajados previos de ',enf[0],' fueron:', enf[1])
  print('La cantidad de dias consecutivos NO trabajados previos de ',enf[0],' fueron:', enf[2])

# Extraer los tipos de contrato y los maximos y minimos permisibles
contador_nombres=0
contador_contrato=0
dic_contrato={}
dic_tipo_contrato={}
# vamos a leer el archivo del ESCENARIO linea por linea
with open("./n030w4/Sc-n030w4.txt") as archivo:
    for linea in archivo:
      # leer el escenario y el numero de enfermeras verificando palabras claves en el fichero      
      if "NURSES =" in linea: 
        num_nurses=int(linea[linea.find('=')+1:linea.find('n')]) #se busca el texto que esta entre esos signos
        contador_nombres+=1 # contador para extraer los nombres que van debajo de la palabra NURSES
      # para filtrar los nombres de las enfermeras
      if contador_nombres>=1 and (linea.split())[0]!='NURSES': 
        contrato=(linea.split())[1] # extraer el tipo de contrato que esta n la posicion 2
        dic_tipo_contrato[contador_nombres]=contrato
        contador_nombres+=1
      if "CONTRACTS =" in linea:
        contador_contrato+=1
      try:
        if contador_contrato>=1 and (linea.split())[0]!='CONTRACTS':
          limites_contrato=(linea.split())[2]
          maximo_limite_NO=limites_contrato[3]        
          dic_contrato[(linea.split())[0]]=[maximo_limite_NO] 
          contador_contrato+=1
      except:
        pass
print('Los valores maximos permitidos para dias consecutivos no trabajados son:',dic_contrato)
print('Los tipos de contrato segun cada enfermera son:',dic_tipo_contrato)

contador_req=0
# vamos a leer el archivo de los requerimientos semanales linea por linea
with open("./n030w4/WD-n030w4-" + semana + ".txt") as archivo:
    for linea in archivo:
      if 'REQUIREMENTS' in linea:
        contador_req+=1
      if contador_req>=1 and contador_req<=6:
        if (linea.split())[0]!='REQUIREMENTS':            
          contador_req+=1

"""Preprocesamiento de los datos antes de ser ingresados al modelo"""

# creamos los range que son listas inmutable de n números enteros consecutivos que empieza en 0 y acaba en el valor del
# argumento - 1.
all_nurses = range(num_nurses)
all_shifts = range(num_shifts)
all_days = range(num_days)
# para imprimir cada uno de los vectores se hace lo siguiente
print('La secuencia de enfermeras es asi:',list(all_nurses))
print('La secuencia de turnos es asi:',list(all_shifts))
print('La secuencia de dias es asi:',list(all_days))

"""Creación del modelo, sus variables  y formulacion de Restricciones iniciales"""

# Creacion del modelo
model = cp_model.CpModel()

# La matriz define asignaciones de turnos a enfermeras de la siguiente manera:
# turnos[(n, d, s)] es igual a 1 si el turno s se asigna a la enfermera n el día d, y 0 en caso contrario.
shifts = {}
for n in all_nurses:
    for d in all_days:
        for s in all_shifts:
            shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

# El siguiente codigo crea las restricciones del problema.
# Cada enfermera es asignada exactamente a un turno a la vez.
for d in all_days:
    for s in all_shifts:
        model.AddExactlyOne(shifts[(n, d, s)] for n in all_nurses)
# Cada enfermera trabaja como mucho en un solo turno al dia
for n in all_nurses:
    for d in all_days:
        model.AddAtMostOne(shifts[(n, d, s)] for s in all_shifts)

"""Se muestra cómo asignar turnos a las enfermeras de la manera más uniforme posible. """

# Aqui se trata de distribuir los turnos de manera uniforme, para que cada enfermera trabaje lo mismo
# usando la variable min_shifts_per_nurse 
print('La cantidad de turnos totales enteros es', num_shifts * num_days)
min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
print('El numero minimo de turnos de cada enfermera entero es ' , min_shifts_per_nurse)

"""Aqui se asegura el balance de los turnos
cuando no sea posible que el producto mostrado sea divisible por el número de enfermeras, en esos casos se procede asignar un turno más
"""

# filtra el caso cuando la division es exacta
if num_shifts * num_days % num_nurses == 0:
    max_shifts_per_nurse = min_shifts_per_nurse
else: # filtra el caso cuando la division es inexacta
    max_shifts_per_nurse = min_shifts_per_nurse + 1

print(' La cantidad maxima de turnos por enfermera es de ',(max_shifts_per_nurse))

for n in all_nurses:
    num_shifts_worked = []
    for d in all_days:
        for s in all_shifts:
            num_shifts_worked.append(shifts[(n, d, s)])
    
    model.Add(min_shifts_per_nurse <= sum(num_shifts_worked))
    # Para segurar que ninguna enfermera se le asigne más de un turno extra. 
    # La restricción no es necesaria en este caso, porque solo hay un turno extra. 
    # Pero para valores de parámetros diferentes, podría haber varios cambios adicionales,
    #  en cuyo caso la restricción es necesaria
    model.Add(sum(num_shifts_worked) <= max_shifts_per_nurse)

"""Ejecutar el Metodo solver del modelo"""

# Creacion del Solver
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
# Enumeracion de soluciones.
solver.parameters.enumerate_all_solutions = True

"""Creacion de una Clase exclusivamente para mostrar los resultados

"""

# funcion para reemplazar el indice por el nombre real de cada enfermera
def reemplazar_nombre(t):
  index_nurse=int(t[t.find('rse')+3:t.find('rse')+5])
  sustituir=dic_nomb_enferm[index_nurse+1][0]
  #print('susti',sustituir)
  palabra_reemplazar=' Nurse ' + str(index_nurse)
  #print('reemp',palabra_reemplazar)
  t=t.replace(palabra_reemplazar,sustituir)
  #print('t=',t)
  return t


class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
        global dic,dic_total
        dic_total={}        
        
        """Print intermediate solutions."""

        def __init__(self, shifts, num_nurses, num_days, num_shifts, limit):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self._shifts = shifts
            self._num_nurses = num_nurses
            self._num_days = num_days
            self._num_shifts = num_shifts
            self._solution_count = 0
            self._solution_limit = limit

        def on_solution_callback(self):
            global dic, turnos_, dic_total
            dic={}                        
            self._solution_count += 1
            #print('Solution %i' % self._solution_count)            
            for d in range(self._num_days):                
                #print('Day %i' % d)
                turnos_=[]
                for n in range(self._num_nurses):
                    is_working = False
                    for s in range(self._num_shifts):
                        if self.Value(self._shifts[(n, d, s)]):
                            is_working = True
                            #print('  Nurse %i works shift %i' % (n, s))
                            texto_nurse='  Nurse %i works shift %i' % (n, s)
                            t=reemplazar_nombre(texto_nurse)
                            turnos_.append(t)                            
                    if not is_working:                     
                        texto_nurse='  Nurse {} does not work'.format(n)
                        t=reemplazar_nombre(texto_nurse)
                        turnos_.append(t)
                dic[d]=turnos_
            if self._solution_count >= self._solution_limit:
                ##print('Stop search after %i solutions' % self._solution_limit)
                self.StopSearch()
            dic_total[self._solution_count]=dic
        def solution_count(self):
            return self._solution_count

"""Desplegar resultados"""

# Se van a Mostrar solo las soluciones validas que se coloque aqui
solution_limit = 75
solution_printer = NursesPartialSolutionPrinter(shifts, num_nurses,
                                                    num_days, num_shifts,
                                                    solution_limit)

solver.Solve(model, solution_printer)

# funcion para encontrar series repetidas 
def count_dups(nums):
    element = []
    freque = []
    if not nums:
        return element
    running_count = 1
    for i in range(len(nums)-1):
        if nums[i] == nums[i+1]:
            running_count += 1
        else:
            freque.append(running_count)
            element.append(nums[i])
            running_count = 1
    freque.append(running_count)
    element.append(nums[i+1])
    return element,freque

# para saber cual es el maximo dias consecutivos no trabajados
def maximo_NO_trabajos(elementos, frecuencia):
  lista_work=[]
  for i,ele in enumerate(elementos):
    if 'work' in ele: 
      lista_work.append(frecuencia[i])
  maximo=max(lista_work)
  return maximo

##Crea una tabla con la solucion por columnas para verificar el minimo y el maximo numnero de asignaciones consecutivas permitidas
#crear columnas y filas del dataframe
columnas=[] ; filas=[]
for nomb in dic_nomb_enferm.keys():
  columnas.append(str(dic_nomb_enferm[nomb][0]))
for f in range(num_days):
  #print(f)
  filas.append(str(f))


#Recorrer todas la soluciones
for sol in dic_total.items():  
  #df_escenario = pd.DataFrame(columns=columnas, index=filas) 
  for num_sol in sol:
    df_escenario = pd.DataFrame(columns=columnas, index=filas) 
    salir_solucion=0
    # para seleccionar solo los diccionarios y omitir los valores enteros que son indices de soluciones    
    try:
      for enfermera in num_sol.keys():
          turnitos=[]
          for nurse in (num_sol[enfermera]):
            nombre=nurse.split()[0] ; turno=nurse.split()[-1]
            turnitos.append(turno)
            #print(turnitos)
            #print(enfermera)
            #print(turno)
          #print(turnitos)
          df_escenario.loc[enfermera] = turnitos # guarda los turnos de cada enfermera
    except:
      indice_solucion=num_sol
    df_escenario=df_escenario.dropna(how='all')
    #print(df_escenario)
    # Recorrer cadacolumna y extraer los maximos no trabajados
    indice_columna=0
    for col in df_escenario.columns:      
      try:
        indice_columna+=1
        lista=list(df_escenario[col])
        (elementos, frecuencia)=count_dups(list(df_escenario[col]))
        MAX_No_trabajados=maximo_NO_trabajos(elementos, frecuencia) 
        VALOR_MAX_permitido=dic_contrato[dic_tipo_contrato[indice_columna]][0]
        ##print(MAX_No_trabajados) 
        #print(VALOR_MAX_permitido)       
        if int(VALOR_MAX_permitido)<int(MAX_No_trabajados):
          print('La solucion',indice_solucion,' No cumple la restriccion para la enfermera',col )          
          salir_solucion=1
          break             
      except:
        #print('e')
        pass
    if salir_solucion==1:      
      break
   # else: 
      #print('f')
df_escenario

# para recodificar los turnos y remmplazar por los nombres de los turnos
def reemplazar_turnos(df):
  for col in df.columns:
    for i in df.index:
      if df[col][i] =='work':
        df[col][i]='libre'
      else:
        for key in dic_turnos.keys():
          #print(df[col][i])
          #print(int(key)-1,df[col][i])
          try:
            if int(key-1)==int(df[col][i]):
              #print('yes')
              df[col][i]=dic_turnos[key][0]
          except:
            pass
          
               
                    
  return df
data=reemplazar_turnos(df_escenario)
data

# extraer el maximo numero de dias no laborados permitidos
def identificar_max_DIAS_permitidos(columna):
  for key in dic_nomb_enferm.keys():   
   if columna in dic_nomb_enferm[key][0]:
     tipo=(dic_tipo_contrato[key])
     maximo=(int(dic_contrato[tipo][0]))
  return maximo

# conseguir la fila donde se insertara el nuevo turno
def buscar_fila_frecuancia_max(nomb_col,max_permitido,frecuencia_max):  
  filas_totales=len(data)
  for i in data.index:
    fila_i=i
    cont_libre=0
    for fila in range(fila_i,filas_totales):
      if data[nomb_col][fila] =='libre':
        cont_libre+=1
      else:
        break
    if frecuencia_max==(cont_libre):
      index_libre=fila_i
      break
    else:
      index_libre=0
  return index_libre 

# funcion para intercambiar turnos y garantizar dias libres maximos permitidos
def intercambiar_turnos(nom_col,indice_reemplazar, max_permitido):
  for col in data.columns:
    if nom_col!=col:
      # escoger la columna a intercambiar turnos
      if (data[col][indice_reemplazar+max_permitido]).lstrip().rstrip()!='libre' and (data[col][indice_reemplazar+max_permitido-1]).lstrip().rstrip()!='libre':
        turno_reemplazar=data[col][indice_reemplazar+max_permitido]
        #print(col,turno_reemplazar)
        data[nom_col][indice_reemplazar+max_permitido]=turno_reemplazar
        data[col][indice_reemplazar+max_permitido]='libre'
        break

# Se hace un Algoritmo para reemplazar los turnos que No cumplen la restriccion 
# de dias maximos No laborados
for col in data.columns:
  # buscar le frecuencia maxima de dias No laborados de cada enfermera
  elem,frecuencia_max=count_dups(list(data[col]))
  # obtener el valor maximo de dias permitidosNo laborados
  max_permitido= identificar_max_DIAS_permitidos(col)
  #print(max_permitido)
  if np.max(np.array([frecuencia_max]))>max_permitido:
    #print(col)
    print('La enfermera ', col, 'No cumple con los dias maximos No laborables que son ',max_permitido)
    # Se busca el indice de fila donde se supera la Restriccion de dias libres maximos
    fila_max= buscar_fila_frecuancia_max(col, max_permitido,np.max(np.array([frecuencia_max])) )
    #print(fila_max)
    # Se intercambian turnos
    intercambiar_turnos(col,fila_max, max_permitido)

# La solucion final que cumple las Restricciones es
print('# La solucion final que cumple las Restricciones es')
print(data)
print()
# Statistics.
print('\nStatistics')
print('  - total cost      : %i' % solver.NumConflicts())
print('  - branches       : %i' % solver.NumBranches())
print('  - wall time      : %f s' % solver.WallTime())
print('  - solutions found: %i' % solution_printer.solution_count())
