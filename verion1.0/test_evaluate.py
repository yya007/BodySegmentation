import tensorflow as tf
import FCN1
from PIL import Image
import numpy as np
import tensorflow as tf
import time
import sys
from scipy.misc import imsave
from test_bd import * 
from evaluate import *  
    
epoch=1
state="norandomrun"
#load network_________________________
number_of_classes=19
size=16
speed=1e-5

#sess=tf.InteractiveSession()
x = tf.placeholder(tf.float32, shape=[None,512,512,3])
y_ = tf.placeholder(tf.float32, shape=[None,512,512,number_of_classes])
keep_prob = tf.placeholder(tf.float32)
y_conv=FCN1.FCN(x,keep_prob,number_of_classes=number_of_classes)
tf.add_to_collection("y_conv", y_conv)
cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
train_step = tf.train.AdamOptimizer(speed).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,3), tf.argmax(y_,3))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
result =tf.argmax(y_conv,3)
saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
      
    modelname=('model_%s_%d'%(state,0))
    print ('start loading %s'%(modelname))                     
    modeldir=('../network/%s/%s'%(modelname,modelname))
    #saver = tf.train.import_meta_graph(modeldir+'.meta')
    saver.restore(sess,modeldir)
    #testing---------------------------


    resdir='../res/%s_%d/'%(state,epochind-1)
    testinsample(sess,result,x,y_,keep_prob,resdir=resdir,printstep=True,number_of_classes=number_of_classes,saveres=False)
    testall(sess,result,x,y_,keep_prob,resdir=resdir,printstep=True,number_of_classes=number_of_classes,saveres=False)
