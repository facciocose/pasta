import gtk
import keybinder

class Clipboard(list):
    def move_to_last(self, item):
        tmp = self.pop(item)
        self.append(tmp)
        return tmp

    def append(self, item):
        if item in self:
            self.move_to_last(self.index(item))
        else:
            if len(self) > 5:
                del self[0]
            super(Clipboard, self).append(item)

class Pasta:
    def __init__(self):
        self.gtk_clip = gtk.Clipboard()
        self.pasta_clip = Clipboard()
        self.gtk_clip.connect("owner-change", self.change)

        self.model = gtk.ListStore(str)

        self.model.append(['Welcome to Pasta'])
        self.model.append(['Pasta is a clipboard-manager'])
        self.model.append(['and this is the content of my clipboard'])

        self.window = gtk.Window()
        self.window.set_decorated(False)
        self.window.set_keep_above(True)
        self.tree = gtk.TreeView(self.model)

        self.tree.connect("select-cursor-row", self.select)
        
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn()
        column.pack_start(cell)
        column.set_attributes(cell, text=0)
        column.set_title('Pasta')
        self.tree.append_column(column)
        
        self.window.add(self.tree)
        self.tree.show()
        self.window.connect('key-press-event', self.hide)

    def hide(self, widget, data=None):
        key = gtk.gdk.keyval_name(data.keyval)
        if key == 'Escape':
            self.window.hide()
    
    def change(self, widget, data=None):
        text = self.get_gtk_clip()
        if text:
            self.pasta_clip.append(text)
            self.model.clear()
            for i in reversed(self.pasta_clip):
                self.model.append([i])
            self.window.hide()
    
    def get_gtk_clip(self):
        return self.gtk_clip.wait_for_text()
    
    def set_gtk_clip(self, text):
        self.gtk_clip.set_text(text)
        self.gtk_clip.store()
    
    def select(self, widget, data=None):
        sel = self.tree.get_selection()
        model, iter = sel.get_selected()
        self.set_gtk_clip(model.get_value(iter, 0))

    def show(self):
        self.window.show()
        # doesn't work :(
        self.window.grab_focus()
    
    def main(self):
        gtk.main()

if __name__ == "__main__":
    pasta = Pasta()
    keybinder.bind("<Control><Alt>P", lambda: pasta.show())
    gtk.main()

