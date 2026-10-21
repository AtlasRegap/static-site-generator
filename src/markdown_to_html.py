from block_markdown import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    raise ValueError(f"Invalid block type: {block_type}")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    return ParentNode("p", text_to_children(paragraph))


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    text = block[4:-3]
    code_node = text_node_to_html_node(TextNode(text, TextType.CODE))
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.lstrip(">").strip())
    content = " ".join(cleaned_lines)
    return ParentNode("blockquote", text_to_children(content))


def unordered_list_to_html_node(block):
    items = []
    for line in block.split("\n"):
        text = line[2:]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)


def ordered_list_to_html_node(block):
    items = []
    for line in block.split("\n"):
        text = line.split(". ", 1)[1]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)
