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

def probes(outputfile, bp):
    ensight.part.select_all()
    ensight.part.modify_begin()
    ensight.part.elt_representation("3D_border_2D_full")
    ensight.part.modify_end()
    
    # Pick-up some points
    ensight.variables.activate("potential")
    ensight.part.select_all()
    # ensight.part.colorby_palette("potential")
    # ensight.legend.select_palette_begin("potential")
    # ensight.legend.visible("ON")

    ensight.query_interact.select_varname_begin("""potential""")
    ensight.query_interact.number_displayed(20)
    ensight.query_interact.query("xyz")

    # Reference potential
    ensight.query_interact.create(-21.75e-3,0.e-3,-421.15e-3)
    
    # HP probes and eventually BP probes
    if bp:
        ensight.query_interact.create(-4.3e-3,  27.16e-3, 128.e-3)
    ensight.query_interact.create(0.e-3,34.e-3,-128.e-3)
        
    if bp:
        ensight.query_interact.create(-6.62e-3, 41.83e-3, 145.e-3)
    ensight.query_interact.create(0.e-3,50.e-3,-145.e-3)

    if bp:
        ensight.query_interact.create(-27.37e-3, 53.68e-3, 161.e-3)
    ensight.query_interact.create(0.e-3,70.e-3,-161.e-3)

    if bp:
        ensight.query_interact.create(-58.37e-3, 58.37e-3, 177.e-3)
    ensight.query_interact.create(0.e-3,96.5e-3,-177.e-3)

    if bp:
        ensight.query_interact.create(-89.8e-3, 65.24e-3, 188.e-3)
    ensight.query_interact.create(0.e-3,126.e-3,-188.e-3)

    if bp:
        ensight.query_interact.create(-122.35e-3, 74.98e-3, 199.e-3)
    ensight.query_interact.create(-12.55e-3,159.51e-3,-199.e-3)

    if bp:
        ensight.query_interact.create(-150.49e-3, 92.22e-3, 210.e-3)
    ensight.query_interact.create(-40.62e-3,169.19e-3,-200.e-3)
    
    # Save output
    print ("Save data to %s" % outputfile)
    ensight.query_interact.save(outputfile)

    
def main(argv):
    print ("probe_voltage.py")
    inputfile = 'Electrics.case'
    outputfile = 'probe_volt.data'
    bp = False

    try:
        opts, args = getopt.getopt(argv,"hi:o:b",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('probe_voltage.py -i <inputfile> -o <outputfile> [-b]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('probe_voltage.py -i <inputfile> -o <outputfile> [-b]')
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
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
    probes(outputfile, bp)

# if __name__ == "__main__":
print ("Running prob_voltage %s" % sys.argv[1:])
main(sys.argv[1:])
