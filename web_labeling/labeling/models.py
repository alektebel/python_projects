from django.db import models
import json
from django.contrib.auth.models import User
import os
from django.contrib.postgres.fields import ArrayField
#print(os.getcwd())
#with open('labeling/static/metadata.json', 'r') as f:
#    dic = json.load(f)
#num_clases = len(dic)-1
#m = dic['num_datos']
num_clases = 2
m = 50

###################################
#
#
#    m    o    d    e    l    s
#
#
####################################

#DATA STUFF

class Datas(models.Model):
    name = models.TextField(max_length = 30, default = 'DATANAME')
    directory_to_label = models.TextField(max_length = 30, default = 'DIR_LABEL')    
    directory_to_test = models.TextField(max_length = 30, default = 'DIR_TEST')
    props = ArrayField(models.FloatField(), size = num_clases)
    def __str__(self):
        return self.name


class Datatest(models.Model):
    name = models.TextField(max_length = 30, default = 'NAME')
    label = models.TextField(max_length = 30, default = 'LABEL')
    datas = models.ForeignKey(Datas, on_delete = models.CASCADE, related_name = 'test_data')
    def __str__(self):
        return self.name + ' label is '+self.label

class Data(models.Model):
    P = models.BooleanField()
    name = models.TextField(max_length = 20, default = 'NAME')
    datas = models.ForeignKey(Datas, on_delete = models.CASCADE, related_name = 'label_data')
    tl = models.TextField(max_length = 30, default = 'class_name')
    def __str__(self):
        return self.name

#This function initialize all the data of the directory of datas
def start_data(datas):
    print('sdf')
    print(os.listdir(datas.directory_to_label))
    for file1 in os.listdir(datas.directory_to_label):
        print('extraction file from file '+os.path.join(datas.directory_to_label, file1))
        temp1 = Data.objects.create(datas_id = datas.id, P = False, name = file1)
        temp1.save()
        datas.label_data.add(temp1)

    for label in os.listdir(datas.directory_to_test):

        for file2 in os.listdir(os.path.join(datas.directory_to_test, label)):
            temp2 = Datatest.objects.create(datas_id = datas.id, name = file2, label = label)
            temp2.save()
            print('extraction file from file '+os.path.join(datas.directory_to_test, file2))

            datas.test_data.add(temp2)
    pass

#LABEL STUFF

#This class initialize a labeler in the database
class Etiquetador(models.Model):
    p = ArrayField(
            ArrayField(
                models.FloatField(),
                size = num_clases),
             size = num_clases)
    
    n = ArrayField(
            models.IntegerField(),
    size = num_clases)

    #p = models.FloatField()
    #n = models.IntegerField()

    name = models.TextField(max_length = 20, default = 'NAME')
    test_passed = models.BooleanField()
    datas = models.ForeignKey(Datas, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' precision of user ' + str(self.p) + ' test_passed ' + str(self.test_passed)

class Label(models.Model):
    clase = models.IntegerField()
    nombre_clase = models.TextField(max_length = 30, default = 'NOMBRE_CLASE')
    etiquetador = models.ForeignKey(Etiquetador, on_delete=models.CASCADE)
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre_clase
class Labeltest(models.Model):
    clase = models.IntegerField()
    nombre_clase = models.TextField(max_length = 30, default = 'NOMBRE_CLASE')
    etiquetador = models.ForeignKey(Etiquetador, on_delete=models.CASCADE)
    datatest = models.ForeignKey(Datatest, on_delete=models.CASCADE, name = 'remain_datatest')
    def __str__(self):
        return self.nombre_clase

