import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import messagebox
from Representations.Circle import Circle
from Representations.Line import Line
from Representations.LineSegment import LineSegment
from Representations.Point import Point
from Representations.Polygon import Polygon
import Problems.ClassicalProblems as classics
from Problems.Complex_Problems.Voronoi import Voronoi
from Problems.Complex_Problems.Closest_Pair_Points import ClosestPair
from Problems.Complex_Problems.Smallest_Circle import make_circle
import copy


class Box:
    def __init__(self, root, msg, values):
        self.value = None

        self.root = root
        self.top = tk.Toplevel(self.root)

        self.frm = tk.Frame(self.top)
        self.frm.pack(fill='both', expand=True)

        self.label = tk.Label(self.frm, text=msg)
        self.label.pack()

        self.country_var = tk.StringVar()
        self.combobox = Combobox(self.frm, textvariable=self.country_var)
        self.combobox['values'] = values
        self.combobox.pack(pady=25)

        self.frmButton = tk.Frame(self.top)
        self.frmButton.pack(side=tk.BOTTOM)

        self.btnOk = tk.Button(self.frmButton, text="Selecionar", command=lambda: self.onClickOk())
        self.btnOk.pack(side=tk.LEFT, padx=25)

        self.btnCancel = tk.Button(self.frmButton, text="Cancelar", command=lambda: self.top.destroy())
        self.btnCancel.pack(side=tk.LEFT, padx=25)

    def onClickOk(self):
        data = self.combobox.get()
        if data:
            self.value = data
            self.top.destroy()


class MainWindow:
    RADIUS = 2
    LOCK = True

    def __init__(self, master):
        self.master = master
        self.master.title("Trabalho PAA")

        self.master.bind('<Return>', self.onPressReturn)

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.classicsMenu = tk.Menu(self.menu)
        self.complexMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Problemas Clássicos", menu=self.classicsMenu)
        self.menu.add_cascade(label="Problemas Complexos", menu=self.complexMenu)
        self.classicsMenu.add_command(label="Distância entre dois pontos", command=self.calcular_distancia_dois_pontos)
        self.classicsMenu.add_command(label="Distância entre um ponto e uma reta",
                                      command=self.calcular_distancia_reta_ponto)
        self.classicsMenu.add_command(label="Área de um polígono", command=self.calcular_area_do_polygon)
        self.classicsMenu.add_command(label="Área de um círculo", command=self.calcular_area_do_circulo)
        self.classicsMenu.add_command(label="Convexidade de um polígono", command=self.calcular_convexidade)
        self.classicsMenu.add_command(label="Dobrar em Triangulos", command=self.calcular_tringulacao)
        self.classicsMenu.add_command(label="Orientação 2D", command=self.calcular_orientacao)
        self.classicsMenu.add_command(label="Lado do círculo", command=self.calcular_lado_circulo)
        self.classicsMenu.add_command(label="Interseção de Segmentos", command=self.calcular_intersecao_segmentos)
        self.classicsMenu.add_command(label="Ponto mais próximo do segmento",
                                      command=self.calcular_ponto_mais_proximo_segmento)
        self.classicsMenu.add_command(label="Ponto dentro do polígono", command=self.ponto_dentro_poligono)

        self.complexMenu.add_command(label="Par mais próximo", command=self.calcular_ponto_mais_proximo)
        self.complexMenu.add_command(label="Circulo Mínimo", command=self.calcular_circulo_minino)
        self.complexMenu.add_command(label="Voronoi", command=self.calcular_voronoi)

        self.frmMain = tk.Frame(self.master)
        self.frmMain.pack(side=tk.LEFT)

        self.w = tk.Canvas(self.frmMain, width=500, height=500)
        self.w.config(background='white')
        self.w.bind('<Button-1>', self.onClick)
        self.w.pack(side=tk.RIGHT)

        self.frmButtons = tk.Frame(self.master)
        self.frmButtons.pack(side=tk.RIGHT)

        self.btnCirculo = tk.Button(self.frmButtons, text="Criar Círculo", width=15, command=self.onClickCriarCirculo)
        self.btnCirculo.pack(side=tk.TOP)

        self.btnLinha = tk.Button(self.frmButtons, text="Criar Linha", width=15, command=self.onClickCriarLinha)
        self.btnLinha.pack(side=tk.TOP)

        self.btnSegmento = tk.Button(self.frmButtons, text="Criar Segmento", width=15, command=self.onCickCriarSegmento)
        self.btnSegmento.pack(side=tk.TOP)

        self.btnPonto = tk.Button(self.frmButtons, text="Criar Ponto", width=15, command=self.onClickCriarPonto)
        self.btnPonto.pack(side=tk.TOP)

        self.btnPolygon = tk.Button(self.frmButtons, text="Criar Polígono", width=15,
                                    command=self.onClickCriarPoligono)
        self.btnPolygon.pack(side=tk.TOP)

        self.btnClear = tk.Button(self.frmButtons, text='Clear', width=15, command=self.onClickClear)
        self.btnClear.pack(side=tk.BOTTOM, pady=50)

        self.circles = []
        self.lines = []
        self.segments = []
        self.points = []
        self.polygons = []

        self.pts = []

    def onClickClear(self):
        self.LOCK = True
        self.w.delete(tk.ALL)
        self.circles.clear()
        self.lines.clear()
        self.segments.clear()
        self.points.clear()
        self.polygons.clear()
        self.liberaTodosBotoes()
        self.pts.clear()

    def onClick(self, event):
        if not self.LOCK:
            self.w.create_oval(event.x-self.RADIUS, event.y-self.RADIUS, event.x+self.RADIUS,
                               event.y+self.RADIUS, fill="black")
            self.pts.append((event.x, event.y))

            if self.btnCirculo['state'] == tk.NORMAL:
                if len(self.pts) == 2:
                    p1 = Point(self.pts[0][0], self.pts[0][1])
                    p2 = Point(self.pts[1][0], self.pts[1][1])

                    distance = classics.distance_between_two_points(p1, p2)
                    circle = Circle(p1, int(distance))
                    self.circles.append(circle)

                    self.draw_circle(p1.get_x(), p1.get_y(), circle.get_radius())
                    nome = "Circ"+str(len(self.circles))
                    self.w.create_text(p1.get_x(), p1.get_y()+circle.get_radius()+7, text=nome)

                    self.liberaTodosBotoes()
                    self.LOCK = True
                    self.pts.clear()
            elif self.btnLinha['state'] == tk.NORMAL:
                if len(self.pts) == 2:
                    p1 = Point(self.pts[0][0], self.pts[0][1])
                    p2 = Point(self.pts[1][0], self.pts[1][1])

                    line = Line.generate_by_two_points(p1, p2)
                    self.lines.append(line)

                    p1_x_canvas = line.get_x_from_y(0)
                    p2_x_canvas = line.get_x_from_y(500)

                    self.w.create_line(int(p1_x_canvas), 0, int(p2_x_canvas), 500, fill="RoyalBlue2")
                    nome = "Lin" + str(len(self.lines))
                    self.w.create_text((p1_x_canvas + p2_x_canvas) / 2, (0 + 500) / 2, text=nome)

                    self.liberaTodosBotoes()
                    self.LOCK = True
                    self.pts.clear()
            elif self.btnSegmento['state'] == tk.NORMAL:
                if len(self.pts) == 2:
                    p1 = Point(self.pts[0][0], self.pts[0][1])
                    p2 = Point(self.pts[1][0], self.pts[1][1])

                    seg = LineSegment(p1, p2)
                    self.segments.append(seg)

                    self.w.create_line(p1.get_x(), p1.get_y(), p2.get_x(), p2.get_y(), fill='red')
                    nome = "Seg"+str(len(self.segments))
                    self.w.create_text((p1.get_x()+p2.get_x())/2, (p1.get_y()+p2.get_y())/2, text=nome)

                    self.liberaTodosBotoes()
                    self.LOCK = True
                    self.pts.clear()
            elif self.btnPonto['state'] == tk.NORMAL:
                p = Point(self.pts[0][0], self.pts[0][1])
                self.points.append(p)

                nome = "Ptn"+str(len(self.points))
                self.w.create_text(p.get_x(), p.get_y()+10, text=nome)
                self.pts.clear()
            elif self.btnPolygon['state'] == tk.NORMAL:
                if len(self.pts) == 2:
                    p1 = Point(self.pts[0][0], self.pts[0][1])
                    p2 = Point(self.pts[1][0], self.pts[1][1])

                    seg = LineSegment(p1, p2)
                    self.polygons[len(self.polygons)-1].add_segment(seg)

                    self.w.create_line(p1.get_x(), p1.get_y(), p2.get_x(), p2.get_y(), fill='blue')

                    del self.pts[0]

    def onClickCriarCirculo(self):
        self.LOCK = False
        self.blockButtons(self.btnCirculo)

    def onClickCriarLinha(self):
        self.LOCK = False
        self.blockButtons(self.btnLinha)

    def onCickCriarSegmento(self):
        self.LOCK = False
        self.blockButtons(self.btnSegmento)

    def onClickCriarPonto(self):
        self.LOCK = False
        self.blockButtons(self.btnPonto)

    def onClickCriarPoligono(self):
        self.LOCK = False
        self.blockButtons(self.btnPolygon)
        self.polygons.append(Polygon())

    def calcular(self):
        pass

    def onPressReturn(self, event):
        if not self.LOCK:
            if self.btnPonto['state'] == tk.NORMAL:
                self.LOCK = True
                self.liberaTodosBotoes()
            elif self.btnPolygon['state'] == tk.NORMAL:
                if len(self.polygons[len(self.polygons)-1].get_list_points()) >= 3:
                    p_i = self.polygons[len(self.polygons)-1].get_list_points()[0]
                    p_f = self.polygons[len(self.polygons)-1].get_list_points()[len(self.polygons[len(self.polygons)-1].get_list_points())-1]

                    seg = LineSegment(p_i, p_f)
                    self.polygons[len(self.polygons) - 1].add_segment(seg)

                    self.w.create_line(p_i.get_x(), p_i.get_y(), p_f.get_x(), p_f.get_y(), fill='blue')
                    nome = "Poly"+str(len(self.polygons))
                    self.w.create_text(p_i.get_x(), p_i.get_y()+15, text=nome)

                    self.LOCK = True
                    self.liberaTodosBotoes()
                    self.pts.clear()

    def onPressEscape(self, event):
        pass

    def blockButtons(self, button: tk.Button):
        self.btnCirculo.configure(state=tk.DISABLED)
        self.btnLinha.configure(state=tk.DISABLED)
        self.btnSegmento.configure(state=tk.DISABLED)
        self.btnPonto.configure(state=tk.DISABLED)
        self.btnPolygon.configure(state=tk.DISABLED)
        button.configure(state=tk.NORMAL)

    def liberaTodosBotoes(self):
        self.btnCirculo.configure(state=tk.NORMAL)
        self.btnLinha.configure(state=tk.NORMAL)
        self.btnSegmento.configure(state=tk.NORMAL)
        self.btnPonto.configure(state=tk.NORMAL)
        self.btnPolygon.configure(state=tk.NORMAL)

    def draw_circle(self, x, y, r, **kwargs):
        self.w.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def calcular_ponto_mais_proximo(self):
        if len(self.points) >= 2:
            closest_point = ClosestPair(self.points)

            res = closest_point.get_closest_points()
            self.w.create_line(res[1].get_x(), res[1].get_y(), res[2].get_x(), res[2].get_y(), fill='green', width=3)

    def calcular_voronoi(self):
        if len(self.points) > 0:
            voronoi = Voronoi(self.points)
            voronoi.process()
            lines = voronoi.get_output()

            for i in lines:
                p0 = i.get_a()
                p1 = i.get_b()
                self.w.create_line(p0.get_x(), p0.get_y(), p1.get_x(), p1.get_y(), fill='green2')

    def calcular_circulo_minino(self):
        if len(self.points) > 0:
            circle = make_circle(self.points)
            self.draw_circle(circle.get_centre().get_x(), circle.get_centre().get_y(), circle.get_radius())

    def calcular_tringulacao(self):
        strings = []
        for i in range(len(self.polygons)):
            strings.append("Poly"+str(i+1))

        box = Box(self.master, "Selecione o polígono para realizar triangulação", strings)

        self.master.wait_window(box.top)

        str_escolhido = box.value
        if str_escolhido is not None:
            escolhido = int(str_escolhido.split("Poly")[1])-1

            polygon = copy.deepcopy(self.polygons[escolhido])

            ears = classics.EarClipping.ears_finding(polygon.get_list())
            edges = classics.EarClipping.ears_clipping(polygon.get_list(), ears)

            if len(edges) > 0:
                for edge in edges:
                    self.w.create_line(edge.get_a().get_x(), edge.get_a().get_y(), edge.get_b().get_x(), edge.get_b().get_y())
            else:
                tk.messagebox.showinfo("Dobra", "Não é possivel realizar dobras sobre este poligono")


    def calcular_distancia_dois_pontos(self):
        strings = []
        for i in range(len(self.points)):
            strings.append("Ptn"+str(i+1))

        box = Box(self.master, "Selecione o primeiro ponto", strings)
        self.master.wait_window(box.top)

        str_escolhido = box.value
        if str_escolhido is not None:
            escolhido1 = int(str_escolhido.split("Ptn")[1]) - 1

            box = Box(self.master, "Selecione o segundo ponto", strings)
            self.master.wait_window(box.top)

            str_escolhido = box.value
            if str_escolhido is not None:
                escolhido2 = int(str_escolhido.split("Ptn")[1]) - 1

                distancia = classics.distance_between_two_points(self.points[escolhido1], self.points[escolhido2])
                self.w.create_line(self.points[escolhido1].get_x(), self.points[escolhido1].get_y(),
                                   self.points[escolhido2].get_x(), self.points[escolhido2].get_y())

                text = "Distance="+str(format(distancia, '.2f'))

                self.w.create_text((self.points[escolhido1].get_x()+self.points[escolhido2].get_x())/2,
                                   (self.points[escolhido1].get_y()+self.points[escolhido2].get_y())/2, text=text)

    def ponto_dentro_poligono(self):
        strings = []
        for i in range(len(self.polygons)):
            strings.append("Poly" + str(i + 1))

        box = Box(self.master, "Selecione o polígono para realizar triangulação", strings)
        self.master.wait_window(box.top)

        str_escolhido = box.value
        if str_escolhido is not None:
            poly_escolhido = int(str_escolhido.split("Poly")[1]) - 1

            strings = []
            for i in range(len(self.points)):
                strings.append("Ptn" + str(i + 1))

            box = Box(self.master, "Selecione o primeiro ponto", strings)
            self.master.wait_window(box.top)

            str_escolhido = box.value
            if str_escolhido is not None:
                pto_escolhido = int(str_escolhido.split("Ptn")[1]) - 1

                res = classics.point_in_polygon(self.points[pto_escolhido], self.polygons[poly_escolhido])

                if res:
                    tk.messagebox.showinfo("Ponto dentro do polígono", "O ponto está dentro do polígono")
                else:
                    tk.messagebox.showinfo("Ponto dentro do polígono", "O ponto não está dentro do polígono")

    def calcular_area_do_circulo(self):
        strings = []
        for i in range(len(self.circles)):
            strings.append("Circ" + str(i + 1))

        box = Box(self.master, "Selecione o círculo", strings)
        self.master.wait_window(box.top)

        if box.value is not None:
            circ_escolhido = self.circles[int(box.value.split("Circ")[1])-1]

            area = classics.area_of_a_circle(circ_escolhido)
            text = "Area=" + str(format(area, '.2f'))

            self.draw_circle(circ_escolhido.get_centre().get_x(), circ_escolhido.get_centre().get_y(),
                             circ_escolhido.get_radius(), fill='grey')
            self.w.create_text(circ_escolhido.get_centre().get_x(),
                               circ_escolhido.get_centre().get_y()-circ_escolhido.get_radius()-10, text=text)

    def calcular_area_do_polygon(self):
        strings = []
        for i in range(len(self.polygons)):
            strings.append("Poly" + str(i + 1))

        box = Box(self.master, "Selecione o polígono", strings)
        self.master.wait_window(box.top)

        if box.value is not None:
            poly_escolhido = self.polygons[int(box.value.split("Poly")[1]) - 1]

            area = classics.polygon_area(poly_escolhido)
            text = "Area=" + str(format(area, '.2f'))

            pts = []
            for i in poly_escolhido.get_list_points():
                pts.append((i.get_x(), i.get_y()))

            self.w.create_polygon(pts, fill='grey')
            self.w.create_text(pts[0][0], pts[0][1]-30, text=text)

    def calcular_intersecao_segmentos(self):
        strings = []
        for i in range(len(self.segments)):
            strings.append("Seg" + str(i + 1))

        box = Box(self.master, "Selecione o primeiro segmento", strings)
        self.master.wait_window(box.top)

        str_escolhido = box.value
        if str_escolhido is not None:
            seg1_escolhido = int(str_escolhido.split("Seg")[1]) - 1

            strings = []
            for i in range(len(self.segments)):
                strings.append("Seg" + str(i + 1))

            box = Box(self.master, "Selecione o segundo segmento", strings)
            self.master.wait_window(box.top)

            str_escolhido = box.value
            if str_escolhido is not None:
                seg2_escolhido = int(str_escolhido.split("Seg")[1]) - 1

                res = classics.intersection_two_lines_segments(self.segments[seg1_escolhido],
                                                               self.segments[seg2_escolhido])

                if res:
                    tk.messagebox.showinfo("Interseção de segmentos", "Possui uma interseção entre os dois segmentos")
                else:
                    tk.messagebox.showinfo("Interseção de segmentos", "Não possui uma interseção entre os dois segmentos")

    def calcular_lado_circulo(self):
        strings = []
        for i in range(len(self.circles)):
            strings.append("Circ" + str(i + 1))

        box = Box(self.master, "Selecione o círculo", strings)
        self.master.wait_window(box.top)

        str_escolhido = box.value
        if str_escolhido is not None:
            circ_escolhido = int(str_escolhido.split("Circ")[1]) - 1

            strings = []
            for i in range(len(self.points)):
                strings.append("Ptn" + str(i + 1))

            box = Box(self.master, "Selecione o ponto", strings)
            self.master.wait_window(box.top)

            str_escolhido = box.value
            if str_escolhido is not None:
                ptn_escolhido = int(str_escolhido.split("Ptn")[1]) - 1

                res = classics.side_of_circle(self.circles[circ_escolhido], self.points[ptn_escolhido])

                if res == 1:
                    tk.messagebox.showinfo("Lado do círculo", "O ponto está dentro do círculo")
                elif res == 0:
                    tk.messagebox.showinfo("Lado do círculo", "O ponto está no raio do círculo")
                else:
                    tk.messagebox.showinfo("Lado do círculo", "O ponto está fora do círculo")

    def calcular_orientacao(self):
        strings = []
        for i in range(len(self.points)):
            strings.append("Ptn" + str(i + 1))

        box = Box(self.master, "Selecione o primeiro ponto", strings)
        self.master.wait_window(box.top)

        str_escolhido = box.value
        if str_escolhido is not None:
            ptn1 = int(str_escolhido.split("Ptn")[1]) - 1

            box = Box(self.master, "Selecione o segundo ponto", strings)
            self.master.wait_window(box.top)

            str_escolhido = box.value
            if str_escolhido is not None:
                ptn2 = int(str_escolhido.split("Ptn")[1]) - 1

                box = Box(self.master, "Selecione o terceiro ponto", strings)
                self.master.wait_window(box.top)

                str_escolhido = box.value

                if str_escolhido is not None:
                    ptn3 = int(str_escolhido.split("Ptn")[1]) - 1

                    res = classics.orient_2d(self.points[ptn1], self.points[ptn2], self.points[ptn3])

                    if res == -1:
                        tk.messagebox.showinfo("Orientação", "Os pontos estão em sentido horário")
                    elif res == 0:
                        tk.messagebox.showinfo("Orientação", "Os pontos são colineares")
                    else:
                        tk.messagebox.showinfo("Orientação", "Os pontos estão em sentido anti-horário")

    def calcular_convexidade(self):
        strings = []
        for i in range(len(self.polygons)):
            strings.append("Poly" + str(i + 1))

        box = Box(self.master, "Selecione o polígono", strings)
        self.master.wait_window(box.top)

        if box.value is not None:
            poly_escolhido = copy.deepcopy(self.polygons[int(box.value.split("Poly")[1]) - 1])

            value = classics.convex_polygon(poly_escolhido)

            if value:
                tk.messagebox.showinfo("Convexidade", "O polígono é convexo")
            else:
                tk.messagebox.showinfo("Convexidade", "O polígono é côncavo")

    def calcular_distancia_reta_ponto(self):
        strings = []
        for i in range(len(self.lines)):
            strings.append("Lin"+str(i+1))

        box = Box(self.master, "Selecione a linha", strings)
        self.master.wait_window(box.top)

        if box.value is not None:
            line_escolhido = self.lines[int(box.value.split("Lin")[1]) -1]

            strings = []
            for i in range(len(self.points)):
                strings.append("Ptn"+str(i+1))

            box = Box(self.master, "Selecione o ponto", strings)
            self.master.wait_window(box.top)

            if box.value is not None:
                ptn_escolhido = self.points[int(box.value.split("Ptn")[1]) -1]

                value = classics.distance_between_one_line_and_one_point(ptn_escolhido, line_escolhido)

                tk.messagebox.showinfo("Distância entre um ponto e reta", "A distância é "+str(value))

    def calcular_ponto_mais_proximo_segmento(self):
        strings = []
        for i in range(len(self.segments)):
            strings.append("Seg"+str(i+1))

        box = Box(self.master, "Selecione o segmento de reta", strings)
        self.master.wait_window(box.top)

        if box.value is not None and len(self.points) > 0:
            seg_escolhido = self.segments[int(box.value.split("Seg")[1]) - 1]

            value = classics.closest_point(seg_escolhido, self.points)

            self.w.create_oval(value.get_x()-self.RADIUS-1, value.get_y()-self.RADIUS-1, value.get_x()+self.RADIUS+1,
                               value.get_y()+self.RADIUS+1, fill="red")


if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
