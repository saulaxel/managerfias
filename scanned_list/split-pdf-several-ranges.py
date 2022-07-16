import PyPDF2

pdf_origen = 'libro-escaneado.pdf'
pdf_destino = 'relieves-{letra}.pdf'
rangos = []
with open('rangos-relieves.txt') as f:
    lineas_sin_salto = [linea.strip() for linea in f.readlines()]
    rangos = [(rango[0], int(rango[1]), int(rango[2])) for rango in [linea.split('-') for linea in lineas_sin_salto]]
    
    print(rangos)
    
pdf_origen_fileobj = open(pdf_origen, 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_origen_fileobj)
    
for letra, inicio, fin in rangos:
    pdf_writer = PyPDF2.PdfFileWriter()
    
    for i in range(inicio - 1, fin):  # [inicio, fin]
        pdf_writer.addPage(pdf_reader.getPage(i))
    
    with open(pdf_destino.format(letra=letra), 'wb') as f_out:
        pdf_writer.write(f_out)