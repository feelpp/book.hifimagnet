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

def add_extrafields(inputs):
    fields = []

    # Create a newfield
    ensight.part.select_all() # or ensight.part.select_begin(1,2,...)
    ensight.variables.evaluate("EleVol = EleMetric(plist,30)")
    fields.append("EleVol")

    if "potential" in inputs:
        ensight.variables.evaluate("V = potential")
        fields.append("V")

    if "current" in inputs:
        ensight.variables.evaluate("J = current / 1.e+06")
        ensight.variables.evaluate("J_axi = RecToCyl(J,0)")
        ensight.variables.evaluate("J_P1 = ElemToNodeWeighted(plist,J,EleVol)")
        ensight.variables.evaluate("J_P1_axi = RecToCyl(J_P1,0)")
        fields.append("J")
        fields.append("J_P1")
        fields.append("J_P1_axi")
        fields.append("J_axi")

    if "temperature" in inputs:
        ensight.variables.evaluate("T = temperature - 273.15")
        fields.append("T")

    if "elasticity_displacement" in inputs:
        ensight.variables.evaluate("U = elasticity_displacement / 1.e-03")
        fields.append("U")
        ensight.variables.evaluate("U_axi = RecToCyl(U,0)")
        fields.append("U_axi")
        
    if "elasticity_von_mises_criterions" in inputs:
        ensight.variables.evaluate("VonMises = elasticity_von_mises_criterions / 1.e+6")
        ensight.variables.evaluate("VonMises_P1 = ElemToNodeWeighted(plist,VonMises,EleVol)")
        fields.append("VonMises")
        fields.append("VonMises_P1")

    if "Bext" in inputs:
        ensight.variables.evaluate("Bext_P1 = ElemToNodeWeighted(plist,Bext,EleVol)")
        fields.append("Bext_P1")
        ensight.variables.evaluate("Bext_axi = RecToCyl(Bext,0)")
        fields.append("Bext_axi")
        
    if "Fext" in inputs:
        ensight.variables.evaluate("Fext_P1 = ElemToNodeWeighted(plist,Fext,EleVol)")
        fields.append("Fext_P1")
        ensight.variables.evaluate("Fext_axi = RecToCyl(Fext_P1,0)")
        fields.append("Fext_axi")

    if "F" in inputs:
        ensight.variables.evaluate("F_P1 = ElemToNodeWeighted(plist,F,EleVol)")
        fields.append("F_P1")
        ensight.variables.evaluate("F_axi = RecToCyl(F_P1,0)")
        fields.append("F_axi")

    return fields

def getfields():
    fields = []
    print ("Get list of fields:")
    vars = core.VARIABLES
    for var in vars:
        name = var.DESCRIPTION
        if var.VARTYPE == ensight.objs.enums.ENS_VAR_TENSOR:
            print ("tensor field: ", name)
        if var.VARTYPE == ensight.objs.enums.ENS_VAR_VECTOR:
            print ("vector field: ", name)
        elif var.VARTYPE == ensight.objs.enums.ENS_VAR_SCALAR:
            print ("scalar field: ", name)
        fields.append(name)

    P0_vars = core.find_objs(core.VARIABLES, filter={enums.LOCATION: enums.ENS_VAR_ELEM})
    for var in P0_vars:
        name = var.DESCRIPTION
        print (name, ": P0 interpolation")

    extra_fields = add_extrafields(fields)
    return fields + extra_fields

def view(field):
    print ("view for %s" % field)
    ensight.part.select_all()
    ensight.part.modify_begin()
    ensight.part.elt_representation("3D_border_2D_full")
    ensight.part.modify_end()

    # Create a newfield
    ensight.part.select_all() # or ensight.part.select_begin(1,2,...)
    ensight.variables.evaluate("EleVol = EleMetric(plist,30)")

    if field == "Bext" or field == "Bext_P1" or field == "Bext_axi":
        # Update Legend
        legend = "T"
        ensight.view_transf.function("global")
        ensight.legend.select_palette_begin(field)
        ensight.legend.title_name("Bext [T]")
        ensight.legend.format("%.2f")
        
    elif field == "Fext" or field == "Fext_P1" or field == "Fext_axi":
        # Update Legend
        legend = "N"
        ensight.view_transf.function("global")
        ensight.legend.select_palette_begin(field)
        ensight.legend.title_name("Fext [N]")
        ensight.legend.format("%.4e")

    elif field == "F" or field == "F_P1" or field == "F_axi":
        # Update Legend
        legend = "N"
        ensight.view_transf.function("global")
        ensight.legend.select_palette_begin(field)
        ensight.legend.title_name("F [N]")
        ensight.legend.format("%.4e")

    elif field == "potential" or field == "V":
        # Update Legend
        legend = "V"
        ensight.view_transf.function("global")
        ensight.legend.select_palette_begin(field)
        ensight.legend.title_name("V [V]")
        ensight.legend.format("%.2f")

    elif field == "displacement" or field == "elasticity_displacement":
        # Update Legend
        legend = "m"
        ensight.view_transf.function("global")
        ensight.legend.select_palette_begin(field)
        ensight.legend.title_name("U [m]")
        ensight.legend.format("%.2e")

    elif field == "U" or field == "U_axi":
        # Update Legend
        legend = "mm"
        ensight.view_transf.function("global")
        ensight.legend.select_palette_begin(field)
        ensight.legend.title_name("U [mm]")
        ensight.legend.format("%.2f")

    elif field == "current":
        legend = "A/m<up>2<no>"
        # Update Legend
        ensight.part.modify_begin()
        ensight.part.elt_representation("Full")
        ensight.part.modify_end()

        ensight.view_transf.function("global")
        ensight.legend.select_palette_begin(field)
        ensight.legend.title_name("J [%s]" % legend)
        # ensight.legend.format("%.2f")

    elif field == "J_P1" or field == "J" or field == "J_axi" or field == "J_P1_axi":
        legend = "A/mm<up>2<no>"
        # Update Legend
        ensight.part.modify_begin()
        ensight.part.elt_representation("Full")
        ensight.part.modify_end()

        ensight.view_transf.function("global")
        ensight.legend.select_palette_begin(field)
        ensight.legend.title_name("J [%s]" % legend)
        ensight.legend.format("%.2e")

    elif field == "temperature":
        legend = "K"
        # Update Legend
        ensight.view_transf.function("global")
        ensight.legend.select_palette_begin(field)
        ensight.legend.title_name("T [%s]" % legend)
        ensight.legend.format("%.2f")

    elif field == "T":
        legend = "C"
        # Update Legend
        ensight.view_transf.function("global")
        ensight.legend.select_palette_begin(field)
        ensight.legend.title_name("T [%s]" % legend)
        ensight.legend.format("%.2f")

    elif field == "elasticity_von_mises_criterions":
        legend = "Pa"
        # Update Legend
        ensight.part.modify_begin()
        ensight.part.elt_representation("Full")
        ensight.part.modify_end()

        ensight.view_transf.function("global")
        ensight.legend.select_palette_begin(field)
        ensight.legend.title_name("VonMises [%s]" % legend)
        ensight.legend.format("%.2e")

    elif field == "VonMises" or "VonMises_P1":
        legend = "MPa"
        # Update Legend
        ensight.part.modify_begin()
        ensight.part.elt_representation("Full")
        ensight.part.modify_end()

        ensight.view_transf.function("global")
        ensight.legend.select_palette_begin(field)
        ensight.legend.title_name("VonMises [%s]" % legend)
        ensight.legend.format("%.2f")
    else:
        print ("Field: %s not supported" % field)
        return None, None

    ensight.part.select_all()
    ensight.part.colorby_palette(field)
    ensight.legend.select_palette_begin(field)
    ensight.legend.visible("ON")

    ensight.view_transf.rotate(-88.125, -1.82432055, 0)
    ensight.viewport.select_default()
    ensight.view_transf.function("global")

    # ensight.part.modify_begin()
    ensight.part.select_all()
    ensight.clip.begin()
    ensight.clip.tool("xyz_box")
    ensight.clip.box_origin(0, 0, -0.800000012)
    ensight.clip.box_axis("x", 1, 0, 0)
    ensight.clip.box_axis("y", 0, 1, 0)
    ensight.clip.box_axis("z", 0, 0, 1)
    ensight.clip.box_length(0.49126631, 0.49126631, 1.10000002)
    ensight.clip.domain("outside")
    ensight.clip.end()
    ensight.clip.create()

    # Change viewpoint
    ensight.view_transf.rotate(18.0169926, -138.100082, 0)
    ensight.view_transf.translate(0.00323051144, -0.182990178, 0)
    ensight.view_transf.zoom(0.45)

    # ensight.viewport.perspective("OFF")
    return field, legend

def stats(name):
    print ("Compute stats for %s" % name)
    ensight.part.select_all()
    ensight.variables.activate(name)
    ensight.variables.evaluate("vMax = Max(plist,%s,[],Compute_Per_part)" % name)
    ensight.variables.evaluate("vMin = Min(plist,%s,[],Compute_Per_part)" % name)
    ensight.variables.evaluate("vMean = SpaMean(plist,%s,[],Compute_Per_part)" % name)
    # ex: ensight.variables.evaluate("StatMoment = StatMoment(plist,1.0,0,Compute_Per_part)")
    # 0: sum
    # 1: average
    # 2: variance
    # 3: skewness ??
    # 4: kurtosis ??
    ensight.variables.evaluate("vAverage = StatMoment(plist,%s,1,Compute_Per_part)" % name)
    ensight.variables.evaluate("vVariance = StatMoment(plist,%s,2,Compute_Per_part)" % name)

    ensight.variables.evaluate("vVol = Vol(plist,Compute_Per_part)")

    for key in ["vMax", "vMin", "vMean", "vVariance", "vVol"]:
        ensight.variables.select_byname_begin(key)
        ensight.variables.save_constants("%s_%s.dat" % (name, key))


# SUBROUTINE for selecting newly created parts
def find_parts(prev=None):
    l = ensight.query_parts(parts="all",client=1)
    out = []
    for i in l:
        out.append(i[0])
    if (prev):
        for i in prev:
            try:
                out.remove(i)
            except:
                pass
    return out
#
# SUBROUTINE to loop through all timesteps to figure out min and max over time
def find_minmax(step_min,step_max,varname):
	nstep = step_max - step_min + 1
	min_val = 9e9
	max_val = -9e9
	ensight.variables.activate(varname)
	a = ensight.query(ensight.VARIABLE_OBJECTS)
	var_list = a[2]
	for i in range(len(var_list)):
		name_now = var_list[i]
		if name_now == varname:
			var_id = i
	#
	for i in range(nstep):
		ensight.solution_time.current_step(i)
		ensight.solution_time.update_to_current()
		b = ensight.query(ensight.VARIABLE_INFORMATION,var_id)
		local_min_val = b[2][0]
		local_max_val = b[2][1]
		if local_min_val < min_val:
			min_val = local_min_val
		if local_max_val > max_val:
			max_val = local_max_val
	#
	return(min_val,max_val)
        
def call_iso_loop(num_bins, min_value, increment, new_parts, total_vol):
	xy = []
	xyquery = []
	for i in range(num_bins):
		# select the isovolume, and constrict range to be Ith bar
		lower_band = i  * increment + min_value
		upper_band = lower_band + increment
		ave_value = (upper_band + lower_band) / 2.0
		# change the isovolume range
		ensight.part.select_begin(new_parts)
		ensight.part.modify_begin()
		ensight.isos.min(lower_band)
		ensight.isos.max(upper_band)
		ensight.part.modify_end()
		ensight.variables.evaluate("elem_vol = EleSize(plist)")
		ensight.variables.evaluate("sum_elesize = StatMoment(plist,elem_vol,0)")
		eval_str = "fractional_size = sum_elesize / " + str(total_vol)
		ensight.variables.evaluate(eval_str)
		frac_size = ensight.ensvariable("fractional_size")[0]
		#
		xy.append([i + 1,lower_band,upper_band,frac_size])
		xyquery.append([lower_band,frac_size])
		xyquery.append([upper_band,frac_size])
	return(xy,xyquery)

def distribution(field, num_bins, save_dist):
    print ("Compute distribution for %s" % field)
    ensight.command.delay_refresh("ON")

    ensight.variables.activate(field)

    # Calculate some range extents here based on part(s) selected
    ensight.part.select_all()
    eval_1 = "tmp_Min = Min(plist,%s)" % str(field)
    eval_2 = "tmp_Max = Max(plist,%s)" % str(field)
    ensight.variables.evaluate(eval_1)
    ensight.variables.evaluate(eval_2)
    min_value = ensight.ensvariable("tmp_Min")[0]
    max_value = ensight.ensvariable("tmp_Max")[0]
    total_range = max_value - min_value
    increment = total_range / num_bins

    # Make IsoVolume
    existing_parts = find_parts()
    ensight.isos.select_default()
    ensight.part.modify_begin()
    ensight.isos.type("isovolume")
    ensight.part.modify_end()
    ensight.part.modify_begin()
    ensight.isos.min(min_value)
    ensight.isos.max(max_value)
    ensight.part.modify_end()
    ensight.part.select_all()
    ensight.isos.begin()
    ensight.isos.variable(field)
    ensight.isos.end()
    ensight.isos.create()
    new_parts = find_parts(existing_parts)

    # Scalar Count based on Fraction of Total Volume calculation.
    ensight.part.select_all()
    # Scalar Count based on Fraction of Total Volume calculation.
    ensight.variables.evaluate("EleSize = EleSize(plist)")
    ensight.variables.evaluate("Total_Volume = StatMoment(plist,EleSize,0)")
    total_vol = ensight.ensvariable("Total_Volume")[0]

    xy,xyquery =  call_iso_loop(num_bins, min_value,increment,new_parts,total_vol)
    # Make histogram from the xy array of values.
    print "="*25
    print "Bar, Min,   Max,   Fraction of Total"
    for i in range(num_bins):
        print ("%i, %5.2f, %5.2f, %7.6f" % (xy[i][0], xy[i][1], xy[i][2], xy[i][3]) )
	#
    # Build a query and plotter from this information
    ensight.query_xy_create(field+" Distribution", field, "Fraction of Total Volume", xyquery)
    plot_cnt = ensight.query(ensight.PLOT_COUNT)
    new_plot = plot_cnt[1][0]
    query_cnt = ensight.query(ensight.QUERY_COUNT)
    new_query = query_cnt[1][0] - 1
    # Figure out the display attributes of the query
    query = ensight.query(ensight.QUERY_DISPLAY_ATTRIBUTES,new_query)
    items = query[1][0].rsplit(" ")
    items.reverse()
    items.append("rescale")
    items.reverse()
    ensight.curve.select_begin(new_plot)
    ensight.curve.assign(str(items[0]),str(items[1]),str(items[2]))
    ensight.plot.select_begin(new_plot)
    ensight.curve.marker("none")
    ensight.command.delay_refresh("OFF")
    if save_dist:
        ensight.curve.save("xy_data", "%s-distribution.exy" % (field)) # .exy file

    # Cleanup
    ensight.part.select_begin(new_parts)
    ensight.part.delete()
    ensight.variables.deactivate("elem_vol")
    ensight.variables.deactivate("Min")
    ensight.variables.deactivate("Max")
    ensight.variables.deactivate("Total_Volume")
    ensight.variables.deactivate("EleSize")
    ensight.variables.deactivate("sum_elesize")
    ensight.variables.deactivate("fractional_size")

def addplot(field, legend, save_data=True):
    print ("addplot for %s" % field)
    r1 = [1.930000e-02,
          2.510000e-02,
          3.160000e-02,
          3.900000e-02,
          4.720000e-02,
          5.620000e-02,
          6.650000e-02,
          7.810000e-02,
          9.090000e-02,
          1.048000e-01,
          1.198000e-01,
          1.359000e-01,
          1.531000e-01,
          1.704000e-01]
    r2 = [2.420000e-02,
          3.070000e-02,
          3.810000e-02,
          4.630000e-02,
          5.530000e-02,
          6.560000e-02,
          7.720000e-02,
          9.000000e-02,
          1.039000e-01,
          1.189000e-01,
          1.350000e-01,
          1.522000e-01,
          1.695000e-01,
          1.860000e-01]

    for i in xrange(14):
        print ("r1[%d]=%g, r2[%d]=%g" % (i, r1[i], i, r2[i]))

        #  Create Query
        ensight.query_ent_var.begin()
        ensight.query_ent_var.description("H%d" % (i+1))
        ensight.query_ent_var.query_type("generated")
        ensight.query_ent_var.number_of_sample_pts(10)
        ensight.query_ent_var.constrain("line_tool")
        ensight.query_ent_var.line_loc(1, r1[i], 0, 0)
        ensight.query_ent_var.line_loc(2, r2[i], 0, 0)
        ensight.query_ent_var.distance("x_from_origin")
        ensight.query_ent_var.variable_1(field)
        ensight.query_ent_var.generate_over("distance")
        ensight.query_ent_var.variable_2("DISTANCE")
        ensight.query_ent_var.end()
        ensight.query_ent_var.query()
        ensight.curve.select_begin(i)
        ensight.curve.assign("rescale", "H%d" % (i+1))
        ensight.curve.select_begin(0)
        if save_data:
            # ensight.curve.save("formatted","plot-format-H%d.dat" % (i+1) )
            ensight.curve.save("xy_data", "%s-format-H%d.exy" % (field, i+1)) # .exy file
            # ensight.curve.save("csv","plot-format-H%d.cvs" % (i+1) ) # .cvs file

    ensight.viewport.select_default()
    ensight.view_transf.function("global")

    # WARNING: following line includes OBSOLETE call (ensight.plot.new_plot).
    ensight.plot.new_plot()
    for i in xrange(14):
        ensight.curve.select_begin(i)
        ensight.plot.select_begin(i, 14)
        ensight.curve.assign("rescale")

        ensight.plot.select_begin(i)
        ensight.plot.visible("OFF")

    ensight.plot.select_begin(14)
    ensight.plot.plot_title(field)
    ensight.plot.axis_x_title("X [m]")
    ensight.plot.axis_y_title("[%s]" % legend)
    ensight.plot.axis_x_min(r1[0])
    ensight.plot.axis_x_max(r2[-1])

def image(field):
    ensight.anim_recorders.render_offscreen("ON")
    ensight.file.image_numpasses(4)
    ensight.file.image_stereo("current")
    ensight.file.image_screen_tiling(1, 1)
    ensight.file.image_format("png")
    ensight.file.image_format_options("Compression Default")
    ensight.file.image_transparent_back("ON")
    ensight.anim_recorders.render_offscreen("ON")
    ensight.file.image_numpasses(4)
    ensight.file.image_stereo("current")
    ensight.file.image_screen_tiling(1, 1)
    ensight.file.image_file("%s.png" % field)
    ensight.file.image_convert("ON")
    ensight.file.save_image()
    ensight.file.image_convert("OFF")

def main(argv):
    """
    "$RESULT/hifimagnet/CoupledCartModel/HL-31_p.json/P1N1_G1/np_32/exports/ensightgold/Electrics/Electrics.case"
    """

    print ("view.py")
    inputfile = 'Electrics.case'
    field = "potential"
    gfactor = 1
    dist  = False
    save_data = False
    save_image = False
    plot = False
    try:
        opts, args = getopt.getopt(argv, "hi:f:dspg", ["ifile=", "field=", "distribution", "save_data", "save_image", "plot", "gfactor="])
    except getopt.GetoptError:
        print ('view.py -i <inputfile> -f <field> -d -s')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('view.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-f", "--field"):
            field = arg
        elif opt in ("-p", "--plot"):
            plot = True
        elif opt in ("--distribution"):
            dist = True
        elif opt in ("-d", "--save_data"):
            save_data = True
        elif opt in ("-s", "--save_image"):
            save_image = True
        elif opt in ("-g", "--geom_factor"):
            gfactor = arg
        else:
            print ("view.py: error unknown option %s" % opt)

    # check if inputfile exist
    print ("Loading %s" % inputfile)
    print ("plot=", plot)
    print ("distribution", dist)
    print ("save_data=", save_data)
    print ("save_image=", save_image)
    print ("gfactor=", gfactor)

    load(inputfile)
    fields = getfields()
    print ("fields=", fields)
    if not field in fields:
        print ("Unsupported field: %s" % field)
        return 1

    # Eventually display "displaced" geometry
    if "elasticity_displacement" in fields:
        ensight.part.displace_by("elasticity_displacement")
        ensight.part.modify_end()
        ensight.part.select_all()
        ensight.part.modify_begin()
        ensight.part.displace_factor(gfactor)
        ensight.part.modify_end()
        
    if dist:
        distribution(field, 100, True)

    # Get stats
    stats(field)

    # Get View
    nfield, nlegend = view(field)

    if plot:
        addplot(nfield, nlegend, save_data)
    if save_image:
        image(nfield)

# if __name__ == "__main__":
print ("Running view %s" % sys.argv[1:])
main(sys.argv[1:])
