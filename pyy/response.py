__license__ = '''
This file is part of pyy.

pyy is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

pyy is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General
Public License along with pyy.  If not, see
<http://www.gnu.org/licenses/>.
'''

class response(object):
    def __init__(self, title='HTML Page'):
        self.title   = title
        
        self.request = None
        self.headers = {
            'Content-Type' : 'text/html',
            'Cache-Control': 'no-cache',
        }
        self.xml     = None
        self.doctype = None
        self.html    = None
    
    def __iadd__(self, obj):
        if self.html:
            body = self.html.getElementsByTagName('body')
            if body:
                body[0] += obj
                return
            else:
                raise ValueError('No body tag found.')
        else:
            raise ValueError('No html tag found.') #Likely not instantiated from a child class
    
    def set_cookie(self, cookie):
        self.cookies[cookie.name] = cookie
    
    def render_headers(self, as_list=False):
        list = self.headers.items()
        list += [('Set-Cookie', cookie.render()) for cookie in self.cookies.values()]
        return list if as_list else '\n'.join("%s: %s" % item for item in list)

    def render(self, just_html=False):
        r = []
        if not just_html:
            r.append(self.render_headers())
            r.append('\n'.join(cookie.render() for cookie in self.cookies.values()))
            r.append('\n\n')
        
        if self.xml:
            r.append(self.xml)
            r.append('\n')
        
        if self.doctype:
            r.append(self.doctype)
            r.append('\n')
        
        r.append(self.html)
        return ''.join(map(str, r))
    
    def __str__(self):
        return self.render()
