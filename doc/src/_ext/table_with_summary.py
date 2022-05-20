#------------------------------------------------------------------------------
# Copyright (c) 2022, Oracle and/or its affiliates.
#
# This software is dual-licensed to you under the Universal Permissive License
# (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl and Apache License
# 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose
# either license.
#
# If you elect to accept the software under the Apache License, Version 2.0,
# the following applies:
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# table_with_summary.py
#
# Defines a directive (list-table-with-summary) that adds support for a summary
# option on top of the regular "list-table" directive.
#------------------------------------------------------------------------------

import sphinx.writers.html5
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives import tables

class ListTableWithSummary(tables.ListTable):

    option_spec = {'summary': directives.unchanged}
    option_spec.update(tables.ListTable.option_spec)

    def run(self):
        result = super().run()
        summary = self.options.get('summary')
        if summary:
            table_node = result[0]
            table_node["summary"] = summary
        return result


class HTMLTranslator(sphinx.writers.html5.HTML5Translator):

    def visit_table(self, node):
        self._table_row_index = 0

        atts = {}
        classes = [cls.strip(' \t\n') \
                for cls in self.settings.table_style.split(',')]
        classes.insert(0, "docutils")  # compat

        # set align-default if align not specified to give a default style
        classes.append('align-%s' % node.get('align', 'default'))

        if 'width' in node:
            atts['style'] = 'width: %s' % node['width']
        if 'summary' in node:
            atts['summary'] = node['summary']
        tag = self.starttag(node, 'table', CLASS=' '.join(classes), **atts)
        self.body.append(tag)


def setup(app):
    app.add_directive('list-table-with-summary', ListTableWithSummary)
    app.set_translator("html", HTMLTranslator, override=True)
