import sys, getopt
import os
import string
import math

from ensight.objs import *
from ensight.core.tool_extension import *

def main(argv):
    print ("Bz_biotsavart.py")
    inputfile = None
    outputfile = None
    axicfg = None
    
    n_sample = 200

    r = 0
    z0 = -10.e-3
    z1 = 10.e-3

    current = 31000
    current_B = 0
    current_H = 0

    
    try:
        opts, args = getopt.getopt(argv,"hi:o:n:0:1:c:f:s",["ifile=","samples=","output=","z0=","z1=","current=","axicfg="])
    except getopt.GetoptError:
        print ('Bz_biotsavart.py -i <inputfile> [-n <samples>] [-z <z0> -z1 <z1>] [-c <current> -f <axicfg>] [-s -o <output>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('Bz_biotsavart.py -i <inputfile> [-n <samples>] [-z <z0> -z1 <z1>] [-c <current> -f <axicfg>] [-s -o <output>]')
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-n", "--samples"):
            n_sample = arg
        elif opt in ("-f", "--axicfg"):
            bmapinput = arg
            # add a check for file existence
            axicfg=bmapinput.replace(".d","")
        elif opt in ("-c", "--current"):
            current = float(arg)
        elif opt in ("-0", "--z0"):
            z0 = float(arg)
        elif opt in ("-1", "--z1"):
            z1 = float(arg)
        elif opt in ("-o", "--output"):
            outputfile = arg
        elif opt in ("-s"):
            save = True
        else:
            print ("Bz_biotsavart.py: error unknown option %s" % opt)

    # check if inputfile exist
    print ('Loading is %s' % inputfile)
    print ('Output=%s' % outputfile)

    nr_axi = 1
    nz_axi = n_sample # n_sample??

    ensight.part.select_default()
    ensight.part.modify_begin()
    ensight.part.elt_representation("3D_feature_2D_full")
    ensight.part.modify_end()
    ensight.data.binary_files_are("native")
    ensight.data.format("ensight case")
    ensight.data.shift_time(1.000000,0.000000,0.000000)
    ensight.data.replace(inputfile)
    ensight.part.select_all()
    ensight.part.modify_begin()
    ensight.part.elt_representation("3D_border_2D_full")
    ensight.part.modify_end()
    ensight.part.colorby_palette("B_bs")
    ensight.legend.select_palette_begin("B_bs")
    ensight.legend.visible("ON")
    ensight.part.select_all()
    ensight.part.opaqueness(0.5)
    ensight.view_transf.view_recall("-Y")
    ensight.view_transf.fit(0)
    #WARNING: the following line failed to translate because the function could not be found in the ensight python module
    #   Actual error: 'module' object has no attribute 'use_qbox_off'

    ensight.viewport.select_default()
    ensight.view_transf.function("global")
    ensight.variables.evaluate("bx = B_bs[X]")
    ensight.part.select_all()
    ensight.variables.evaluate("by = B_bs[Y]")
    ensight.part.select_all()
    ensight.variables.evaluate("bz = B_bs[Z]")

    ####

    x = 0
    y = 0
    # print "r=%d, t=%d, x=%g, y=%g, t_exp=%d"%(r, i, x, y, angle_exp[i] )
        
    ensight.curve.select_default()
    ensight.part.select_all()
        
    ensight.query_ent_var.begin()        
    ensight.query_ent_var.description("")
    ensight.query_ent_var.query_type("generated")
    ensight.query_ent_var.number_of_sample_pts(nz_axi+1)
    ensight.query_ent_var.constrain("line_tool")
    ensight.query_ent_var.line_loc(1,x,y,z0)
    ensight.query_ent_var.line_loc(2,x,y,z1)
    ensight.query_ent_var.distance("z_from_origin")
    ensight.query_ent_var.variable_1("bz")
    ensight.query_ent_var.generate_over("distance")
    ensight.query_ent_var.variable_2("DISTANCE")
    ensight.query_ent_var.end()

    ensight.query_ent_var.query()
    ensight.curve.select_begin(0)
    ensight.curve.assign("rescale","bz","vs.","Distance","for","line","tool")
    ensight.plot.select_begin(0)
    ensight.curve.desc("Bz")
    ensight.plot.plot_title("Bz")
    ensight.plot.axis_x_title("Z[mm]")
    ensight.plot.axis_x_title("Z[mm]")
    ensight.plot.axis_y_title("T")
    ensight.plot.axis_y_title("T")
    ensight.curve.select_default()
    ensight.plot.select_default()
    ensight.solution_time.current_step(0)
    ensight.solution_time.update_to_current()
    ensight.curve.select_begin(0)
    ensight.curve.save("formatted","Bz_biot.dat")

    # remove plots
    ensight.plot.select_begin(0)
    ensight.plot.delete_plot()
    ensight.curve.delete()
    ensight.curve.select_default()

    # create input data for B_Map
    if axicfg:
        r_axi = 0
        z0_axi = z0
        z1_axi = z1
        B_Map_input = open("Bmap.in", "w")
        B_Map_input.write("%g\n"%current);
        ###TODO check first if Bitter:
        B_Map_input.write("%g\n"%current_B);
        ###TODO check first if Supra:
        # B_Map_input.write("%g\n"%current_S);
        B_Map_input.write("%g\n"%r_axi);
        B_Map_input.write("%g\n"%r_axi);
        B_Map_input.write("%g\n"%z0_axi);
        B_Map_input.write("%g\n"%z1_axi);
        B_Map_input.write("%d\n"%nr_axi);
        B_Map_input.write("%d\n"%nz_axi);
        B_Map_input.close();
        
        # system call to B_Map
        print "Running: B_Map --interactive %s.d < Bmap.in > B_Map.log 2>&1 " % axicfg
        os.system(r"B_Map --interactive %s.d < Bmap.in > B_Map.log 2>&1 " % axicfg)
        
        # rename output
        os.rename("%s_Field_Map.dat" % axicfg, "%s_Field_Map_bz.dat" % axicfg )

    # 
    import numpy as np
    import io
    import matplotlib.pyplot as plt
    print "Export to MatPlotlib"

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel('z[mm]')
    ax1.set_ylabel('T')
    ax1.set_title(r'Bz on Oz axis (I = %g A)' % current )

    if axicfg:
        ana = None
        try:
            ana = np.genfromtxt("%s_Field_Map_bz.dat" % axicfg )
        except:
            print "Failed loading ana data %s_Field_Map_bz.dat" % axicfg
            pass
        z = ana[:,1]
        bz = ana[:,3]
        ax1.plot(z,bz, c='r', marker='d', markevery=4, label='ana')

    biot = np.genfromtxt("Bz_biot.dat", skip_header=6, skip_footer=6)
    z_biot =  biot[:,4]
    bz_biot = biot[:,0]
    ax1.plot(z_biot,bz_biot, c='g', marker='s', markevery=4, label='biot-savart')
        
    ax1.grid(True)
    leg = ax1.legend()
    
    plt.xlim(z0,z1)
    if save:
        plt.savefig("Bz_I%gA.png" % current, format='png')
    else:
        plt.show()

    plt.close(fig)

    os.rename("Bz_biot.dat", "Bz_biot_I%gA.dat" % current )
    os.rename("%s_Field_Map_bz.dat" % axicfg, "%s_Field_Map_bz_I%gA.dat" % (axicfg,current) )

    # Get Bz(0,0,0)
    ensight.query_interact.select_varname_begin("""B_bs 'Z'""")
    ensight.query_interact.query("xyz")
    ensight.part.select_all()
    ensight.query_interact.create(0.00000e+00,0.00000e+00,0.00000e+00)
    ensight.query_interact.save("Bz0_I%gA" % current)
    
# if __name__ == "__main__":
print ("Running Bz_biotsavart %s" % sys.argv[1:])
main(sys.argv[1:])
