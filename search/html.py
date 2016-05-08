# Create the html display of a given search
# Use the image as background and overlay the svg
# (remove all the paths in the svg that were not found and write the copy in a new file)
import os
from svg.path import parse_path
from xml.dom.minidom import Document, parse, parseString
from utils.fio import get_absolute_path, get_config
from utils.transcription import WordCoord

class HTMLVisualization:
    def __init__(self):
        self.__document = Document()
        self.html = self.__document.createElement('html')
        self.head = self.__document.createElement('head')
        self.body = self.__document.createElement('body')
        self.html.appendChild(self.head)
        self.html.appendChild(self.body)
        css = self.__document.createElement('style')
        text = self.__document.createTextNode('div { position: absolute; }')
        css.appendChild(text)
        self.head.appendChild(css)

    # TODO: Refactor!
    def add_image(self, img_src, svg_src=None, svg_str=None, img_id=None, paths=None, words=None):
        div = self.__document.createElement('div')
        if img_id:
            div.setAttribute('id', img_id)
        div.setAttribute('style', 'background-image: url("' + img_src + '");')
        if svg_src:
            svg_doc = parse(svg_src)
        elif svg_str:
            svg_doc = parseString(svg_str)
        if svg_doc:
            if words is not None:
                svg_doc = filter_svg_by_id(svg_doc, words)
                div.appendChild(svg_doc)
            elif paths is not None:
                svg_doc = filter_svg(svg_doc, paths)
                div.appendChild(svg_doc)
            else:
                div.appendChild(svg_doc.documentElement)
        self.body.appendChild(div)

    def add_image_by_id(self, img_id, word_ids=None):
        config = get_config()
        img_dir = get_absolute_path(config.get('KWS', 'images'))
        img_src = os.path.join(img_dir, img_id + '.jpg')
        svg_dir = get_absolute_path(config.get('KWS', 'locations'))
        svg_src = os.path.join(svg_dir, img_id + '.svg')
        self.add_image(img_src, svg_src=svg_src, words=word_ids)

    def save(self, file_path='output.html'):
        file_handle = open(file_path, 'w')
        self.html.writexml(file_handle)
        file_handle.close()

def filter_svg(svg_doc, paths):
    svg_root = svg_doc.getElementsByTagName('svg')[0]
    # copy only the root node
    new_svg = svg_root.cloneNode(False)
    for element in svg_doc.getElementsByTagName('path'):
        parsed_path = parse_path(element.getAttribute('d'))
        for path in paths:
            if path == parsed_path:
                new_svg.appendChild(element)
                break

    return new_svg

def filter_svg_by_id(svg_doc, word_ids):
    svg_root = svg_doc.getElementsByTagName('svg')[0]
    # copy only the root node
    new_svg = svg_root.cloneNode(False)
    for element in svg_doc.getElementsByTagName('path'):
        for word_id in word_ids:
            if element.getAttribute('id') == word_id:
                new_svg.appendChild(element)
                break

    return new_svg
