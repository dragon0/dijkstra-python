#!/usr/bin/python3

import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk

def dijkstra(graph, source, dest):
    # dist[v] is distance from source to v
    dist = {vertex: float('inf') for vertex in graph.keys()}
    # prev[v] is the node from which v was reached;
    # eg. if prev['coors'] is 'dodgers' and prev['dodgers'] is 'petco'
    #     then the path was petco -> dodgers -> coors
    prev = {vertex: None for vertex in graph.keys()}

    # the distance from source to source is 0
    # (any non-inf means the vertex has been visited)
    dist[source] = 0
    # copy the vertex list
    q = list(graph.keys())

    # loop until q is empty
    while q:
        # get the vertex that is closest to start;
        # that is, the vertex u with the smallest dist[u]
        u = min(q, key=lambda vertex: dist[vertex])
        # we're visiting it, so remove it from the queue
        q.remove(u)

        # if u == dest then we have found the path from source to dest;
        # if dist[u] == float('inf') then there is no path from source to u;
        # since we're always taking the smallest dist[u], if we see an inf
        # then the rest of the graph is not connected to source
        if dist[u] == float('inf') or u == dest:
            break

        # loop over all neighbors v of u
        for v, cost in graph[u]:
            # get the current dist from source to u and add dist from u to v
            alt = dist[u] + cost
            # if this is smaller than the current distance from source to v
            # then the path from source to v via u is shorter than any existing
            # path from source to v
            if alt < dist[v]:
                # store the new smaller distance
                dist[v] = alt
                # we now travel from source to v via u
                prev[v] = u

    # now build the path from source to dest;
    # note that we could also just return prev; doing so would allow us to
    # build a spanning tree rooted at source (we would remove the dest
    # parameter in this case)
    s = []
    u = dest
    # prev[source] is None (and should be the only None reachable from dest)
    while prev[u]:
        s.append(u)
        u = prev[u]
    s.append(u)
    s.reverse()
    return s

class DijkstraViewer(tk.Frame):
    def __init__(self, master, graph):
        tk.Frame.__init__(self, master)
        self.pack(expand="yes", fill="both")
        self.graph = graph
        cb_contents = sorted(['"{}"'.format(k) for k in graph.keys()])
        self.createWidgets(cb_contents)

    def createWidgets(self, cb_contents):
        self.listbox = tk.Listbox(self)

        cb_contents_str = ' '.join(cb_contents)
        self.combo_source = ttk.Combobox(self, values=cb_contents_str)
        self.combo_dest = ttk.Combobox(self, values=cb_contents_str)

        init = next(iter(sorted(self.graph.keys())))
        self.combo_source.set(init)
        self.combo_dest.set(init)

        self.combo_source.config(state="readonly")
        self.combo_dest.config(state="readonly")

        self.listbox.pack(side='top', expand='yes', fill='both')
        self.combo_source.pack(side="top", expand='yes', fill='x')
        self.combo_dest.pack(side="top", expand='yes', fill='x')

        self.combo_source.bind('<<ComboboxSelected>>', self.reset)
        self.combo_dest.bind('<<ComboboxSelected>>', self.reset)

    def reset(self, event):
        self.listbox.delete(0, 'end')
        source = self.combo_source.get()
        dest = self.combo_dest.get()
        path = dijkstra(self.graph, source, dest)
        for item in path:
            self.listbox.insert('end', item)
        #lb = tk.Listbox()
        #lb.insert('end', 'hello')
        #lb.insert(0, 'world')
        #lb.delete(0)
        #lb.delete(0, 'end')


class Application(tk.Frame):
    def __init__(self, master=None):
        # 800 x 400
        tk.Frame.__init__(self, master)
        self.pack(expand="yes", fill="both")
        self.createWidgets()
        self.buildTree()
        window = tk.Toplevel()
        window.title('Traversal Path')
        window.minsize(width=300, height=300)
        dkView = DijkstraViewer(window, self.graph)

    def createWidgets(self):
        self.treeview = ttk.Treeview(self)
        #self.treeview.grid(row=0, column=0, sticky="NESW")
        self.treeview.pack(side="top", fill='both', expand='yes')
        # insert top-level item
        # iid = self.treeview.insert('', 'end', text='top-level')
        # insert child of iid
        # iid2 = self.treeview.insert(iid, 'end', text='child')

        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                                            command=root.destroy)
        #self.QUIT.grid(row=1, column=0)
        self.QUIT.pack(side="bottom")

    def buildTree(self):
        tree = ET.parse('info.xml')
        root = tree.getroot()
        self.graph = graph = {}

        american_league = root.find('.//american-league')
        amid = self.treeview.insert('', 'end', text='American League')
        for child in american_league.iterfind('stadium'):
            stadname = child.attrib.get('stadium_name')
            graph[stadname] = []
            stadid = self.treeview.insert(amid, 'end', 
                    text=stadname)
            for conn in child.iterfind('connection'):
                connto = conn.attrib.get('to')
                conndist = int(conn.attrib.get('distance'))
                graph[stadname].append((connto, conndist))
                self.treeview.insert(stadid, 'end', text=connto)

        national_league = root.find('.//national-league')
        natid = self.treeview.insert('', 'end', text='National League')
        for child in national_league.iterfind('stadium'):
            stadname = child.attrib.get('stadium_name')
            graph[stadname] = []
            stadid = self.treeview.insert(natid, 'end', 
                    text=stadname)
            for conn in child.iterfind('connection'):
                connto = conn.attrib.get('to')
                conndist = int(conn.attrib.get('distance'))
                graph[stadname].append((connto, conndist))
                self.treeview.insert(stadid, 'end', text=connto)

root = tk.Tk()
root.title('Graph')
root.minsize(width=300, height=700)
app = Application(master=root)
app.mainloop()

#tv = ttk.Treeview()
#tv.pack()
#ids = []
#ids.append(tv.insert('', 'end', text='1'))
#ids.append(tv.insert('', 'end', text='2'))
#ids.append(tv.insert('', 'end', text='3'))
#tv.delete(*ids)

