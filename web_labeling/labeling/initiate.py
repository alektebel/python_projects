from .models import Datas, Label
import os
import numpy as np


NAME = ''
LABEL = ''
TEST = ''

d = Datas(name = NAME, directory_to_label = LABEL, directory_to_test = TEST)
props  = []
for i in range(len(os.listdir(directory_to_test))):
    props.append(len(os.listdir(os.listdir(directory_to_test)[i])))
props = np.asarray(props)
props = props/np.sum(props)
d.props = props
d.save()
start_data(d)

