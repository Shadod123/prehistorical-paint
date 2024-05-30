import math
import tkinter as tk
from tkinter import filedialog, ttk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Transformações Geométricas, Rasterização e Recorte")
        
        # Cria um canvas para desenhar os objetos
        self.canvas = tk.Canvas(self, width=1280, height=720, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
                
        # Liga os eventos de clique e movimento do mouse
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.update_cursor_position)
        
        # Inicializa variáveis de controle
        self.start_point = None
        self.end_point = None
        self.dots_coords_list = []
        self.drawn_objects_coords = []
        self.updated_drawn_objects_coords = []
        self.polygon = None
        self.letter = 'A'
        self.selection_mode = False
        self.selection_area = None
        self.u1 = 0.0
        self.u2 = 1.0
        self.inside = False
        
        # Cria uma label para mostrar a posição do cursor
        self.cursor_position_label = tk.Label(self, text="x: 0, y: 0")
        self.cursor_position_label.place(x=0, y=0)
        
        # Cria frames para organizar os botões
        self.first_button_row_frame = tk.Frame(self)
        self.first_button_row_frame.pack(side=tk.TOP, pady=10)       
        self.second_button_row_frame = tk.Frame(self)
        self.second_button_row_frame.pack(side=tk.TOP, pady=10)
        self.third_button_row_frame = tk.Frame(self)
        self.third_button_row_frame.pack(side=tk.TOP, pady=10)
        
        self.clear_canvas_button = tk.Button(
            self.first_button_row_frame, text="Limpar Tela", font=("TkDefaultFont", 15),
            command=self.clear_canvas
        )
        self.clear_canvas_button.pack(side="left", padx=10)
        
        
        # Seleção de modo de desenho ou de seleção de região
        self.mode_selection_label = tk.Label(
            self.first_button_row_frame, text="Modos: ", font=("TkDefaultFont", 15, "bold"),
        )
        self.mode_selection_label.pack(side="left", padx=(10,0))
        
        self.draw_mode_button = tk.Button(
            self.first_button_row_frame, text="Desenhar", font=("TkDefaultFont", 15),
            command=self.draw_mode_enabler, relief="sunken"
        )
        self.draw_mode_button.pack(side="left", padx=3)
        
        self.selection_mode_button = tk.Button(
            self.first_button_row_frame, text="Selecionar Região", font=("TkDefaultFont", 15),
            command=self.selection_mode_enabler
        )
        self.selection_mode_button.pack(side="left", padx=(3,18))
        
        
        # Botões para desenhar diferentes objetos
        self.dda_line_button = tk.Button(
            self.first_button_row_frame, text="Linha (DDA)",  font=("TkDefaultFont", 15),
            command=self.draw_line_dda_caller
        )
        self.dda_line_button.pack(side="left", padx=10)
        
        self.bresenham_line_button = tk.Button(
            self.first_button_row_frame, text="Linha (Bresenham)",  font=("TkDefaultFont", 15),
            command=self.draw_line_bresenham_caller
        )
        self.bresenham_line_button.pack(side="left", padx=10)
        
        self.bresenham_circle_button = tk.Button(
            self.first_button_row_frame, text="Circunferência (Bresenham)",  font=("TkDefaultFont", 15),
            command=self.draw_circle_bresenham_caller
        )
        self.bresenham_circle_button.pack(side="left", padx=10)
        
        self.connect_all_alphabet_order_button = tk.Button(
            self.first_button_row_frame, text="Conectar Todos os Objetos",  font=("TkDefaultFont", 15),
            command=self.connect_all_alphabet_order
        )
        self.connect_all_alphabet_order_button.pack(side="left", padx=10)
        
        self.cohen_sutherland_snip_button = tk.Button(
            self.first_button_row_frame, text="Recorte (Cohen-Sutherland)",  font=("TkDefaultFont", 15),
            command=self.region_snip_cohen_sutherland_caller
        )
        self.cohen_sutherland_snip_button.pack(side="left", padx=10)
        
        self.liang_barsky_snip_button = tk.Button(
            self.first_button_row_frame, text="Recorte (Liang-Barsky)",  font=("TkDefaultFont", 15),
            command=self.region_snip_liang_barsky_caller
        )
        self.liang_barsky_snip_button.pack(side="left", padx=10)
        
        
        # Botões para operações de transformação com retas
        self.lines_transformations_label = tk.Label(
            self.second_button_row_frame, text="Retas", font=("TkDefaultFont", 15, "bold"),
        )
        self.lines_transformations_label.pack(side="left", padx=(37, 15))
        
        self.translation_tx_field_label = tk.Label(
            self.second_button_row_frame, text="Tx: ", font=("TkDefaultFont", 15),
        )
        self.translation_tx_field_label.pack(side="left", padx=(10, 0))
        
        self.translation_tx_field = tk.Entry(self.second_button_row_frame)
        self.translation_tx_field.pack(side="left", padx=(0, 3))
        self.translation_tx_field.config(width=4, font=("TkDefaultFont", 15))
        self.translation_tx_field.insert(0, "0")
        
        self.translation_ty_field_label = tk.Label(
            self.second_button_row_frame, text="Ty: ", font=("TkDefaultFont", 15),
        )
        self.translation_ty_field_label.pack(side="left", padx=(3, 0))
        
        self.translation_ty_field = tk.Entry(self.second_button_row_frame)
        self.translation_ty_field.pack(side="left", padx=(0, 5))
        self.translation_ty_field.config(width=4, font=("TkDefaultFont", 15))
        self.translation_ty_field.insert(0, "0")
        
        self.translation_button = tk.Button(
            self.second_button_row_frame, text="Transladar",  font=("TkDefaultFont", 15),
            command=lambda: self.translation_caller(int(self.translation_tx_field.get()), int(self.translation_ty_field.get()))
        )
        self.translation_button.pack(side="left", padx=(5,15))
        
        self.rotation_angle_field_label = tk.Label(
            self.second_button_row_frame, text="Ângulo (°): ", font=("TkDefaultFont", 15),
        )
        self.rotation_angle_field_label.pack(side="left", padx=(10, 0))
        
        self.rotation_angle_field = tk.Entry(self.second_button_row_frame)
        self.rotation_angle_field.pack(side="left", padx=(0, 5))
        self.rotation_angle_field.config(width=4, font=("TkDefaultFont", 15))
        self.rotation_angle_field.insert(0, "0")
        
        self.rotation_button = tk.Button(
            self.second_button_row_frame, text="Rotacionar",  font=("TkDefaultFont", 15),
            command=lambda: self.rotation_caller(int(self.rotation_angle_field.get()))
        )
        self.rotation_button.pack(side="left", padx=(5,15))
        
        self.rescale_sx_field_label = tk.Label(
            self.second_button_row_frame, text="Sx: ", font=("TkDefaultFont", 15),
        )
        self.rescale_sx_field_label.pack(side="left", padx=(10, 0))
        
        self.rescale_sx_field = tk.Entry(self.second_button_row_frame)
        self.rescale_sx_field.pack(side="left", padx=(0, 3))
        self.rescale_sx_field.config(width=4, font=("TkDefaultFont", 15))
        self.rescale_sx_field.insert(0, "1")
        
        self.rescale_sy_field_label = tk.Label(
            self.second_button_row_frame, text="Sy: ", font=("TkDefaultFont", 15),
        )
        self.rescale_sy_field_label.pack(side="left", padx=(3, 0))
        
        self.rescale_sy_field = tk.Entry(self.second_button_row_frame)
        self.rescale_sy_field.pack(side="left", padx=(0, 3))
        self.rescale_sy_field.config(width=4, font=("TkDefaultFont", 15))
        self.rescale_sy_field.insert(0, "1")
        
        self.rescale_button = tk.Button(
            self.second_button_row_frame, text="Aplicar Escala", 
            command=lambda: self.rescale_caller(float(self.rescale_sx_field.get()), float(self.rescale_sy_field.get())), font=("TkDefaultFont", 15),
        )
        self.rescale_button.pack(side="left", padx=(5,15))
        
        self.x_mirroring_button = tk.Button(
            self.second_button_row_frame, text="Reflexão X", font=("TkDefaultFont", 15),
            command=self.x_mirroring_caller
        )
        self.x_mirroring_button.pack(side="left", padx=10)
        
        self.y_mirroring_button = tk.Button(
            self.second_button_row_frame, text="Reflexão Y", font=("TkDefaultFont", 15),
            command=self.y_mirroring_caller
        )
        self.y_mirroring_button.pack(side="left", padx=10)
        
        self.xy_mirroring_button = tk.Button(
            self.second_button_row_frame, text="Reflexão XY",  font=("TkDefaultFont", 15),
            command=self.xy_mirroring_caller
        )
        self.xy_mirroring_button.pack(side="left", padx=10)
        
        
        # Botões para operações de transformação com polígonos
        self.polygons_transformations_label = tk.Label(
            self.third_button_row_frame, text="Polígonos", font=("TkDefaultFont", 15, "bold")
        )
        self.polygons_transformations_label.pack(side="left", padx=(0, 15))
        
        self.polygon_translation_tx_field_label = tk.Label(
            self.third_button_row_frame, text="Tx: ",  font=("TkDefaultFont", 15),
        )
        self.polygon_translation_tx_field_label.pack(side="left", padx=(10, 0))
        
        self.polygon_translation_tx_field = tk.Entry(self.third_button_row_frame)
        self.polygon_translation_tx_field.pack(side="left", padx=(0, 3))
        self.polygon_translation_tx_field.config(width=4, font=("TkDefaultFont", 15))
        self.polygon_translation_tx_field.insert(0, "0")
        
        self.polygon_translation_ty_field_label = tk.Label(
            self.third_button_row_frame, text="Ty: ", font=("TkDefaultFont", 15)
        )
        self.polygon_translation_ty_field_label.pack(side="left", padx=(3, 0))
        
        self.polygon_translation_ty_field = tk.Entry(self.third_button_row_frame)
        self.polygon_translation_ty_field.pack(side="left", padx=(0, 5))
        self.polygon_translation_ty_field.config(width=4, font=("TkDefaultFont", 15))
        self.polygon_translation_ty_field.insert(0, "0")
        
        self.polygon_translation_button = tk.Button(
            self.third_button_row_frame, text="Transladar", font=("TkDefaultFont", 15),
            command=lambda: self.polygon_translation_caller(int(self.polygon_translation_tx_field.get()), int(self.polygon_translation_ty_field.get()))
        )
        self.polygon_translation_button.pack(side="left", padx=(5,15))
        
        self.polygon_rotation_angle_field_label = tk.Label(
            self.third_button_row_frame, text="Ângulo (°): ", font=("TkDefaultFont", 15)
        )
        self.polygon_rotation_angle_field_label.pack(side="left", padx=(10, 0))
        
        self.polygon_rotation_angle_field = tk.Entry(self.third_button_row_frame)
        self.polygon_rotation_angle_field.pack(side="left", padx=(0, 5))
        self.polygon_rotation_angle_field.config(width=4, font=("TkDefaultFont", 15))
        self.polygon_rotation_angle_field.insert(0, "0")
        
        self.polygon_rotation_button = tk.Button(
            self.third_button_row_frame, text="Rotacionar", font=("TkDefaultFont", 15),
            command=lambda: self.polygon_rotation_caller(int(self.polygon_rotation_angle_field.get()))
        )
        self.polygon_rotation_button.pack(side="left", padx=(5,15))
        
        self.polygon_rescale_sx_field_label = tk.Label(
            self.third_button_row_frame, text="Sx: ", font=("TkDefaultFont", 15),
        )
        self.polygon_rescale_sx_field_label.pack(side="left", padx=(10, 0))
        
        self.polygon_rescale_sx_field = tk.Entry(self.third_button_row_frame)
        self.polygon_rescale_sx_field.pack(side="left", padx=(0, 3))
        self.polygon_rescale_sx_field.config(width=4, font=("TkDefaultFont", 15))
        self.polygon_rescale_sx_field.insert(0, "1")
        
        self.polygon_rescale_sy_field_label = tk.Label(
            self.third_button_row_frame, text="Sy: ",  font=("TkDefaultFont", 15)
        )
        self.polygon_rescale_sy_field_label.pack(side="left", padx=(3, 0))
        
        self.polygon_rescale_sy_field = tk.Entry(self.third_button_row_frame)
        self.polygon_rescale_sy_field.pack(side="left", padx=(0, 3))
        self.polygon_rescale_sy_field.config(width=4, font=("TkDefaultFont", 15))
        self.polygon_rescale_sy_field.insert(0, "1")

        self.polygon_rescale_button = tk.Button(
            self.third_button_row_frame, text="Aplicar Escala", font=("TkDefaultFont", 15),
            command=lambda: self.polygon_rescale_caller(float(self.polygon_rescale_sx_field.get()), float(self.polygon_rescale_sy_field.get()))
        )
        self.polygon_rescale_button.pack(side="left", padx=(5,15))

        self.polygon_x_mirroring_button = tk.Button(
            self.third_button_row_frame, text="Reflexão X", font=("TkDefaultFont", 15),
            command=self.polygon_x_mirroring_caller
        )
        self.polygon_x_mirroring_button.pack(side="left", padx=10)
        
        self.polygon_y_mirroring_button = tk.Button(
            self.third_button_row_frame, text="Reflexão Y", font=("TkDefaultFont", 15),
            command=self.polygon_y_mirroring_caller
        )
        self.polygon_y_mirroring_button.pack(side="left", padx=10)
        
        self.polygon_xy_mirroring_button = tk.Button(
            self.third_button_row_frame, text="Reflexão XY", font=("TkDefaultFont", 15),
            command=self.polygon_xy_mirroring_caller
        )
        self.polygon_xy_mirroring_button.pack(side="left", padx=10)


    
    # Método chamado quando ocorre um clique no canvas          
    def on_click(self, event):
        if self.selection_mode:
            if not self.start_point:
                self.start_point = (event.x, event.y)
                self.canvas.create_rectangle(self.start_point[0], self.start_point[1], self.start_point[0], self.start_point[1], outline="red", width=5)
            else:
                self.end_point = (event.x, event.y)
                self.canvas.create_rectangle(self.end_point[0], self.end_point[1], self.end_point[0], self.end_point[1], outline="red", width=4)
                self.canvas.create_rectangle(self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1], outline="red")
                self.selection_area = (self.start_point, self.end_point)
                self.start_point = None
                self.end_point = None
        else:
            if not self.start_point:
                self.start_point = (event.x, event.y)
                self.dots_coords_list.append(self.start_point)
                self.canvas.create_rectangle(self.start_point[0], self.start_point[1], self.start_point[0], self.start_point[1], outline="blue", width=5)
                self.canvas.create_text(self.start_point[0] - 18, self.start_point[1] + 5, text=self.letter, anchor="sw")
                self.letter = chr(ord(self.letter) + 1)
            else:
                self.end_point = (event.x, event.y)
                self.dots_coords_list.append(self.end_point)
                self.canvas.create_rectangle(self.end_point[0], self.end_point[1], self.end_point[0], self.end_point[1], outline="blue", width=5)
                self.canvas.create_text(self.end_point[0] + 10, self.end_point[1] + 5, text=self.letter, anchor="sw")
                self.letter = chr(ord(self.letter) + 1)
                if self.letter > 'Z':
                    self.letter = 'A'
                self.drawn_objects_coords.append((self.start_point, self.end_point))
                self.start_point = None
                self.end_point = None

               
                
    def clear_canvas(self):
        # Limpa todos os objetos desenhados no canvas e reinicializa as variáveis
        self.canvas.delete("all")
        self.dots_coords_list = []
        self.drawn_objects_coords = []
        self.updated_drawn_objects_coords = []
        self.polygon = None
        self.letter = 'A'
        self.selection_area = None
        self.start_point = None
        self.end_point = None
        self.selection_mode = False
        self.selection_mode_button.config(relief="raised")
        self.draw_mode_button.config(relief="sunken")
        
        
        
    def selection_mode_enabler(self):
        # Ativa o modo de seleção e altera a aparência dos botões correspondentes
        self.selection_mode = True
        self.selection_mode_button.config(relief="sunken")  # Botão de modo de seleção pressionado
        self.draw_mode_button.config(relief="raised")  # Botão de modo de desenho realçado

    def draw_mode_enabler(self):
        # Ativa o modo de desenho e altera a aparência dos botões correspondentes
        self.selection_mode = False
        self.selection_mode_button.config(relief="raised")  # Botão de modo de seleção realçado
        self.draw_mode_button.config(relief="sunken")  # Botão de modo de desenho pressionado
        
        

    def update_cursor_position(self, event):
        # Atualiza a posição do cursor na label correspondente
        self.cursor_position_label.config(text=f"x: {event.x}, y: {event.y}")
        
        

    def draw_line_dda_caller(self):
        # Chama a função para desenhar uma linha usando o algoritmo DDA
        if self.drawn_objects_coords:
            start, end = self.drawn_objects_coords[-1]
            self.draw_line_dda(start[0], start[1], end[0], end[1])
        else:
            print("Nenhum objeto definido.")

    def draw_line_dda(self, x1, y1, x2, y2):
        # Desenha uma linha usando o algoritmo DDA
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            return
        x_increment = dx / steps
        y_increment = dy / steps
        x = x1
        y = y1
        for _ in range(steps):
            # Desenha um ponto na posição arredondada atual
            self.canvas.create_rectangle(round(x), round(y), round(x), round(y), outline="black")
            x += x_increment
            y += y_increment
            
            

    def draw_line_bresenham_caller(self):
        # Chama a função para desenhar uma linha usando o algoritmo de Bresenham
        if self.drawn_objects_coords:
            start, end = self.drawn_objects_coords[-1]
            self.draw_line_bresenham(start[0], start[1], end[0], end[1])
        else:
            print("Nenhum objeto definido.")               

    def draw_line_bresenham(self, x1, y1, x2, y2):
        # Desenha uma linha usando o algoritmo de Bresenham
        dx = x2 - x1
        dy = y2 - y1
        const1, const2, p = None, None, None
        if dx >= 0:
            incrx = 1
        else:
            incrx = -1
            dx = -dx
        if dy >= 0:
            incry = 1
        else:
            incry = -1
            dy = -dy
        x, y = x1, y1
        # Desenha um ponto inicial
        self.canvas.create_rectangle(x, y, x, y, outline="black")
        if dy < dx:
            p = 2 * dy - dx
            const1 = 2 * dy
            const2 = 2 * (dy - dx)
            for _ in range(dx):
                x += incrx
                if p < 0:
                    p += const1
                else:
                    y += incry
                    p += const2
                # Desenha um ponto na posição arredondada atual
                self.canvas.create_rectangle(x, y, x, y, outline="black")
        else:
            p = 2 * dx - dy
            const1 = 2 * dx
            const2 = 2 * (dx - dy)
            for _ in range(dy):
                y += incry
                if p < 0:
                    p += const1
                else:
                    x += incrx
                    p += const2
                # Desenha um ponto na posição arredondada atual
                self.canvas.create_rectangle(x, y, x, y, outline="black")


               
    
    def draw_circle_bresenham_caller(self):
        # Método para chamar a função de desenho de círculo usando o algoritmo de Bresenham
        if self.drawn_objects_coords:
            start, end = self.drawn_objects_coords[-1]
            # Desenha uma linha entre os pontos inicial e final
            self.draw_line_bresenham(start[0], start[1], end[0], end[1])
            # Calcula o raio do círculo
            self.draw_circle_bresenham(start[0], start[1], self.calc_distance(start[0], start[1], end[0], end[1]))
        else:
            print("Nenhum objeto definido.")
            
    
    
    def calc_distance(self, x1, y1, x2, y2):
        # Método para calcular o raio da circunferência utilizando a fórmula da distância euclidiana
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    
    def draw_circle_bresenham(self, xc, yc, r):
        # Método para desenhar um círculo usando o algoritmo de Bresenham
        x = 0
        y = r
        p = 3 - 2 * r
        while x <= y:
            # Plota os pontos simétricos do círculo em torno do centro (xc, yc)
            self.plot_circle_points(xc, yc, x, y)
            if p < 0:
                p += 4 * x + 6
            else:
                p += 4 * (x - y) + 10
                y -= 1
            x += 1
    
    def plot_circle_points(self, xc, yc, x, y):
        # Método para desenhar os pontos simétricos do círculo em torno do centro (xc, yc)
        # Cria retângulos em torno dos pontos para simular os pontos do círculo
        self.canvas.create_rectangle(xc + x, yc + y, xc + x, yc + y, outline="black")
        self.canvas.create_rectangle(xc - x, yc + y, xc - x, yc + y, outline="black")
        self.canvas.create_rectangle(xc + x, yc - y, xc + x, yc - y, outline="black")
        self.canvas.create_rectangle(xc - x, yc - y, xc - x, yc - y, outline="black")
        self.canvas.create_rectangle(xc + y, yc + x, xc + y, yc + x, outline="black")
        self.canvas.create_rectangle(xc - y, yc + x, xc - y, yc + x, outline="black")
        self.canvas.create_rectangle(xc + y, yc - x, xc + y, yc - x, outline="black")
        self.canvas.create_rectangle(xc - y, yc - x, xc - y, yc - x, outline="black")
        
        
    
    def connect_all_alphabet_order(self):
        # Método para conectar todos os pontos em ordem alfabética
        self.connect_all_dots()
        self.polygon = self.dots_coords_list.copy()
        self.start_point = None
        self.end_point = None

    def connect_all_dots(self):
        # Método para conectar todos os pontos na lista de coordenadas de pontos
        for i in range(len(self.dots_coords_list) - 1):
            self.draw_line_dda(self.dots_coords_list[i][0], self.dots_coords_list[i][1], self.dots_coords_list[i + 1][0], self.dots_coords_list[i + 1][1])
        # Conecta o último ponto ao primeiro para formar um polígono fechado
        self.draw_line_dda(self.dots_coords_list[-1][0], self.dots_coords_list[-1][1], self.dots_coords_list[0][0], self.dots_coords_list[0][1])
        
        
    
    def region_snip_cohen_sutherland_caller(self):
        # Método para chamar a função de recorte de região usando o algoritmo de Cohen-Sutherland
        if self.selection_area:
            if self.drawn_objects_coords:
                # Limpa o canvas antes de realizar o recorte
                self.canvas.delete("all")
                for start, end in self.drawn_objects_coords:
                    if start and end:
                        # Obtém os limites da área de seleção
                        x_min, x_max, y_min, y_max = self.get_selection_area_bounds()
                        # Realiza o recorte de Cohen-Sutherland
                        self.region_snip_cohen_sutherland(start[0], start[1], end[0], end[1], x_min, y_min, x_max, y_max)
                        if self.inside:
                            # Se o segmento estiver completamente dentro da área de seleção, adiciona à lista de objetos atualizados
                            self.updated_drawn_objects_coords.append((self.start_point, self.end_point))
                            self.start_point = None
                            self.end_point = None
                # Atualiza a lista de objetos desenhados com os objetos que permaneceram após o recorte
                self.drawn_objects_coords = self.updated_drawn_objects_coords.copy()
                self.updated_drawn_objects_coords = []
            else:
                print("Nenhum objeto definido.")
        else:
            print("Região de recorte não definida.")
    
    def get_selection_area_bounds(self):
        # Método para obter os limites da área de seleção
        if self.selection_area[0][0] > self.selection_area[1][0]:
            x_min, x_max = self.selection_area[1][0], self.selection_area[0][0]
        else:
            x_min, x_max = self.selection_area[0][0], self.selection_area[1][0]
        if self.selection_area[0][1] > self.selection_area[1][1]:
            y_min, y_max = self.selection_area[1][1], self.selection_area[0][1]
        else:
            y_min, y_max = self.selection_area[0][1], self.selection_area[1][1]
        return x_min, x_max, y_min, y_max
    
    
    
    def region_snip_cohen_sutherland(self, x1, y1, x2, y2, x_min, y_min, x_max, y_max):
        # Método para realizar o recorte de Cohen-Sutherland
        accept = False
        done = False
        while not done:
            # Calcula os códigos de recorte para os pontos inicial e final
            code1 = self.compute_code(x1, y1, x_min, y_min, x_max, y_max)
            code2 = self.compute_code(x2, y2, x_min, y_min, x_max, y_max)
            if code1 == 0 and code2 == 0:
                # Segmento completamente dentro da área de seleção
                accept = True
                done = True
            elif code1 & code2:
                # Segmento completamente fora da área de seleção
                done = True
            else:
                if code1 != 0:
                    code = code1
                else:
                    code = code2
                if code & 1:
                    x = x_min
                    y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                elif code & 2:
                    x = x_max
                    y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                elif code & 4:
                    y = y_min
                    x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                elif code & 8:
                    y = y_max
                    x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                if code == code1:
                    x1 = x
                    y1 = y
                else:
                    x2 = x
                    y2 = y
        if accept:
            # Desenha o segmento se estiver completamente dentro da área de seleção
            self.draw_line_dda(round(x1), round(y1), round(x2), round(y2))
            self.inside = True
            self.start_point = (round(x1), round(y1))
            self.end_point = (round(x2), round(y2))
        else:
            self.inside = False
            self.start_point = None
            self.end_point = None
    
    def compute_code(self, x, y, x_min, y_min, x_max, y_max):
        # Método para calcular o código de recorte para um ponto específico
        code = 0
        if x < x_min:
            code = code | 1
        elif x > x_max:
            code = code | 2
        if y < y_min:
            code = code | 4
        elif y > y_max:
            code = code | 8
        return code



    def region_snip_liang_barsky_caller(self):
        # Chama a função para recortar linhas usando o algoritmo de Liang-Barsky
        if self.selection_area:
            if self.drawn_objects_coords:
                self.canvas.delete("all")
                for start, end in self.drawn_objects_coords:
                    if start and end:
                        # Obtém as coordenadas da área de seleção
                        x_min, x_max, y_min, y_max = self.get_selection_area_bounds()
                        # Realiza o recorte usando o algoritmo de Liang-Barsky
                        self.region_snip_liang_barsky(start[0], start[1], end[0], end[1], x_min, y_min, x_max, y_max)
                        if self.inside:
                            # Adiciona a linha recortada à lista de objetos atualizados
                            self.updated_drawn_objects_coords.append((self.start_point, self.end_point))
                            self.start_point = None
                            self.end_point = None
                # Atualiza a lista de objetos desenhados para refletir as mudanças
                self.drawn_objects_coords = self.updated_drawn_objects_coords.copy()
                self.updated_drawn_objects_coords = []
            else:
                print("Nenhum objeto definido.")
        else:
            print("Região de recorte não definida.")
            
            

    def region_snip_liang_barsky(self, x1, y1, x2, y2, x_min, y_min, x_max, y_max):
        # Realiza o recorte de uma linha usando o algoritmo de Liang-Barsky
        self.u1 = 0.0
        self.u2 = 1.0
        dx = x2 - x1
        dy = y2 - y1
        # Executa os testes de recorte
        if self.clip_test(-dx, x1 - x_min, self.u1, self.u2):
            if self.clip_test(dx, x_max - x1, self.u1, self.u2):
                if self.clip_test(-dy, y1 - y_min, self.u1, self.u2):
                    if self.clip_test(dy, y_max - y1, self.u1, self.u2):
                        if self.u2 < 1.0:  # Se u2 for menor que 1.0, ajusta x2 e y2
                            x2 = x1 + self.u2 * dx
                            y2 = y1 + self.u2 * dy
                        if self.u1 > 0.0:  # Se u1 for maior que 0.0, ajusta x1 e y1
                            x1 = x1 + self.u1 * dx
                            y1 = y1 + self.u1 * dy
                        # Desenha a linha recortada no canvas
                        self.draw_line_dda(round(x1), round(y1), round(x2), round(y2))
                        self.inside = True
                        self.start_point = (round(x1), round(y1))
                        self.end_point = (round(x2), round(y2))
                        return
        self.inside = False
        self.start_point = None
        self.end_point = None

    def clip_test(self, p, q, u1, u2):
        # Executa o teste de recorte
        r = None
        result = True
        if p < 0.0:
            r = q / p
            if r > u2:
                result = False
            elif r > u1:
                self.u1 = r  # Atualiza u1 se necessário
        elif p > 0.0:
            r = q / p
            if r < u1:
                result = False
            elif r < u2:
                self.u2 = r  # Atualiza u2 se necessário
        elif q < 0.0:
            result = False
        return result


    def translation_caller(self, tx, ty):
        # Chama a função para realizar uma translação nos objetos desenhados
        if self.drawn_objects_coords:
            start, end = self.drawn_objects_coords[-1]
            # Atualiza as coordenadas dos objetos desenhados com a translação
            self.drawn_objects_coords[-1] = self.translation(start[0], start[1], end[0], end[1], tx, ty)
        else:
            print("Nenhum objeto definido.")  # Mensagem de aviso se nenhum objeto estiver definido

    def translation(self, x1, y1, x2, y2, tx, ty):
        # Realiza uma translação nos pontos especificados e desenha a linha resultante
        x1, y1 = x1 + tx, y1 + ty
        x2, y2 = x2 + tx, y2 + ty 
        # Desenha a linha resultante no canvas
        self.draw_line_dda(x1, y1, x2, y2)
        # Retorna as coordenadas transladadas dos pontos
        return (x1, y1), (x2, y2)
    
    

    def rotation_caller(self, angle_degrees):
        # Chama a função para realizar uma rotação nos objetos desenhados
        if self.drawn_objects_coords:
            start, end = self.drawn_objects_coords[-1]
            # Calcula as novas coordenadas dos pontos após a rotação
            x1, y1, x2, y2 = self.rotation(start[0], start[1], end[0], end[1], -angle_degrees, start[0], start[1])
            # Atualiza as coordenadas dos objetos desenhados com a rotação
            self.drawn_objects_coords[-1] = (x1, y1), (x2, y2)
            self.canvas.delete("all")
            # Desenha a linha resultante no canvas
            self.draw_line_dda(x1, y1, x2, y2)
        else:
            print("Nenhum objeto definido.")

    def rotation(self, x1, y1, x2, y2, angle_degrees, cx, cy):
        # Realiza uma rotação nos pontos especificados em torno de um ponto central
        angle_rad = math.radians(angle_degrees)
        # Calcula as novas coordenadas do ponto de início após a rotação
        x_rotated = (x1 - cx) * math.cos(angle_rad) - (y1 - cy) * math.sin(angle_rad) + cx
        y_rotated = (x1 - cx) * math.sin(angle_rad) + (y1 - cy) * math.cos(angle_rad) + cy
        x1, y1 = x_rotated, y_rotated
        # Calcula as novas coordenadas do ponto final após a rotação
        x_rotated = (x2 - cx) * math.cos(angle_rad) - (y2 - cy) * math.sin(angle_rad) + cx
        y_rotated = (x2 - cx) * math.sin(angle_rad) + (y2 - cy) * math.cos(angle_rad) + cy
        x2, y2 = x_rotated, y_rotated
        return round(x1), round(y1), round(x2), round(y2)
    
    

    def rescale_caller(self, sx, sy):
        # Chama a função para realizar uma escala nos objetos desenhados
        if self.drawn_objects_coords:
            start, end = self.drawn_objects_coords[-1]
            # Calcula as novas coordenadas dos pontos após a escala
            x1, y1, x2, y2 = self.rescale(start[0], start[1], end[0], end[1], sx, sy)
            # Atualiza as coordenadas dos objetos desenhados com a escala
            self.drawn_objects_coords[-1] = (x1, y1), (x2, y2)
            self.canvas.delete("all")
            # Desenha a linha resultante no canvas
            self.draw_line_dda(x1, y1, x2, y2)
        else:
            print("Nenhum objeto definido.")

    def rescale(self, x1, y1, x2, y2, sx, sy):
        # Realiza uma escala nos pontos especificados
        x3, y3 = x1, y1 
        x4, y4 = x2 * sx, y2 * sy 
        return round(x3), round(y3), round(x4), round(y4)

    
    
    def x_mirroring_caller(self):
        # Chama a função para fazer espelhamento em torno do eixo x
        if self.drawn_objects_coords:
            start, end = self.drawn_objects_coords[-1]
            x1, y1, x2, y2 = self.x_mirroring(start[0], start[1], end[0], end[1])
            self.drawn_objects_coords[-1] = (x1, y1), (x2, y2)
            # Limpa o canvas e redesenha o plano cartesiano
            self.canvas.delete("all")
            self.draw_cartesian_plane_axis()
            # Desenha a linha espelhada
            self.draw_line_dda(x1, y1, x2, y2)
        else:
            print("Nenhum objeto definido.")

    def x_mirroring(self, x1, y1, x2, y2):
        # Calcula as coordenadas espelhadas em torno do eixo x
        canvas_height = self.canvas.winfo_height()
        x3, y3 = x1, canvas_height - y1
        x4, y4 = x2, canvas_height - y2
        return round(x3), round(y3), round(x4), round(y4)
    
    

    def y_mirroring_caller(self):
        # Chama a função para fazer espelhamento em torno do eixo y
        if self.drawn_objects_coords:
            start, end = self.drawn_objects_coords[-1]
            x1, y1, x2, y2 = self.y_mirroring(start[0], start[1], end[0], end[1])
            self.drawn_objects_coords[-1] = (x1, y1), (x2, y2)
            # Limpa o canvas e redesenha o plano cartesiano
            self.canvas.delete("all")
            self.draw_cartesian_plane_axis()
            # Desenha a linha espelhada
            self.draw_line_dda(x1, y1, x2, y2)
        else:
            print("Nenhum objeto definido.")

    def y_mirroring(self, x1, y1, x2, y2):
        # Calcula as coordenadas espelhadas em torno do eixo y
        canvas_width = self.canvas.winfo_width()
        x3, y3 = canvas_width - x1, y1
        x4, y4 = canvas_width - x2, y2
        return round(x3), round(y3), round(x4), round(y4)
    
    

    def xy_mirroring_caller(self):
        # Chama a função para fazer espelhamento em torno dos eixos x e y simultaneamente
        if self.drawn_objects_coords:
            start, end = self.drawn_objects_coords[-1]
            x1, y1, x2, y2 = self.xy_mirroring(start[0], start[1], end[0], end[1])
            self.drawn_objects_coords[-1] = (x1, y1), (x2, y2)
            # Limpa o canvas e redesenha o plano cartesiano
            self.canvas.delete("all")
            self.draw_cartesian_plane_axis()
            # Desenha a linha espelhada
            self.draw_line_dda(x1, y1, x2, y2)
        else:
            print("Nenhum objeto definido.")

    def xy_mirroring(self, x1, y1, x2, y2):
        # Calcula as coordenadas espelhadas em torno dos eixos x e y simultaneamente
        canvas_height = self.canvas.winfo_height()
        canvas_width = self.canvas.winfo_width()
        x3, y3 = canvas_width - x1, canvas_height - y1
        x4, y4 = canvas_width - x2, canvas_height - y2
        return round(x3), round(y3), round(x4), round(y4)


    
    def draw_polygon(self):
        # Desenha o polígono definido pelas coordenadas armazenadas na lista 'polygon'
        for i in range(len(self.polygon) - 1):
            # Desenha as arestas do polígono
            self.draw_line_dda(self.polygon[i][0], self.polygon[i][1], self.polygon[i + 1][0], self.polygon[i + 1][1])
            # Adiciona rótulos às vértices do polígono
            self.canvas.create_text(self.polygon[i][0] + 15, self.polygon[i][1] + 5, text=chr(ord('A') + i), anchor="center")
            # Destaca as vértices do polígono
            self.canvas.create_rectangle(self.polygon[i][0], self.polygon[i][1], self.polygon[i][0], self.polygon[i][1], outline="blue", width=5)
            self.canvas.create_rectangle(self.polygon[i + 1][0], self.polygon[i + 1][1], self.polygon[i + 1][0], self.polygon[i + 1][1], outline="blue", width=5)
        # Fecha o polígono, ligando a última vértice à primeira
        self.draw_line_dda(self.polygon[-1][0], self.polygon[-1][1], self.polygon[0][0], self.polygon[0][1])
        self.canvas.create_text(self.polygon[-1][0] + 15, self.polygon[-1][1] + 5, text=chr(ord('A') + len(self.polygon) - 1), anchor="center")



    def calc_polygon_center(self):
        # Calcula o centro geométrico do polígono
        x_sum = 0
        y_sum = 0
        for x, y in self.polygon:
            x_sum += x
            y_sum += y
        return x_sum / len(self.polygon), y_sum / len(self.polygon)
    
    

    def draw_cartesian_plane_axis(self):
        # Desenha os eixos do plano cartesiano
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.canvas.create_line(0, canvas_height / 2, canvas_width, canvas_height / 2, fill="black")
        self.canvas.create_line(canvas_width / 2, 0, canvas_width / 2, canvas_height, fill="black")
        # Desenha as marcações nos eixos
        for i in range(0, canvas_width, 20):
            self.canvas.create_line(i, canvas_height / 2 - 2, i, canvas_height / 2 + 2, fill="black")
        for i in range(0, canvas_height, 20):
            self.canvas.create_line(canvas_width / 2 - 2, i, canvas_width / 2 + 2, i, fill="black")
            
            

    def polygon_translation_caller(self, tx, ty):
        # Chama a função para transladar o polígono
        if self.polygon:
            self.polygon_translation(tx, ty)
        else:
            print("Nenhum polígono definido.")

    def polygon_translation(self, tx, ty):
        # Translada o polígono pelas coordenadas (tx, ty)
        for i in range(len(self.polygon)):
            self.polygon[i] = (self.polygon[i][0] + tx, self.polygon[i][1] + ty)
        # Limpa o canvas e redesenha o polígono
        self.canvas.delete("all")
        self.draw_polygon()
    
    
    
    def polygon_rotation_caller(self, angle_degrees):
        # Chama a função para rotacionar o polígono
        if self.polygon:
            self.polygon_rotation(-angle_degrees)
        else:
            print("Nenhum polígono definido.")

    def polygon_rotation(self, angle_degrees):
        # Rotaciona o polígono em torno de seu centro
        center_x, center_y = self.calc_polygon_center()
        angle_rad = math.radians(angle_degrees)
        for i in range(len(self.polygon)):
            # Aplica a fórmula de rotação para cada vértice do polígono
            x_rotated = (self.polygon[i][0] - center_x) * math.cos(angle_rad) - (self.polygon[i][1] - center_y) * math.sin(angle_rad) + center_x
            y_rotated = (self.polygon[i][0] - center_x) * math.sin(angle_rad) + (self.polygon[i][1] - center_y) * math.cos(angle_rad) + center_y
            self.polygon[i] = (round(x_rotated), round(y_rotated))
        # Limpa o canvas e redesenha o polígono
        self.canvas.delete("all")
        self.draw_polygon()
        
        

    def polygon_rescale_caller(self, sx, sy):
        # Chama a função para redimensionar o polígono
        if self.polygon:
             self.polygon_rescale(sx, sy)
        else:
            print("Nenhum polígono definido.")

    def polygon_rescale(self, sx, sy):
        # Redimensiona o polígono mantendo seu centro
        center_x, center_y = self.calc_polygon_center()
        for i in range(len(self.polygon)):
            # Aplica o fator de escala em relação ao centro do polígono
            x = self.polygon[i][0]
            y = self.polygon[i][1]
            x_rescaled = (x - center_x) * sx + center_x
            y_rescaled = (y - center_y) * sy + center_y
            self.polygon[i] = (round(x_rescaled), round(y_rescaled))
        # Limpa o canvas e redesenha o polígono
        self.canvas.delete("all")
        self.draw_polygon()
    
    
    
    def polygon_x_mirroring_caller(self):
        # Chama a função para espelhar o polígono em relação ao eixo x
        if self.polygon:
            self.polygon_x_mirroring()
        else:
            print("Nenhum polígono definido.")         

    def polygon_x_mirroring(self):
        # Espelha o polígono em relação ao eixo x
        canvas_height = self.canvas.winfo_height()
        for i in range(len(self.polygon)):
            # Inverte a coordenada y de cada vértice do polígono em relação à altura do canvas
            self.polygon[i] = (self.polygon[i][0], canvas_height - self.polygon[i][1])
        # Limpa o canvas e redesenha o plano cartesiano e o polígono
        self.canvas.delete("all")
        self.draw_cartesian_plane_axis()
        self.draw_polygon()



    def polygon_y_mirroring_caller(self):
        # Chama a função para espelhar o polígono em relação ao eixo y
        if self.polygon:
            self.polygon_y_mirroring()
        else:
            print("Nenhum polígono definido.")

    def polygon_y_mirroring(self):
        # Espelha o polígono em relação ao eixo y
        canvas_width = self.canvas.winfo_width()
        for i in range(len(self.polygon)):
            # Inverte a coordenada x de cada vértice do polígono em relação à largura do canvas
            self.polygon[i] = (canvas_width - self.polygon[i][0], self.polygon[i][1])
        # Limpa o canvas e redesenha o plano cartesiano e o polígono
        self.canvas.delete("all")
        self.draw_cartesian_plane_axis()
        self.draw_polygon()



    def polygon_xy_mirroring_caller(self):
        # Chama a função para espelhar o polígono em relação aos eixos x e y
        if self.polygon:
            self.polygon_xy_mirroring()
        else:
            print("Nenhum polígono definido.")

    def polygon_xy_mirroring(self):
        # Espelha o polígono em relação aos eixos x e y
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        for i in range(len(self.polygon)):
            # Inverte as coordenadas x e y de cada vértice do polígono em relação à largura e altura do canvas
            self.polygon[i] = (canvas_width - self.polygon[i][0], canvas_height - self.polygon[i][1])
        # Limpa o canvas e redesenha o plano cartesiano e o polígono
        self.canvas.delete("all")
        self.draw_cartesian_plane_axis()
        self.draw_polygon()



if __name__ == "__main__":
    app = Application()
    app.mainloop()
