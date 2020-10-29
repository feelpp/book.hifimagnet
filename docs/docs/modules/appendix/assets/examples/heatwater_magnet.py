#!/usr/bin/env python
# encoding: utf-8

r"""
One-dimensional advection
=========================

Solve the linear advection equation:

.. math:: 
    q_t + u q_x = 0.

Here q is the density of some conserved quantity and u is the velocity.

The initial condition is a Gaussian and the boundary conditions are periodic.
The final solution is identical to the initial data because the wave has
crossed the domain exactly once.

L=2*h with h=1.577944e-01 (from HL-31.d par ex - lattest helix)
rho=st.steam_pT(pascal, kelvin).rho
cp = st.steam_pT(pascal, kelvin).cp

Flow1: l/s
Section= (from HL-31.d par ex)
Tin1
U1: sum(Icoil1,...,Icoil7)
Power1: U1*(Idcct1+Idcct2)

psi: Power1*(x+h)/(2*h)

x0 = -1.5*h
x1 = 2*h
x = pyclaw.Dimension(x0,x1,nx,name='x')
psi[0,:] = [ Power1*(xi+h)/(2*h) if abs(xi) <= h else 0 for xi in xc]

"Sh0":"262.292e-6",	
"Sh1":"139.392e-6",	
"Sh2":"176.149e-6",	
"Sh3":"217.995e-6",	
"Sh4":"264.365e-6",	
"Sh5":"315.259e-6",	
"Sh6":"373.504e-6",	
"Sh7":"439.1e-6",	
"Sh8":"511.483e-6",	
"Sh9":"590.085e-6",	
"Sh10":"674.908e-6",	
"Sh11":"765.952e-6",	
"Sh12":"863.215e-6",	
"Sh13":"961.045e-6",	
"Sh14":"292.364e-6"	

"""
from __future__ import absolute_import
import numpy as np
from clawpack import riemann

import freesteam as st

# see http://www.clawpack.org/pyclaw/problem.html#adding-source-terms
def step_Euler_radial(solver,state,dt):
    q   = state.q
    aux = state.aux
    xc = state.grid.x.centers

    rhocp = state.problem_data['rhocp']
    L = state.problem_data['L']
    Power1= state.problem_data['Power1']
    Q = state.problem_data['Q']
    
    psi = np.empty(q.shape)
    psi[0,:] = [ Q if abs(xi) <= L else 0 for xi in xc]
    # psi[0,:] = [ Q*(xi+L)/(2*L) if abs(xi) <= L else 0 for xi in xc]
    
    q[0,:] = q[0,:] + dt * psi[0,:]

def dq_Euler_radial(solver,state,dt):
    q   = state.q
    aux = state.aux
    xc = state.grid.x.centers

    rhocp = state.problem_data['rhocp']
    L = state.problem_data['L']
    Q = state.problem_data['Q']

    psi = np.empty(q.shape)
    psi[0,:] = [ Q if abs(xi) <= L else 0 for xi in xc]
    # psi[0,:] = [ Q*(xi+L)/(2*L) if abs(xi) <= L else 0 for xi in xc]

    dq = np.empty(q.shape)
    dq[0,:] = + dt * psi[0,:]
    
    return dq

def setup(num_output_times=10, tfinal=3, nx=200, kernel_language='Python', use_petsc=False, solver_type='classic', weno_order=5, 
          time_integrator='SSP104', outdir='./_output'):

    if use_petsc:
        import clawpack.petclaw as pyclaw
    else:
        from clawpack import pyclaw

    if kernel_language == 'Fortran':
        riemann_solver = riemann.advection_1D
    elif kernel_language == 'Python':
        riemann_solver = riemann.advection_1D_py.advection_1D
            
    if solver_type=='classic':
        solver = pyclaw.ClawSolver1D(riemann_solver)
        solver.step_source=step_Euler_radial
        solver.dt_variable=True
        solver.cfl_desired = 0.9
        solver.max_steps = 50000
    elif solver_type=='sharpclaw':
        solver = pyclaw.SharpClawSolver1D(riemann_solver)
        solver.dq_src=dq_Euler_radial
        solver.weno_order = weno_order
        solver.dt_variable=True
        solver.cfl_desired = 0.9
        solver.time_integrator = time_integrator
        solver.max_steps = 50000
        if time_integrator == 'SSPLMMk3':
            solver.lmm_steps = 5
            solver.check_lmm_cond = True
    else: raise Exception('Unrecognized value of solver_type.')

    solver.kernel_language = kernel_language
    verbosity = 1
    total_steps = 30
    
    solver.bc_lower[0] = pyclaw.BC.extrap #periodic
    solver.bc_upper[0] = pyclaw.BC.extrap #periodic

    # x = pyclaw.Dimension(0.0,xl,nx,name='x')
    L = 1.577944e-01
    print ("L=", L)
    x0 = -1.5*L
    x1 = 4*L
    x = pyclaw.Dimension(x0,x1,nx,name='x')
    domain = pyclaw.Domain(x)
    state = pyclaw.State(domain,solver.num_eqn)

    Tin = 15
    rho = st.steam_pT(10 * 1e+5, Tin+273).rho
    cp = st.steam_pT(10 * 1e+5, Tin+273).cp
    print ("rho=", rho)
    print ("cp=", cp)
    print ("rhocp=", rho*cp)

    Flow = 140.e-3
    Section =  262.292e-6 \
	+ 139.392e-6 \
        + 176.149e-6 \
	+ 217.995e-6 \
	+ 264.365e-6 \
        + 315.259e-6 \
        + 373.504e-6 \
        + 439.1e-6 \
        + 511.483e-6 \
        + 590.085e-6 \
        + 674.908e-6 \
        + 765.952e-6 \
        + 863.215e-6 \
        + 961.045e-6 \
        + 292.364e-6
    print ("Section=", Section)

    Power1 = 12.5e+6
    print ("Power=", Power1)
    Qth = Power1 / (Section*(2*L))
    print ("delta T = Pe/(rho Cp Debit)=", Power1/(rho*cp*Flow))
    print ("Qth = Power / ( Section * (2*L) )=", Qth, "Qth/(rhocp)=", Qth/(rho*cp), "Q=", Qth/100.)
    u = Flow/Section
    print ("u = Flow / Section=", u, "u/rhocp=", u/(rho*cp))
    
    state.problem_data['rhocp'] = rho*cp  # Specific Heat
    state.problem_data['u'] = u  # Advection velocity
    state.problem_data['L'] = L  # Advection velocity
    state.problem_data['Power1'] = Power1  # Advection velocity
    state.problem_data['Q'] = Qth/(rho*cp)   # Advection velocity

    # Initial data
    xc = state.grid.x.centers
    state.q[0,:] = Tin

    claw = pyclaw.Controller()
    claw.keep_copy = True
    claw.solution = pyclaw.Solution(state,domain)
    claw.solver = solver

    if outdir is not None:
        claw.outdir = outdir
    else:
        claw.output_format = None

    claw.tfinal = tfinal
    claw.setplot = setplot
    claw.num_output_times = num_output_times

    return claw

def add_source(current_data):
    """ 
    Plot Qth using VisClaw.
    """ 
    from pylab import plot
    x = current_data.x
    t = current_data.t

    L = 1.577944e-01
    qsource = [ (xi+L)/(2*L) if abs(xi) <= L else 0 for xi in x]
    plot(x, qsource, 'r')
    
def setplot(plotdata):
    """ 
    Plot solution using VisClaw.
    """ 
    plotdata.clearfigures()  # clear any old figures,axes,items data

    plotfigure = plotdata.new_plotfigure(name='q', figno=1)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.ylimits = [10,40]
    plotaxes.title = 'q'

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
    plotitem.plotstyle = '-o'
    plotitem.color = 'b'
    plotitem.kwargs = {'linewidth':2,'markersize':5}
    
    # plotaxes.afteraxes = add_source

    return plotdata

 
if __name__=="__main__":
    from clawpack.pyclaw.util import run_app_from_main

    # load M9...txt
    # Create 
    output = run_app_from_main(setup,setplot)
