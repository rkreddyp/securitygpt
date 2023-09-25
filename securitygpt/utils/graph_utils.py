from graphviz import Digraph

#class ExecuteTaskGraph(task_graph):

    #def __init__(self, task_graph):
        #print ('init ExecuteTaskGraph')

    #def execute_tool(tool_name, tool_args):
        #args = ast.literal_eval(tool_args)
        #tool_instance = globals()[tool_name]()
        #tool_result = tool_instance.run( tool_args)
        #return tool_result


def visualize_knowledge_graph(kg):
    print (kg.keys())
    dot = Digraph(comment="Knowledge Graph")

    # Add nodes
    for node in kg['nodes']:
        dot.node(str(node['id']), node['label'], color=node['color'])

    # Add edges
    for edge in kg['edges']:
        #dot.edge(str(edge['source']), str(edge['target']), label=edge['label'], color=edge['color'])
        dot.edge(str(edge['source']), str(edge['target']), label=edge['label'])

    # Render the graph
    #dot.render("knowledge_graph.gv", view=True)
    return dot


def generate_graphviz(data):
    dot = Digraph()

    # Create nodes
    for item in data:
        task_id = str(item['id'])
        task_name =  f"{task_id}: {item['task']}"
        tool_name = f"{item['tool_name']}"
        dot.node(task_id, task_name + "\n Tool to Use:" + tool_name)

    # Create edges
    for item in data:
        task_id = str(item['id'])
        subtasks = item['subtasks']
        for subtask in subtasks:
            dot.edge(task_id, str(subtask))
            #dot.edge(str(subtask), task_id)
    # Render the graph
    #dot.format = 'png'
    dot.attr(size=f"{10},{10}", dpi='50')
    dot.render('graph', view=True, cleanup=True, format='svg')
    

def code_to_work ():
        
    # Generate the graph
    generate_graphviz(plan.dict()['task_graph'])

    from IPython.display import Image

    from IPython.display import Image, display, HTML, SVG

    # Path to your image
    image_path = 'graph.png'

    # Desired height for the image (in pixels)
    image_height = 1000
    image_width = 1000
    # Create an HTML tag with the image and set the height
    image_html = f'<img src="{image_path}" style="height:{image_height}px; width:{image_width}px">'

    # Display the image in the notebook
    #display(HTML(image_html))

    #display(Image(filename='graph.png', width=1000, height=2000)    )
    display(SVG(filename='graph.svg')    )