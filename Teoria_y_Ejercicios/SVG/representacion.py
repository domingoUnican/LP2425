from dataclasses import dataclass, field
from typing import List
import matplotlib.pyplot as plt
from typing import Optional

@dataclass
class SVG:
    tipo: str
    atributos: dict
    hijos: List['SVG']
    plt: any = field(default=plt, init=False)

    def to_string(self, n):
        resultado = f'{" "*n}{self.tipo}\n'
        for hijo in self.hijos():
            if hijo:
                resultado += hijo.to_string(n+2)
        return resultado

    def dibuja(self, ax: Optional[any] = None) -> any:
        """
        Dibuja el objeto SVG según su tipo y sus atributos.
        Si no se proporciona un objeto eje (ax), se crea uno.
        Luego dibuja de forma recursiva los hijos.
        """
        if ax is None:
            fig, ax = self.plt.subplots()

        if self.tipo.lower() == "rect":
            # Se espera que los atributos incluyan: x, y, width, height, y opcionalmente color.
            x = self.atributos.get("x", 0)
            y = self.atributos.get("y", 0)
            width = self.atributos.get("width", 10)
            height = self.atributos.get("height", 10)
            color = self.atributos.get("color", "blue")
            # Crear un rectángulo con plt.Rectangle y agregarlo al eje
            rect = plt.Rectangle((x, y), width, height, color=color, label=self.atributos.get("label", "Rectángulo"))
            ax.add_patch(rect)

        elif self.tipo.lower() == "circle":
            # Se esperan atributos: cx, cy, radius, y opcionalmente color.
            cx = self.atributos.get("cx", 0.5)
            cy = self.atributos.get("cy", 0.5)
            radius = self.atributos.get("radius", 0.4)
            color = self.atributos.get("color", "red")
            circle = plt.Circle((cx, cy), radius, color=color, label=self.atributos.get("label", "Círculo"))
            ax.add_patch(circle)

        elif self.tipo.lower() == "triangle":
            # Se espera que los atributos incluyan una lista de puntos en 'points'
            # Cada punto es una tupla (x, y). Se cierra el polígono repitiendo el primer punto.
            points = self.atributos.get("points", [(1, 1), (2, 3), (3, 1)])
            if points:
                xs = [p[0] for p in points] + [points[0][0]]
                ys = [p[1] for p in points] + [points[0][1]]
                color = self.atributos.get("color", "green")
                ax.fill(xs, ys, color=color, label=self.atributos.get("label", "Triángulo"))
        # Se pueden agregar más tipos según se necesite

        # Dibujar de forma recursiva los hijos
        for hijo in self.hijos:
            hijo.dibuja(ax)

        ax.set_aspect('equal')
        return ax


if __name__ == '__main__':
    # Crear algunos objetos SVG
    rect_svg = SVG(
        tipo="rect",
        atributos={"x": 0.1, "y": 0.1, "width": 0.6, "height": 0.3, "color": "blue", "label": "Rectángulo"},
        hijos=[]
    )
    circle_svg = SVG(
        tipo="circle",
        atributos={"cx": 0.5, "cy": 0.5, "radius": 0.4, "color": "red", "label": "Círculo"},
        hijos=[]
    )
    triangle_svg = SVG(
        tipo="triangle",
        atributos={"points": [(1, 1), (2, 3), (3, 1)], "color": "green", "label": "Triángulo"},
        hijos=[circle_svg, rect_svg]
    )

    
    # Dibujar
    ax = triangle_svg.dibuja()
    plt.legend()
    plt.show()
