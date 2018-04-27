# coding:utf-8
import bisect, copy

__all__ = ['Node']

class Node(object):
    def __init__(self):
        self.children = []
        self.children_names = {}
        self._parent = None
        self.x = 0
        self.y = 0
        self.scale = 1.0
        self.rotation = 0.0

        self.visible = True

        self.is_running = False

    def _get_position(self):
        return (self.x, self.y)
    
    def _set_position(self, (x, y)):
        self.x, self.y = x, y
    
    position = property(_get_position, _set_position,
                        doc='''The (x, y) coordinates of the object.
                        :type: (int, int)
                        ''')
    def _get_parent(self):
        if self._parent is None: return None
        else: return self._parent()

    def _set_parent(self, parent):
        if parent is None: self._parent = None
        else: self._parent = weakref.ref(parent)

    parent = property(_get_parent, _set_parent, doc='''The parent of this object.
    :type: object
    ''')

    def add(self, child, z=0, name=None):
        """
        Add a child to the container

        :Parameters:
            `child`: object
                object to be added
            `z` : float
                the z index of self
            `name` : str
                Name of the child
        """

        if name:
            if name in self.children_names:
                raise Exception("Name already exists: {}".format(name))
            self.children_names[name] = child
        
        child.parent = self

        elem = z, child
        bisect.insort(self.children, elem)
        
        return self

    def remove(self, obj):
        if isinstance(obj, str):
            if obj in self.children_names:
                child = self.children_names[obj]
                self._remove(child)
            else:
                raise Exception("Child not found: {}".format(obj))
        else:
            self._remove(obj)

    def _remove( self, child ):
        l_old = len(self.children)
        self.children = [ (z,c) for (z,c) in self.children if c != child ]

        if l_old == len(self.children):
            raise Exception("Child not found: %s" % str(child) )

        if self.is_running:
            child.on_exit()

    def get_children(self):
        return [ c for (z, c) in self.child]

    def __contains__(self, child):
        return child in self.get_children()

    def get(self, name):
        if name in self.children_names:
            return self.children_names[name]
        else:
            raise Exception("Child not found: {}".format(name))

    def on_exit(self):
        self.is_running = False

        for c in self.get_children():
            c.on_exit()

    def on_enter(self):
        self.is_running = True

        for c in self.get_children():
            c.on_enter()

    def draw(self, *args, **kwargs):
        pass