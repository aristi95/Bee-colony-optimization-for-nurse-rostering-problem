

from ortools.sat.python import cp_model 
import pandas as pd
import numpy as np

Scenario = input("Nombre del archivo de escenario: ")
historia = input("Nombre del archivo de historia: ")
semana = input("Nombre del archivo de escenario: ")

contador_nombres=0 
dic_nomb_enferm={} 
contador_turnos=0 
dic_turnos={} 

with open("./n005w4/" + Scenario) as archivo:
    for linea in archivo:
      if "SCENARIO =" in linea: escenario = linea [linea.find('=')+1:-1]
      if "NURSES =" in linea: 
        num_nurses=int(linea[linea.find('=')+1:linea.find('n')]) 
        contador_nombres+=1 
      if contador_nombres>=1 and (linea.split())[0]!='NURSES': 
        nombre_enfermera=(linea.split())[0] 
        dic_nomb_enferm[contador_nombres]=nombre_enfermera 
        contador_nombres+=1
      if "SHIFT_TYPES =" in linea: 
        num_shifts=int(linea[linea.find('=')+1:linea.find('n')])  
        contador_turnos+=1 
      if contador_turnos>=1 and contador_turnos<=num_shifts :       
        if len (linea.split())==2: 
          tipo_turno=(linea.split())[0] 
          min_max_turnos=(linea.split())[1]
          dic_turnos[contador_turnos]=[tipo_turno,min_max_turnos]
          contador_turnos+=1
      if "WEEKS =" in linea: num_days=7*int(linea[linea.find('=')+1:linea.find('n')]) 
  
      
print('***  DATOS GENERALES DEL PROBLEMA ***')
print(' ')
print('El Escenario es:', escenario)
print('El numero de Enfermeras es:', num_nurses)
print('El numero de Turnos es:', num_shifts)
print('El numero de dias es:', num_days)
print('Los nombres de las enfermeras son:',dic_nomb_enferm)
print('Los tipos de turnos y sus rangos maximos y minimos son:',dic_turnos)

contador_historico=0 
with open("./n005w4/" + historia) as archivo:
    for linea in archivo:
      if 'NURSE_HISTORY' in linea:
        contador_historico+=1  
      if contador_historico>=1 and (linea.split())[0]!='NURSE_HISTORY':
        num_dias_trabajados= (linea.split())[-2]
        num_dias_NO_trabajados= (linea.split())[-1]
        dic_nomb_enferm[contador_historico]=[dic_nomb_enferm[contador_historico],num_dias_trabajados,num_dias_NO_trabajados]
        contador_historico+=1

for enf in dic_nomb_enferm.values():
  print('La cantidad de dias consecutivos trabajados previos de ',enf[0],' fueron:', enf[1])
  print('La cantidad de dias consecutivos NO trabajados previos de ',enf[0],' fueron:', enf[2])


contador_nombres=0
contador_contrato=0
dic_contrato={}
dic_tipo_contrato={}

with open("./n005w4/" + Scenario) as archivo:
    for linea in archivo:    
      if "NURSES =" in linea: 
        num_nurses=int(linea[linea.find('=')+1:linea.find('n')]) 
        contador_nombres+=1 
      if contador_nombres>=1 and (linea.split())[0]!='NURSES': 
        contrato=(linea.split())[1] 
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
with open("./n005w4/" + semana) as archivo:
    for linea in archivo:
      if 'REQUIREMENTS' in linea:
        contador_req+=1
      if contador_req>=1 and contador_req<=6:
        if (linea.split())[0]!='REQUIREMENTS':            
          contador_req+=1


all_nurses = range(num_nurses)
all_shifts = range(num_shifts)
all_days = range(num_days)
print('La secuencia de enfermeras es asi:',list(all_nurses))
print('La secuencia de turnos es asi:',list(all_shifts))
print('La secuencia de dias es asi:',list(all_days))


model = cp_model.CpModel()

shifts = {}
for n in all_nurses:
    for d in all_days:
        for s in all_shifts:
            shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))
for d in all_days:
    for s in all_shifts:
        model.AddExactlyOne(shifts[(n, d, s)] for n in all_nurses)
for n in all_nurses:
    for d in all_days:
        model.AddAtMostOne(shifts[(n, d, s)] for s in all_shifts)


print('La cantidad de turnos totales enteros es', num_shifts * num_days)
min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
print('El numero minimo de turnos de cada enfermera entero es ' , min_shifts_per_nurse)


if num_shifts * num_days % num_nurses == 0:
    max_shifts_per_nurse = min_shifts_per_nurse
else: 
    max_shifts_per_nurse = min_shifts_per_nurse + 1

print(' La cantidad maxima de turnos por enfermera es de ',(max_shifts_per_nurse))

for n in all_nurses:
    num_shifts_worked = []
    for d in all_days:
        for s in all_shifts:
            num_shifts_worked.append(shifts[(n, d, s)])
    
    model.Add(min_shifts_per_nurse <= sum(num_shifts_worked))
    model.Add(sum(num_shifts_worked) <= max_shifts_per_nurse)


solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
solver.parameters.enumerate_all_solutions = True

def reemplazar_nombre(t):
  index_nurse=int(t[t.find('rse')+3:t.find('rse')+5])
  sustituir=dic_nomb_enferm[index_nurse+1][0]
  palabra_reemplazar=' Nurse ' + str(index_nurse)
  t=t.replace(palabra_reemplazar,sustituir)
  return t


class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
        global dic,dic_total
        dic_total={}        

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
            for d in range(self._num_days):    
                turnos_=[]
                for n in range(self._num_nurses):
                    is_working = False
                    for s in range(self._num_shifts):
                        if self.Value(self._shifts[(n, d, s)]):
                            is_working = True
                            texto_nurse='  Nurse %i works shift %i' % (n, s)
                            t=reemplazar_nombre(texto_nurse)
                            turnos_.append(t)                            
                    if not is_working:                     
                        texto_nurse='  Nurse {} does not work'.format(n)
                        t=reemplazar_nombre(texto_nurse)
                        turnos_.append(t)
                dic[d]=turnos_
            if self._solution_count >= self._solution_limit:
                self.StopSearch()
            dic_total[self._solution_count]=dic
        def solution_count(self):
            return self._solution_count


solution_limit = 10
solution_printer = NursesPartialSolutionPrinter(shifts, num_nurses,
                                                    num_days, num_shifts,
                                                    solution_limit)

solver.Solve(model, solution_printer)

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

def maximo_NO_trabajos(elementos, frecuencia):
  lista_work=[]
  for i,ele in enumerate(elementos):
    if 'work' in ele: 
      lista_work.append(frecuencia[i])
  maximo=max(lista_work)
  return maximo

columnas=[] ; filas=[]
for nomb in dic_nomb_enferm.keys():
  columnas.append(str(dic_nomb_enferm[nomb][0]))
for f in range(num_days):
  filas.append(str(f))


for sol in dic_total.items():   
  for num_sol in sol:
    df_escenario = pd.DataFrame(columns=columnas, index=filas) 
    salir_solucion=0
    try:
      for enfermera in num_sol.keys():
          turnitos=[]
          for nurse in (num_sol[enfermera]):
            nombre=nurse.split()[0] ; turno=nurse.split()[-1]
            turnitos.append(turno)
          df_escenario.loc[enfermera] = turnitos
    except:
      indice_solucion=num_sol
    df_escenario=df_escenario.dropna(how='all')
    indice_columna=0
    for col in df_escenario.columns:      
      try:
        indice_columna+=1
        lista=list(df_escenario[col])
        (elementos, frecuencia)=count_dups(list(df_escenario[col]))
        MAX_No_trabajados=maximo_NO_trabajos(elementos, frecuencia) 
        VALOR_MAX_permitido=dic_contrato[dic_tipo_contrato[indice_columna]][0]    
        if int(VALOR_MAX_permitido)<int(MAX_No_trabajados):
          print('La solucion',indice_solucion,' No cumple la restriccion para la enfermera',col )          
          salir_solucion=1
          break             
      except:
        pass
    if salir_solucion==1:      
      break
df_escenario


def reemplazar_turnos(df):
  for col in df.columns:
    for i in df.index:
      if df[col][i] =='work':
        df[col][i]='libre'
      else:
        for key in dic_turnos.keys():
          try:
            if int(key-1)==int(df[col][i]):
              df[col][i]=dic_turnos[key][0]
          except:
            pass         
  return df
data=reemplazar_turnos(df_escenario)
data


def identificar_max_DIAS_permitidos(columna):
  for key in dic_nomb_enferm.keys():   
   if columna in dic_nomb_enferm[key][0]:
     tipo=(dic_tipo_contrato[key])
     maximo=(int(dic_contrato[tipo][0]))
  return maximo


def buscar_fila_frecuencia_max(nomb_col,max_permitido,frecuencia_max):  
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


def intercambiar_turnos(nom_col,indice_reemplazar, max_permitido):
  for col in data.columns:
    if nom_col!=col:
      if (data[col][indice_reemplazar+max_permitido]).lstrip().rstrip()!='libre' and (data[col][indice_reemplazar+max_permitido-1]).lstrip().rstrip()!='libre':
        turno_reemplazar=data[col][indice_reemplazar+max_permitido]
        data[nom_col][indice_reemplazar+max_permitido]=turno_reemplazar
        data[col][indice_reemplazar+max_permitido]='libre'
        break


for col in data.columns:
  elem,frecuencia_max=count_dups(list(data[col]))
  max_permitido= identificar_max_DIAS_permitidos(col)
  if np.max(np.array([frecuencia_max]))>max_permitido:
    print('La enfermera ', col, 'No cumple con los dias maximos No laborables que son ',max_permitido)
    fila_max= buscar_fila_frecuencia_max(col, max_permitido,np.max(np.array([frecuencia_max])) )
    intercambiar_turnos(col,fila_max, max_permitido)


print('# La solucion final que cumple las Restricciones es')
print(data)
print()
print('\nStatistics')
print('  - total cost      : %i' % solver.NumConflicts())
print('  - branches       : %i' % solver.NumBranches())
print('  - wall time      : %f s' % solver.WallTime())
print('  - solutions found: %i' % solution_printer.solution_count())
