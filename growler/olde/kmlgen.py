#!/usr/bin/env python

# Modifications by Nick Aldwin <nick@aldwin.us>

# Copyright (c) 2011 Nine More Minutes, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of Nine More Minutes, Inc. nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys
import xml.dom.minidom

class Element(xml.dom.minidom.Element):

    def writexml(self, writer, indent="", addindent="", newl=""):
        # indent = current indentation
        # addindent = indentation to add to higher levels
        # newl = newline string
        writer.write(indent+"<" + self.tagName)

        attrs = self._get_attributes()
        a_names = attrs.keys()
        a_names.sort()

        for a_name in a_names:
            writer.write(" %s=\"" % a_name)
            xml.dom.minidom._write_data(writer, attrs[a_name].value)
            writer.write("\"")
        if self.childNodes:
            newl2 = newl
            if len(self.childNodes) == 1 and \
                self.childNodes[0].nodeType == xml.dom.minidom.Node.TEXT_NODE:
                indent, addindent, newl = "", "", ""
            writer.write(">%s"%(newl))
            for node in self.childNodes:
                node.writexml(writer,indent+addindent,addindent,newl)
            writer.write("%s</%s>%s" % (indent,self.tagName,newl2))
        else:
            writer.write("/>%s"%(newl))

# Monkey patch Element class to use our subclass instead.
xml.dom.minidom.Element = Element

class KML:
    """Creates KML"""

    def __init__(self, title, description=''):
        """Create the overall KML document."""
        self.kml_doc = xml.dom.minidom.Document()
        kml = self.kml_doc.createElement('kml')
        kml.setAttribute('xmlns', 'http://www.opengis.net/kml/2.2')
        self.kml_doc.appendChild(kml)
        document = self.kml_doc.createElement('Document')
        kml.appendChild(document)
        docName = self.kml_doc.createElement('name')
        document.appendChild(docName)
        docName_text = self.kml_doc.createTextNode(title)
        docName.appendChild(docName_text)
        docDesc = self.kml_doc.createElement('description')
        document.appendChild(docDesc)
        docDesc_text = self.kml_doc.createTextNode(description)
        docDesc.appendChild(docDesc_text)

    def append(self, xml):
        """Append the XML within the Document element"""
        doc = self.kml_doc.documentElement.getElementsByTagName('Document')[0]
        doc.appendChild(xml.documentElement)

    def add_style(self, style_id, icon_href):
        """Add a new style for different placemark icons."""
        doc = xml.dom.minidom.Document()
        style = doc.createElement('Style')
        style.setAttribute('id', style_id)
        doc.appendChild(style)
        icon_style = doc.createElement('IconStyle')
        style.appendChild(icon_style)
        icon = doc.createElement('Icon')
        icon_style.appendChild(icon)
        href = doc.createElement('href')
        icon.appendChild(href)
        href_text = doc.createTextNode(icon_href)
        href.appendChild(href_text)
        self.append(doc)

    def add_placemark(self, name, lon, lat, desc='', style='', altitude=0):
        """Add a new Placemark."""
        doc = xml.dom.minidom.Document()
        pm = doc.createElement("Placemark")
        doc.appendChild(pm)
        name_el = doc.createElement("name")
        pm.appendChild(name_el)
        name_text = doc.createTextNode(name)
        name_el.appendChild(name_text)
        desc_el = doc.createElement("description")
        pm.appendChild(desc_el)
        desc_text = doc.createTextNode(desc)
        desc_el.appendChild(desc_text)
        if style:
            style_url = doc.createElement("styleUrl")
            pm.appendChild(style_url)
            style_url_text = doc.createTextNode('#%s' % style)
            style_url.appendChild(style_url_text)
        pt = doc.createElement("Point")
        pm.appendChild(pt)
        coords = doc.createElement("coordinates")
        pt.appendChild(coords)
        coords_text = doc.createTextNode('%s,%s,%s' % (lon,lat,altitude))
        coords.appendChild(coords_text)
        self.append(doc)

    def output_kml(self):
        """Output as KML"""
        return self.kml_doc.toprettyxml(indent="  ", encoding='UTF-8')
