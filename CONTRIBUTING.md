# PREAPP
preapp is node based. this design choice is so that you as a developer can utilize work done so far and add new functionality to an existing pipeline. 


## Get Started Developing
preapp is made of nodes and each node contains its own functionality in preapp. here I will outline the basic parameters and functions of each node to help you get started contributing to preapp.


### Important Node parameters
```python
 # this is the unique string identifier of this node
name: str

# these are the CLI prompt questions this node needs to execute
questions: List[Question] 

# this is a list of the names of nodes that need to execute before this node can execute
parents: List[str] = [],

# this is a list of the names of nodes that need to execute after this node has executed
children: List[str] = [],

# this is the priority of this node. this is used to rank nodes executed at the same 
# level in the tree
priority: int = 0,
        
# this is a flag if the node should write its data to the output file        
serializable: bool = True,
```

### Important Node functions
```python
def pre_process(self) -> None:
    # this function will execute before this node prompts its questions

def post_process(self, responses: Dict[str, Any]) -> None:
    # this function will execute after this node prompts its questions.
    # responses is a dictionary of the questions and their values

@staticmethod
def get_full_response() -> Dict[str, Any]:
    # this function will return the reponses for all nodes that have executed. 
    # the format is 
    # {
    #   "<node_name>": {
    #       "<question_name>": "<question_value>",
    #       ...
    #   },
    #   ...
    # }

@staticmethod
def register(node: Node) -> None:
    # this function takes in an instance of a node and will add it to the parsing tree
    # Note: this function should be placed in the file the node is defined in and should be 
    # called when the application starts 
```

### Example Node
this is a small example of what a node might look like 
```python
# in preapp/nodes/example_node.py

from .. import Node, InputQuestion

class ExampleNode(Node):
    """This is an example Node """

    def __init__(self):
        super(ExampleNode, self).__init__(
            # name of the node
            "example", 

            # questions for the node
            [
                InputQuestion("name", "Enter your name"),
                InputQuestion(
                    "bio", "Enter a quick bio about yourself"
                ),
            ],
        )

    def pre_process(self) -> None:
        print ("processing example node . . . ")

    def post_process(self, responses: Dict[str, Any]) -> None:
        print ("finished processing example node")

Node.register(ExampleNode())
```