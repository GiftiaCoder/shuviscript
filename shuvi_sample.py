import shuvi.graph as graph
import shuvi.method.method as method
import tensorflow as tf

class InputMethod(method.ShuviMethod):
    def __init__(self, name, graph, inputs):
        super().__init__(name, graph, inputs)
        self.register_output('output', tf.Variable(tf.random_uniform([4], -1.0, 1.0)))

class OutputMethod(method.ShuviMethod):
    def __init__(self, name, graph, inputs):
        super().__init__(name, graph, inputs)

        offset = tf.placeholder(tf.float32)
        self.register_placeholder('offset', offset)

        input = inputs['input.output']
        output = input * input + offset
        self.register_output('output', output)

script = 'input = (output)()input_method()\n' \
         'output = (output)(offset)output_method(input.output)'

graph = graph.ShuviGraph(script, {
    'input_method': InputMethod,
    'output_method': OutputMethod,
})
graph.build_self()

with tf.Session() as sess:
    graph.init(sess)
    print(graph.run(sess, 'output.output', {
        'output.offset': 1
    }))
    print(graph.run(sess, 'output.output', {
        'output.offset': 10
    }))