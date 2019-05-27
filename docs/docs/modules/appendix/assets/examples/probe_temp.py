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
    ensight.variables.activate("temperature")
    ensight.part.select_all()

    ensight.query_interact.select_varname_begin("""temperature""")
    ensight.query_interact.number_displayed(20)
    ensight.query_interact.query("xyz")

    # Reference potential
    ensight.query_interact.create(-3.554e-3,-33.8174e-3,-118e-3)
    ensight.query_interact.create(-5.4752e-3,34.5691e-3,135e-3)
    
    # Save output
    print ("Save data to %s" % outputfile)
    ensight.query_interact.save(outputfile)

    
def main(argv):
    print ("probe_temp.py")
    inputfile = 'Thermics.case'
    outputfile = 'probe_temp.data'
    bp = False

    try:
        opts, args = getopt.getopt(argv,"hi:o:b",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('probe_temp.py -i <inputfile> -o <outputfile> [-b]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('probe_temp.py -i <inputfile> -o <outputfile> [-b]')
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-b", "--bp"):
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
print ("Running prob_temp %s" % sys.argv[1:])
main(sys.argv[1:])
