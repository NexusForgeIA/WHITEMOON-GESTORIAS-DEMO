#!/usr/bin/env python3
"""Genera docs/contrato-compraventa.pdf (plantilla en blanco para rellenar)."""
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

PURPLE = colors.HexColor("#7c3aed")
PURPLE_DARK = colors.HexColor("#5b21b6")
GREY = colors.HexColor("#555555")

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "contrato-compraventa.pdf")
OUT = os.path.abspath(OUT)

HEADER_H = 22 * mm
FOOTER_H = 16 * mm


def draw_header(c):
    c.setFillColor(PURPLE)
    c.rect(0, PAGE_H - HEADER_H, PAGE_W, HEADER_H, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGIN, PAGE_H - HEADER_H + 8 * mm, "WhiteMoon Gestoría IA")
    c.setFont("Helvetica", 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - HEADER_H + 8.5 * mm,
                      "Trámites de tráfico y transportes")


def draw_footer(c):
    c.setFillColor(PURPLE)
    c.rect(0, 0, PAGE_W, FOOTER_H, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(
        PAGE_W / 2, FOOTER_H / 2 - 3,
        "WhiteMoon Gestoría IA  ·  comercial@whitemoon.es  ·  643 199 580  ·  whitemoon.es",
    )


class Cursor:
    TOP_PAD = 10 * mm
    BOT_PAD = 10 * mm

    def __init__(self, c):
        self.c = c
        self.y = PAGE_H - HEADER_H - self.TOP_PAD

    def ensure(self, needed):
        if self.y - needed < FOOTER_H + self.BOT_PAD:
            self.c.showPage()
            draw_header(self.c)
            draw_footer(self.c)
            self.y = PAGE_H - HEADER_H - self.TOP_PAD

    def title(self, text):
        self.ensure(14 * mm)
        self.c.setFillColor(PURPLE_DARK)
        self.c.setFont("Helvetica-Bold", 14)
        self.c.drawCentredString(PAGE_W / 2, self.y, text)
        self.y -= 4 * mm
        self.c.setStrokeColor(PURPLE)
        self.c.setLineWidth(1)
        self.c.line(MARGIN, self.y, PAGE_W - MARGIN, self.y)
        self.y -= 7 * mm

    def section(self, text):
        self.ensure(11 * mm)
        self.c.setFillColor(PURPLE)
        self.c.rect(MARGIN, self.y - 5.5 * mm, CONTENT_W, 7 * mm, stroke=0, fill=1)
        self.c.setFillColor(colors.white)
        self.c.setFont("Helvetica-Bold", 10.5)
        self.c.drawString(MARGIN + 3 * mm, self.y - 3.5 * mm, text)
        self.y -= 10 * mm

    def field(self, label):
        self.ensure(8 * mm)
        self.c.setFillColor(colors.black)
        self.c.setFont("Helvetica", 10)
        self.c.drawString(MARGIN, self.y, label + ":")
        label_w = self.c.stringWidth(label + ": ", "Helvetica", 10)
        self.c.setStrokeColor(GREY)
        self.c.setLineWidth(0.5)
        self.c.line(MARGIN + label_w + 2 * mm, self.y - 1, PAGE_W - MARGIN, self.y - 1)
        self.y -= 7 * mm

    def paragraph(self, text, font="Helvetica", size=9.5, leading=4.3 * mm, gap=2 * mm):
        self.c.setFillColor(colors.black)
        self.c.setFont(font, size)
        words = text.split()
        line = ""
        max_w = CONTENT_W
        for w in words:
            test = (line + " " + w).strip()
            if self.c.stringWidth(test, font, size) <= max_w:
                line = test
            else:
                self.ensure(leading + 2 * mm)
                self.c.setFont(font, size)
                self.c.drawString(MARGIN, self.y, line)
                self.y -= leading
                line = w
        if line:
            self.ensure(leading + 2 * mm)
            self.c.setFont(font, size)
            self.c.drawString(MARGIN, self.y, line)
            self.y -= leading
        self.y -= gap

    def spacer(self, h):
        self.y -= h


def build():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("Contrato de compraventa de vehículo usado")
    c.setAuthor("WhiteMoon Gestoría IA")
    draw_header(c)
    draw_footer(c)
    cur = Cursor(c)

    cur.title("CONTRATO DE COMPRAVENTA DE VEHÍCULO USADO")

    cur.section("DATOS DEL VENDEDOR")
    cur.field("Nombre / Empresa")
    cur.field("NIF / CIF / NIE")
    cur.field("Domicilio")
    cur.field("Representante de la empresa / NIF / NIE")

    cur.section("DATOS DEL COMPRADOR")
    cur.field("Nombre / Empresa")
    cur.field("NIF / CIF / NIE")
    cur.field("Domicilio")
    cur.field("Representante de la empresa / NIF / NIE")

    cur.section("DATOS DEL VEHÍCULO")
    cur.field("Marca y Modelo")
    cur.field("Matrícula / Bastidor")
    cur.field("Kilómetros / Fecha 1ª Matriculación")

    cur.section("CLÁUSULAS")
    clausulas = [
        "1. El vendedor declara que el vehículo objeto de este contrato es de su "
        "legítima propiedad, que se encuentra libre de cargas y gravámenes y al "
        "corriente del pago de los impuestos que le son exigibles.",
        "2. El precio pactado por la compraventa del vehículo es de: "
        "_______________________ euros, que el comprador abona al vendedor en "
        "este acto, sirviendo el presente documento como carta de pago.",
        "3. El vendedor manifiesta que no existen cargas, embargos, reservas de "
        "dominio ni limitaciones de disposición sobre el vehículo, y que no "
        "pesa sobre el mismo ninguna sanción o procedimiento pendiente.",
        "4. El vendedor facilita al comprador todos los documentos necesarios "
        "para la inscripción del cambio de titularidad en la Jefatura de Tráfico "
        "(DGT): permiso de circulación, ficha técnica y mandatos firmados.",
        "5. El comprador asume todas las responsabilidades derivadas de la "
        "propiedad y uso del vehículo desde la fecha de este contrato, "
        "comprometiéndose a tramitar el cambio de titularidad en plazo.",
    ]
    for cl in clausulas:
        cur.paragraph(cl, gap=2 * mm)

    cur.spacer(1 * mm)
    cur.section("FIRMAS")
    cur.paragraph("En _______________________  a  _______  de  "
                  "_____________________  de  __________", gap=8 * mm)

    cur.ensure(16 * mm)
    line_y = cur.y
    half = CONTENT_W / 2
    c.setStrokeColor(GREY)
    c.setLineWidth(0.5)
    c.line(MARGIN, line_y, MARGIN + half - 10 * mm, line_y)
    c.line(MARGIN + half + 10 * mm, line_y, PAGE_W - MARGIN, line_y)
    c.setFont("Helvetica", 9.5)
    c.setFillColor(colors.black)
    c.drawCentredString(MARGIN + (half - 10 * mm) / 2, line_y - 5 * mm, "Firmado: EL VENDEDOR")
    c.drawCentredString(MARGIN + half + 10 * mm + (half - 10 * mm) / 2, line_y - 5 * mm,
                        "Firmado: EL COMPRADOR")

    c.save()
    print("Generado:", OUT)


if __name__ == "__main__":
    build()
