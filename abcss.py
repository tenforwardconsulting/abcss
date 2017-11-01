# Originally written by Mark Norman (mark@tenforwardconsulting.com)

import sublime, sublime_plugin
import string
import re

class AbcssCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    print('ABCSS Sorting...')

    view = self.view

    if self.handle_generic_sort(view):
      return

    if self.handle_selection_sort(view):
      return

    all_content = sublime.Region(0, view.size())

    AbcssCommand.all_lines = view.lines(all_content)
    AbcssCommand.line_number = 0

    AbcssCommand.sort_array = []
    AbcssCommand.insert_begin = 0
    AbcssCommand.insert_end = 0

    for line in AbcssCommand.all_lines:
      AbcssCommand.line_number += 1

      line_string = view.substr(line)

      leading_spaces = re.compile('^\s*').match(line_string).end()

      first_or_blank = (leading_spaces == 0 | len(line_string.strip()) == 0)
      first_word_match = re.compile('^\s*((\.)?[^\s\.\#\:\,\[]+)').match(line_string)

      if first_or_blank:
        first_word = ''
      elif first_word_match:
        first_word = first_word_match.group(1).strip()

      if (
          # EMPTY
          first_word == '' or
          # HTML TAG
          first_word in htmlArray or
          # CLASS/ID
          first_word.startswith('.') or
          first_word.startswith('#') or
          # PARENT REFERENCE
          first_word.startswith('&') or
          # PSEUDO CLASS
          first_word.startswith(':') or
          # WILDCARD
          first_word.startswith('*') or
          # VARIABLE
          first_word.startswith('$')
        ):
        self.replace_content(view, edit, line)

      else:
        if AbcssCommand.insert_begin == 0:
          AbcssCommand.insert_begin = line.begin()
        AbcssCommand.insert_end = line.end()

        AbcssCommand.sort_array.append(line_string)

        if line == AbcssCommand.all_lines[len(AbcssCommand.all_lines) - 1]:
          self.replace_content(view, edit, line)


  def handle_generic_sort(self, view):
    main_region = sublime.Region(0, view.size())
    if main_region.end() == 0:
      return False

    all_lines = view.lines(main_region)

    has_indent = False
    for line in all_lines:
      line_string = view.substr(line)

      leading_space_match = re.compile('^\s*').match(line_string)
      leading_spaces = leading_space_match.end()

      if leading_spaces != 0:
        has_indent = True
        break

    if has_indent:
      return False
    else:
      sublime.active_window().run_command('sort_lines', { 'case_sensitive': False })
      return True


  def handle_selection_sort(self, view):
    selection_count = 0
    for selection in view.sel():
      selection_count += len(selection)
    if selection_count > 0:
      sublime.active_window().run_command('sort_lines', { 'case_sensitive': False })
      return True

    return False

  def check_and_add_trailing_space(self, view, edit):
    all_lines = view.lines(sublime.Region(0, view.size()))
    last_line = all_lines[len(all_lines) - 1]
    last_line_string = view.substr(last_line).strip()

    if len(last_line_string) > 0:
      view.insert(edit, last_line.end(), '\n\n')


  def replace_content(self, view, edit, line):
    if AbcssCommand.sort_array:
      AbcssCommand.sort_array.sort(key=lambda x: x.replace('-', ''))

      replacement_range = sublime.Region(AbcssCommand.insert_begin, AbcssCommand.insert_end)
      replacement_string = '\n'.join(str(x) for x in AbcssCommand.sort_array)

      view.replace(edit, replacement_range, replacement_string)

      AbcssCommand.sort_array = []
      AbcssCommand.insert_begin = 0
      AbcssCommand.insert_end = 0


  def fake_clear_console(self):
    # space out console becuase there is no clear method
    print('\n' * 100)


  def set_default_content(self, edit):
    defaultContent = '''
body
  color: black
  z-index: 1
  background: white
  text-align: center

.class1
  margin: 10px
  padding: 10px
  float: left
  .sub-class1
    text-align: center
    font-size: 12px
    clear: both

.class2
  text-align: center
  background: #dddddd
  font-size: 12px
  font-family: Tahoma
  line-height: 1.4

#my_id
  text-decoration: none
  color: blue
  text-align: center
  .my-something
    .my-other-something
      display: none
  &:first-child
    color: green
  *
    padding: 0
    margin: 10px
'''.strip()

    self.view.insert(edit, 0, defaultContent)

htmlArray = [
  'a',
  'abbr',
  'acronym',
  'address',
  'applet',
  'area',
  'article',
  'aside',
  'audio',
  'b',
  'base',
  'basefont',
  'bdi',
  'bdo',
  'big',
  'blockquote',
  'body',
  'br',
  'button',
  'canvas',
  'caption',
  'center',
  'cite',
  'code',
  'col',
  'colgroup',
  'datalist',
  'dd',
  'del',
  'details',
  'dfn',
  'dialog',
  'dir',
  'div',
  'dl',
  'dt',
  'em',
  'embed',
  'fieldset',
  'figcaption',
  'figure',
  'font',
  'footer',
  'form',
  'frame',
  'frameset',
  'h1',
  'h2',
  'h3',
  'h4',
  'h5',
  'h6',
  'head',
  'header',
  'hr',
  'html',
  'i',
  'iframe',
  'img',
  'input',
  'ins',
  'kbd',
  'keygen',
  'label',
  'legend',
  'li',
  'link',
  'main',
  'map',
  'mark',
  'menu',
  'menuitem',
  'meta',
  'meter',
  'nav',
  'noframes',
  'noscript',
  'object',
  'ol',
  'optgroup',
  'option',
  'output',
  'p',
  'param',
  'pre',
  'progress',
  'q',
  'rp',
  'rt',
  'ruby',
  's',
  'samp',
  'script',
  'section',
  'select',
  'small',
  'source',
  'span',
  'strike',
  'strong',
  'style',
  'sub',
  'summary',
  'sup',
  'svg',
  'table',
  'tbody',
  'td',
  'textarea',
  'tfoot',
  'th',
  'thead',
  'time',
  'title',
  'tr',
  'track',
  'tt',
  'u',
  'ul',
  'var',
  'video',
  'wbr'
]
