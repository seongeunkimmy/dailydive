import tensorflow as tf
from keras.models import load_model
from transformers import AutoTokenizer, TFBertForSequenceClassification
import numpy as np
import os


def create_klue_model():
    max_len = 128
    model_name = "klue/bert-base"
    base_model = TFBertForSequenceClassification.from_pretrained(model_name, num_labels=6, from_pt=True)

    input_ids_layer = tf.keras.layers.Input(shape=(max_len,), dtype=tf.int32, name='input_ids')
    attention_masks_layer = tf.keras.layers.Input(shape=(max_len,), dtype=tf.int32, name='input_masks')
    segments_layer = tf.keras.layers.Input(shape=(max_len,), dtype=tf.int32, name='int_segments')

    bert_outputs = base_model([input_ids_layer, attention_masks_layer, segments_layer])

    bert_output = bert_outputs[0]

    dropout_rate = 0.5
    num_class = 6
    dropout = tf.keras.layers.Dropout(dropout_rate)(bert_output)
    sentiment_layer = tf.keras.layers.Dense(num_class, activation='softmax',
                                            kernel_initializer=tf.keras.initializers.he_uniform())(dropout)
    sentiment_model = tf.keras.Model([input_ids_layer, attention_masks_layer, segments_layer], sentiment_layer)

    optimizer = tf.keras.optimizers.AdamW(learning_rate=3e-5)
    sentiment_model.compile(optimizer=optimizer,
                            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                            metrics=['accuracy'])

    sentiment_model.load_weights(filepath='C:/pycharm/dailydive/dailydive_project/models/best_model_val_adamw.h5')

    return sentiment_model


def load_klue_tokenizer():
    model_name = "klue/bert-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    return tokenizer