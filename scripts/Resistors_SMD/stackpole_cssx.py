#http://katalog.we-online.com/en/pbs/WE-MAPI]

#sizes,shapes,etc]
#name, range, L, W, pad-w, pad-gap, pad-h, component-height
resistors = [
['CSS0603',     '5-15m',            1.6,    0.8,    1.0,    0.5,    1.27,  0.3],
['CSS0805',     '5-15m',            2.03,   1.27,   1.8,    0.66,   2.18,  0.3],
['CSS1206',     '1-50m',            3.2,    1.6,    1.6,    1.0,    2.18,  0.65],
['CSS2010',     '1-3m',             5.08,   2.54,   2.89,   1.22,   2.92,  0.79],
['CSS2010',     '3.1-100m',         5.08,   2.54,   2.29,   2.41,   2.92,  0.65],
['CSS2512',     '0.5-4m',           6.25,   3.3,    3.05,   1.27,   3.68,  0.79],
['CSS2512',     '4.1-75m',          6.25,   3.3,    2.11,   3.18,   3.68,  0.65],
['CSSH2512',    '0.5m',             6.25,   3.3,    3.05,   1.27,   3.68,  0.79],
['CSSH2512',    '0.6-2.9m_4.1-10m', 6.25,   3.3,    2.19,   3.0,    3.68,  0.79],
['CSSH2512',    '3-4m',             6.25,   3.3,    2.79,   1.8,    3.68,  0.79],
['CSS2725',     '0.25-0.5m',        6.81,   6.45,   3.18,   1.32,   6.86,  0.99],
['CSS2725',     '1m',               6.81,   6.45,   3.18,   1.32,   6.86,  1.09],
['CSS2725',     '1.5m',             6.81,   6.45,   3.18,   1.32,   6.86,  0.99],
['CSS2725',     '2m',               6.81,   6.45,   3.18,   1.32,   6.86,  0.89],
['CSS2725',     '2.5m',             6.81,   6.45,   3.18,   1.32,   6.86,  0.89],
['CSS2725',     '3m',               6.81,   6.45,   3.18,   1.32,   6.86,  0.89],
['CSS2728',     '4-100m',           6.71,   7.19,   2.75,   3.51,   7.82,  0.99],
['CSSH2728',    '4-100m',           6.71,   7.19,   2.75,   3.51,   7.82,  0.99],
['CSS4527',     '0.5-5m',           11.43,  6.85,   4.8,    5.51,   8.74,  1.5],
['CSS4527',     '5.1-120m',         11.43,  6.85,   3.4,    8.31,   8.74,  1.5],
]

import sys
import os
import math

output_dir = os.getcwd()

#if specified as an argument, extract the target directory for output footprints
if len(sys.argv) > 1:
    out_dir = sys.argv[1]
    
    if os.path.isabs(out_dir) and os.path.isdir(out_dir):
        output_dir = out_dir
    else:
        out_dir = os.path.join(os.getcwd(),out_dir)
        if os.path.isdir(out_dir):
            output_dir = out_dir

if output_dir and not output_dir.endswith(os.sep):
    output_dir += os.sep
        
#import KicadModTree files
sys.path.append("..\\..")
from KicadModTree import *
from KicadModTree.nodes.specialized.PadArray import PadArray

prefix = "R_"
part = "Stackpole_{pn}_{rng}"
dims = "{l:0.1f}mmx{w:0.1f}mm"

desc = "Resistor, Stackpole, {pn}"
tags = "resistor current sensing smd"

def roundup(val):
    return math.ceil(val*100)/100

for resistor in resistors:
    name,rng,l,w,x,g,y,h = resistor

    fp_name = prefix + part.format(pn=str(name), rng=str(rng))
    
    fp = Footprint(fp_name)
    
    description = desc.format(pn = part.format(pn=str(name), rng=str(rng))) + ", " + dims.format(l=l,w=w)
    
    fp.setTags(tags)
    fp.setAttribute("smd")
    fp.setDescription(description)
    
    # set general values
    fp.append(Text(type='reference', text='REF**', at=[0,-roundup(y/2)-1], layer='F.SilkS'))
    fp.append(Text(type='value', text=fp_name, at=[0,roundup(y/2)+1.5], layer='F.Fab'))
    
    #calculate pad center
    #pad-width pw
    pw = x # (x-g) / 2
    c = g/2 + pw/2
    
    #add the component outline
    fp.append(RectLine(start=[-roundup(l/2),-roundup(w/2)],end=[roundup(l/2),roundup(w/2)],layer='F.Fab',width=0.15))
    
    layers = ["F.Cu","F.Paste","F.Mask"]
    
    #add pads
    fp.append(Pad(number=1,at=[-roundup(c),0],layers=layers,shape=Pad.SHAPE_RECT,type=Pad.TYPE_SMT,size=[roundup(pw),roundup(y)]))
    fp.append(Pad(number=2,at=[roundup(c),0],layers=layers,shape=Pad.SHAPE_RECT,type=Pad.TYPE_SMT,size=[roundup(pw),roundup(y)]))
    
    #add inductor courtyard
    cx = roundup(c + pw/2)
    cy = roundup(y / 2)
    
    fp.append(RectLine(start=[-cx,-cy],end=[cx,cy],offset=0.35,width=0.05,grid=0.05,layer="F.CrtYd"))
    
    #add lines
    fp.append(Line(start=[-roundup(g/2)+0.2,-roundup(w/2)-0.1],end=[roundup(g/2)-0.2,-roundup(w/2)-0.1]))
    fp.append(Line(start=[-roundup(g/2)+0.2,roundup(w/2)+0.1],end=[roundup(g/2)-0.2,roundup(w/2)+0.1]))
    
    # Add refdes to fabrication layer
    fontsize_max = 1.0
    if fontsize_max * 5 > l:
        fontsize_max = l / 5
    if fontsize_max + 0.2 > w:
        fontsize_max = w - 0.2
    if fontsize_max < 0.1:
        fontsize_max = 0.1
    font_thickness = roundup(fontsize_max * 0.15)
    fontsize = [fontsize_max, fontsize_max]

    fp.append(Text(type='user', text='%R', size=fontsize, thickness=font_thickness, at=[0, 0], layer='F.Fab'))

    #Add a model
    fp.append(Model(filename="${KISYS3DMOD}/Resistor_SMD.3dshapes/" + fp_name + ".wrl"))
    
    #filename
    filename = output_dir + fp_name + ".kicad_mod"
    
    file_handler = KicadFileHandler(fp)
    file_handler.writeFile(filename)
    