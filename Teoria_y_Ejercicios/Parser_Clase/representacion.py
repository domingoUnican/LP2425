from dataclasses import dataclass
from typing import List

MAPEO_COLORES = {
    "red": "r",
    "green": "g",
    "blue": "b",
    "black": "k",
    "white": "w",
}

@dataclass
class SVG:
    tipo: str
    atributos: dict
    hijos: List['SVG']
    fig: any = None
    ax: any = None
    plt: any = None

    def dibuja(self):
        print("Dibujando:", self.tipo, self.atributos)

        if self.tipo == "circle":
            coordX = float(self.atributos["cx"]) / 100
            coordY = float(self.atributos["cy"]) / 100
            radio = float(self.atributos["r"]) / 100
            linewidth = float(self.atributos["stroke-width"])
            colorPerimetro = MAPEO_COLORES.get(self.atributos.get("stroke"), "k")
            colorRelleno = MAPEO_COLORES.get(self.atributos.get("fill"), "none")
            print("Círculo:", coordX, coordY, radio, colorPerimetro, colorRelleno)
            objeto = self.plt.Circle(
                (coordX, coordY), radio, edgecolor=colorPerimetro, facecolor=colorRelleno, linewidth=linewidth
            )
            self.ax.add_patch(objeto)

        elif self.tipo == "rect":
            coordX = float(self.atributos["x"]) / 100
            coordY = float(self.atributos["y"]) / 100
            width = float(self.atributos["width"]) / 100
            height = float(self.atributos["height"]) / 100
            linewidth = float(self.atributos["stroke-width"])
            colorPerimetro = MAPEO_COLORES.get(self.atributos.get("stroke"), "k")
            colorRelleno = (
                "none"
                if self.atributos.get("fill") == "none"
                else MAPEO_COLORES.get(self.atributos.get("fill"), "none")
            )
            print("Rectángulo:", coordX, coordY, width, height, colorPerimetro, colorRelleno)
            objeto = self.plt.Rectangle(
                (coordX, coordY), width, height, edgecolor=colorPerimetro, facecolor=colorRelleno, linewidth=linewidth
            )
            self.ax.add_patch(objeto)

        self.ax.set_aspect("equal")

        for hijo in self.hijos:
            print("Hijo:", hijo.tipo)
            hijo.fig = self.fig
            hijo.ax = self.ax
            hijo.plt = self.plt
            hijo.dibuja()

    def to_string(self, n):
        resultado = f'{" " * n}{self.tipo}\n'
        for hijo in self.hijos:
            resultado += hijo.to_string(n + 2)
        return resultado