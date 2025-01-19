import javalang

# Corrected Java code
java_code = """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""

# Parse Java code into tokens
try:
    tokens = list(javalang.tokenizer.tokenize(java_code))
    parser = javalang.parser.Parser(tokens)
    tree = parser.parse()

    # Traverse the AST
    def traverse_ast(node):
        if isinstance(node, javalang.ast.Node):
            print(f"Node: {node.__class__.__name__}")
            for _, child in node:
                traverse_ast(child)

    traverse_ast(tree)
except javalang.parser.JavaSyntaxError as e:
    print("JavaSyntaxError:", e)
