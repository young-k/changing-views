"""
Train TensorFlow models.
"""

import tensorflow as tf
from models import SiameseRNN
from loader import Loader
from tqdm import tqdm

N_EPOCHS = 1000

train = Loader('./data/training')
valid = Loader('./data/testing')
model = SiameseRNN()
saver = tf.train.Saver()
best = 0

with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)
    sess.run(init)
    for n in tqdm(range(N_EPOCHS)):
        for i in tqdm(range(train.n_batches)):
            comment1, comment2, labels = train.next_batch()
            train_dict = {model.input1: comment1, model.input2: comment2, model.labels: labels}
            loss, _ = sess.run([model.loss, model.train_step], feed_dict=train_dict)
        if (n % 2) == 0:
            acc_va = 0
            for j in tqdm(range(valid.n_batches)):
                comment1, comment2, labels = valid.next_batch()
                valid_dict = {model.input1: comment1, model.input2: comment2, model.labels: labels}
                acc = sess.run(model.accuracy, feed_dict=valid_dict)
                acc_va += acc
            acc_va /= valid.n_batches
            print('Training loss: {:.3f}, Validation accuracy: {:.2f}%'.format(loss, 100*acc_va))
            if acc_va > best:
                best = acc_va
                saver.save(sess, './models')
            else:
                saver.restore(sess, './models')
