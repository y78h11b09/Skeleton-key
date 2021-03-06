from __future__ import division

import tensorflow as tf
import json
from ops import resnet, level1_model


class Level1Model(object):

    def __init__(self, config, mode):
        self.config = config
        self.mode = mode
        # self.train_resnet = (train_resnet & (mode == 'training'))

        self.weight_initializer = tf.contrib.layers.xavier_initializer()
        self.const_initializer = tf.constant_initializer(0.0)
        self.emb_initializer = tf.random_uniform_initializer(minval=-1.0, maxval=1.0)
        self.level1_word2ix = json.load(open('data/train/word2ix_stem.json'))

        self.level1_model = level1_model.Level1Model(word_to_idx=self.level1_word2ix,
                                                     dim_feature=config.LEVEL1_dim_feature,
                                                     dim_embed=config.LEVEL1_dim_embed,
                                                     dim_hidden=config.LEVEL1_dim_hidden,
                                                     alpha_c=config.LEVEL1_alpha, dropout=config.LEVEL1_dropout,
                                                     n_time_step=config.LEVEL1_T,
                                                     train=(self.mode == 'training'))

    def build(self):
        self.level1_model.init_inference()
        self.level1_model.inference_1step()
        self.level1_model.inference_rest()
        if self.mode == 'training':
            return self.level1_model.build_training()
        # else: