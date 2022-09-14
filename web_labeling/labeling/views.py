from django.shortcuts import render
import random
# Create your views here.
from .models import Label, Etiquetador, Datas, Data, Datatest, Labeltest
import os
import numpy as np



###################
#  V  I  E  W  S  #
###################




alpha = 0.99
beta = 0.95
#dataset = Datas.objects.filter(pk = 3)[0]
#print(dataset)
#num_clases = len(os.listdir(dataset.dir:ectory_to_test))
#print(num_clases)
#props = dataset.props

def gen_name_data(request):
    m = 24
    index = int(random.random()*m)
    m = 24
    index = int(random.random()*m)
    if random.random() > 0.5:
        N = 'O'
    else:
        N = 'R'
    name = N+'_'+str(index)+'.jpg'
    return name


def subestimar_user(user):
        nuevo_user = user.p
        for j in range(num_clases):
            nuevo_user[j][j] = (user.p[j][j] + (np.sqrt(user.p[j][j]*(1-user.p[j][j])/user.n[j]))*stats.norm.ppf(prob_sub))
            r = 1 - nuevo_user[j][j]
            z = np.sum(nuevo_user[:,j]) - nuevo_user[j, j]
            temp = np.ones(num_clases)*r/z
            temp[j] = 1
            nueva_user[:,j] = nuevo_user[:,j]*temp
        return user.p

def get_p_sub(et, prob_sub, datas):
    num_clases = len(datas.props)
    temp = et.p
    if np.sum(np.sum(np.asarray(et.p))) != np.sum(np.asarray(et.n)):
        print(np.asarray(et.p))
        return np.asarray(et.p)
    else:
        for i in range(num_clases):
            for j in range(num_clases):
                temp[i][j] = et.p[i][j]/et.n[j]
    temp = np.asarray(temp)
    return temp
    #p_sub = np.asarray(temp)
    #for j in range(num_clases):
    #    p_sub[j,j] = (p_sub[j,j] + (np.sqrt(p_sub[j,j]*(1-p_sub[j,j])/et.n[j]))*stats.norm.ppf(prob_sub))
    #    r = 1 - temp[j][j]
    #    z = np.sum(np.asarray(et.p)[:,j]) - et.p[j, j]
    #    temp = np.ones(num_clases)*r/z
    #    temp[j] = 1
    #    p_sub[:,j] = p_sub[:,j]*temp
    #print(p_sub)
    #return p_sub


def get_precs(c):
    precs = np.zeros(num_clases)
    for n in range(num_clases):
        precs[n] = c[n, n]/np.sum(c, axis = 0)[n]
    return precs

def get_conf_final(coleccion, data):
    tabla = np.zeros((num_clases, num_clases))
    for i in range(len(data)):
        tabla[coleccion[i], data[i]] = tabla[coleccion[i], data[i]]+1
    
    return tabla


def get_name_class(clas_ind, datas):
    return os.listdir(datas.directory_to_test)[clas_ind]


def comprobar_prob(lista, alpha, datas):
    probs = list(datas.props)
    temp = []

    for k in range(len(datas.props)):
        temp.append([])
        for i in lista:
            if i.clase == k:
                temp[k].append(Etiquetador.objects.filter(pk = i.etiquetador_id)[0])
    probs = np.asarray(probs)
    for k in range(len(datas.props)):
        for i, vot in enumerate(temp):
            if len(vot) >= 1:
                for le in vot:
                    p_sub = get_p_sub(le, beta, datas)
                    if i == k:
                        probs[k] = probs[k]*p_sub[k,k]
                    elif i!= k:
                        probs[k] = probs[k]*p_sub[i,k]
    probs = probs/np.sum(probs)
    '''Esta función solicita la clase de la etiqueta que se quiere comprobar, E, un diccionario que contiene los votantes de
    cada clase, y la lista de usuarios.'''
    
    if max(probs) > alpha:
        return [True, probs.get_index(max(probs))]
    else:
        return [False, 'Nada']

def get_index_class(clas, datas):
    return os.listdir(datas.directory_to_test).index(clas)

def get_name_class(clas_ind, datas):
    return os.listdir(datas.directory_to_test)[clas_ind]


def get_done_datatest(et):
    lis = et.labeltest_set.all()
    aux = []
    for i in lis:
        aux.append(Datatest.objects.filter(pk = i.remain_datatest_id)[0].name)
    print('DONE')
    print(len(set(aux)))
    return aux


def get_done_data(et):
    lis = et.label_set.all()
    print(lis)
    aux = []
    for i in lis:
        aux.append(Data.objects.filter(pk = i.data_id)[0].name)
    print(aux)
    return aux


def get_labeled_data(datas):
    aux = []
    for i in datas.label_data.all():
        if i.P == True:
            aux.append(i.name)
        else:
            pass
    return aux





def detail_labeling(request, datas_name, data):

   #We first get the datas from the objects 
    datas = Datas.objects.filter(name = datas_name)[0]


    #If a labeler doesn't exists for the current user, and the current data, we create a new one
    if len(Etiquetador.objects.filter(name = request.user.get_username(), datas_id = datas.id)) == 0:
        print('we create a labeler for the user' + request.user.get_username())
        t = []
        for i in range(len(datas.props)):
            t.append([])
            for j in range(len(datas.props)):
                t[i].append(0)
        et = Etiquetador.objects.create(p = t, n = t[0], name = request.user.get_username(), test_passed = False, user_id = request.user.id, datas_id = datas.id)
        et.save()
    else:

        #If the labeler does exists, we filter that labeler
        et = Etiquetador.objects.filter(name = request.user.get_username(), datas_id = datas.id)[0]
    

    #Does the user has passed the test stage?
    temp = []
    done = get_done_datatest(et)
    
    for clas in os.listdir(datas.directory_to_test):
    
        if len([element for element in os.listdir(os.path.join(datas.directory_to_test, clas)) if element not in done]) == 0:
            temp.append(True)
        else:
            temp.append(False)

    et.test_passed = all(temp)


    temp2 = []
    for nombre in os.listdir(datas.directory_to_test):
        temp2 += os.listdir(os.path.join(datas.directory_to_test, nombre))
    done = get_done_datatest(et)

    ####  T E S T  P H A S E ######
    if et.test_passed == False:
        datatest = Datatest.objects.filter(name = data)[0]
        print('INTERESTING THING')
        print(hasattr(request, 'name_real'))
        if hasattr(request, 'name_real') == False:
            for nombre in os.listdir(datas.directory_to_test):
                temp2 += os.listdir(os.path.join(datas.directory_to_test, nombre))
            done = get_done_datatest(et)
            name_real_in = random.choice([element for element in temp2 if element not in done])
            name_class_in = Datatest.objects.filter(name = name_real_in)[0].label
            request.name_real = name_real_in
            request.name_class = name_class_in

        name_real = request.name_real
        name_class = request.name_class
        next_datatest = Datatest.objects.filter(name = name_real, nombre_clase = name_class)[0]
        temp2 = []
        print('We vote for '+datatest.nombre_clase)
        print('If the class if (cor) ' + name_class)
        for nombre_clase in os.listdir(datas.directory_to_test):
        
            if nombre_clase in request.POST.keys():
                l = Labeltest(clase = get_index_class(nombre_clase, datas),
                        nombre_clase = nombre_clase,
                        etiquetador_id = et.id,
                        remain_datatest_id = Datatest.objects.filter(name = name_real)[0].id)
                
                et.p[get_index_class(nombre_clase, datas)][ get_index_class(name_class, datas)] += 1
                et.n[get_index_class(name_class, datas)] += 1
                
                l.save()
                et.labeltest_set.add(l)
                et.save()
        name = name_real

        temp2 = []
        for nombre in os.listdir(datas.directory_to_test):
            temp2 += os.listdir(os.path.join(datas.directory_to_test, nombre))
        done = get_done_datatest(et)
        name_real_next = random.choice([element for element in temp2 if element not in done])
        name_class_next = Datatest.objects.filter(name = name_real)[0].label

        context = {
             'title' : "TEST"+request.user.username+str(len([element for element in temp2 if element not in done])),
            'user_id': request.user.id,
            'name' : name,
            'path' : os.path.join(name_class, name_real),
            'CLASES': os.listdir(datas.directory_to_test),
            'flag_test':True,
            'next_data':next_data_test,

            }
        
        return render(request, 'label.html', context)

    ## N O R M A L I Z E
    #if np.sum(np.sum(np.asarray(et.p), axis = 1)) == np.sum(np.asarray(et.n)):
    #    print('This is TRUE ########################################################')
    #    for i in range(len(et.n)):
    #        for j in range(len(et.n)):
    #            print('NORMALIZATION')
    #            et.p[i][j] = et.p[i][j]/et.n[j] 
    #Since the test_passed was true, the following code is executed. This only shows the user a bunch of images unlabeled that we want to label    
    #et.save()






    # t r a i n
    if et.test_passed == True:
        temp3 = os.listdir(datas.directory_to_label)
        done = get_done_data(et)
        labeled = get_labeled_data(datas)
        if len([element for element in temp3 if element not in done+labeled]) == 0:
            context = {
                    'flag' :True

                    }
        
            return render(request, 'home.html', context)
        name_real = random.choice([element for element in temp3 if element not in done+labeled])
        print('Quedan' + str(len([element for element in temp3 if element not in done+labeled])) + 'imagenes') 
        data = Data.objects.filter(name = name_real)[0]

        #dataname = gen_name_data(request)
        #data = Data.objects.filter(name = dataname)[0]
        #name = gen_name_data(request)
        #data = Data.objects.filter(name = name)[0]
        temp3 = os.listdir(datas.directory_to_label)
        done = get_done_data(et)
        labeled = get_labeled_data(datas)
        if len([element for element in temp3 if element not in done+labeled]) == 0:
        
            context = {
                    'flag' : True,
                    }
            return render(request, 'home.html', context)

        for nombre_clase in os.listdir(datas.directory_to_test):
            if request.POST.get(nombre_clase) == nombre_clase:
                l = Label(nombre_clase = nombre_clase, clase = os.listdir(os.path.join(os.getcwd(), datas.directory_to_test)).index(nombre_clase))
                try:
                    et = Etiquetador.objects.filter(name = request.user.get_username())[0]
                except:
                    print('labeler does not exists')
                    return render(request, 'label.html')

                l.data_id = data.id
                l.etiquetador_id = et.id
                l.save()


    
        if comprobar_prob(data.label_set.all(), alpha, datas)[0] == True:
            data.P = True
            print('ETIQUETADA '+data.name)
            data.tl = comprobar_prob(data.label_set.all(),alpha, datas)[1]
        context = {
                'title' : "TRAIN"+request.user.username+str(len([element for element in temp3 if element not in done])),
                'user_id': request.user.id,
                'name' : name_real,
                'CLASES': os.listdir(datas.directory_to_test),
            
                }
        return render(request, 'label.html', context)


