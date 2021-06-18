import os, sys
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line
               in tf.gfile.GFile("retrained_labels.txt")]

# Unpersists graph from file
f = tf.gfile.FastGFile("retrained_graph.pb", 'rb')
graph_def = tf.GraphDef()
graph_def.ParseFromString(f.read())
tf.import_graph_def(graph_def, name='')

def prediction(filename):
    image_path = filename
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()
    with tf.Session() as sess:
        result = []
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            result.append('%s,%.5f' % (human_string, score))
        #tf.reset_default_graph()
        return result
