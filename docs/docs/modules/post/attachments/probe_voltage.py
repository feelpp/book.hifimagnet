import sys, getopt

from ensight.objs import *
from ensight.core.tool_extension import *

def load(inputfile):
    ensight.part.select_default()

    ensight.data.binary_files_are("native")
    ensight.data.format("ensight case")
    ensight.data.shift_time(1.000000, 0.000000, 0.000000)
    ensight.solution_time.monitor_for_new_steps("off")
    ensight.data.replace(inputfile)

def probes(outputfile, bp, field):
    ensight.part.select_all()
    ensight.part.modify_begin()
    ensight.part.elt_representation("3D_border_2D_full")
    ensight.part.modify_end()
    
    # Pick-up some points
    ensight.variables.activate(field)
    ensight.part.select_all()
    # ensight.part.colorby_palette("potential")
    # ensight.legend.select_palette_begin("potential")
    # ensight.legend.visible("ON")

    varname = """%s""" % field
    ensight.query_interact.select_varname_begin(varname)
    ensight.query_interact.number_displayed(20)
    ensight.query_interact.query("xyz")

    # Reference potential
    ensight.query_interact.create(-21.75,0.,-421.15)
    
    # HP probes and eventually BP probes
    if bp:
        ensight.query_interact.create(-4.3,  27.16, 128.)
    ensight.query_interact.create(0.,34.,-128.)
        
    if bp:
        ensight.query_interact.create(-6.62, 41.83, 145.)
    ensight.query_interact.create(0.,50.,-145.)

    if bp:
        ensight.query_interact.create(-27.37, 53.68, 161.)
    ensight.query_interact.create(0.,70.,-161.)

    if bp:
        ensight.query_interact.create(-58.37, 58.37, 177.)
    ensight.query_interact.create(0.,96.5,-177.)

    if bp:
        ensight.query_interact.create(-89.8, 65.24, 188.)
    ensight.query_interact.create(0.,126.,-188.)

    if bp:
        ensight.query_interact.create(-122.35, 74.98, 199.)
    ensight.query_interact.create(-12.55,159.51,-199.)

    if bp:
        ensight.query_interact.create(-150.49, 92.22, 210.)
    ensight.query_interact.create(-40.62,169.19,-200.)
    
    # Save output
    print ("Save data to %s" % outputfile)
    ensight.query_interact.save(outputfile)

    
def main(argv):
    print ("probe_voltage.py")
    inputfile = 'Electrics.case'
    outputfile = 'probe_volt.data'
    field = 'hdg_poisson_electro_potential' # or 'thermo_electric.electric.electric_potential'
    bp = False

    try:
        opts, args = getopt.getopt(argv,"hi:o:bf:",["ifile=","ofile=","field="])
    except getopt.GetoptError:
        print ('probe_voltage.py -i <inputfile> -o <outputfile> [-b] [-f <field>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('probe_voltage.py -i <inputfile> -o <outputfile> [-b] [-f <field>]')
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-f", "--field"):
            field = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-b"):
            bp = True
        else:
            print ("probe_voltage.py: error unknown option %s" % opt)

    # check if inputfile exist
    print ('Loading is %s' % inputfile)
    print ('Output=%s' % outputfile)
    print ('BP=%s' % bp)

    load(inputfile)
    probes(outputfile, bp, field)

# if __name__ == "__main__":
print ("Running prob_voltage %s" % sys.argv[1:])
main(sys.argv[1:])
