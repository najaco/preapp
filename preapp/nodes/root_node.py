from .. import Node


class RootNode(Node):
    """ The root node of the preapp application, All required entry point nodes are defined here """

    def __init__(self):
        super(RootNode, self).__init__(
            "root",
            [],
            children=["metadata", "github", "platform", "output"],
            serializable=False,
        )


Node.register(RootNode())
