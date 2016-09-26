#!/usr/bin/env python
# encoding: utf-8

r"""
Shallow water flow
==================

Solve the one-dimensional shallow water equations including bathymetry:

.. math::
    h_t + (hu)_x & = 0 \\
    (hu)_t + (hu^2 + \frac{1}{2}gh^2)_x & = -g h b_x.

Here h is the depth, u is the velocity, g is the gravitational constant, and b
the bathymetry.  
"""

import numpy
from clawpack import riemann

def setup(kernel_language='Python',use_petsc=False, outdir='./_output', solver_type='classic'):

    if use_petsc:
        import clawpack.petclaw as pyclaw
    else:
        from clawpack import pyclaw

    solver = pyclaw.ClawSolver1D(riemann.shallow_1D_py.shallow_fwave_1d)
    solver.limiters = pyclaw.limiters.tvd.vanleer
    solver.kernel_language = "Python"
    solver.fwave = True
    solver.num_waves = 2
    solver.num_eqn = 2
    solver.bc_lower[0] = pyclaw.BC.wall
    solver.bc_upper[0] = pyclaw.BC.wall
    solver.aux_bc_lower[0] = pyclaw.BC.wall
    solver.aux_bc_upper[0] = pyclaw.BC.wall
    solver.step_source = stepSource

    # x_star = numpy.sqrt(55.0 / 1e-2)
    x_star = 85
    xlower = -x_star
    xupper = x_star
    x = pyclaw.Dimension( xlower, xupper, 500, name='x')
    domain = pyclaw.Domain(x)
    state = pyclaw.State(domain, 2, 1)

    # Gravitational constant
    state.problem_data['grav'] = 9.8
    state.problem_data['sea_level'] = 0.0
    
    xc = state.grid.x.centers
    # state.aux[0, :] = 0.8 * numpy.exp(-xc**2 / 0.2**2) - 1.0
    x_star = numpy.sqrt(80.0 / 1e-2) - 1.0
    state.aux[0, :] = 1.e-2*(xc**2) - 80
    ze = -((xc)**2)/10
    state.q[0, :] = numpy.where(ze>-10., 40.e0*numpy.exp(ze) - state.aux[0, :], numpy.where(state.aux[0, :]<=0, -state.aux[0, :], 0.))
    state.q[1, :] = 0.0

    claw = pyclaw.Controller()
    claw.keep_copy = True
    claw.tfinal = 8.0
    claw.output_style = 1
    claw.num_output_times = 25
    claw.solution = pyclaw.Solution(state, domain)
    claw.solver = solver
    claw.setplot = setplot
    claw.write_aux_init = True

    if outdir is not None:
        claw.outdir = outdir
    else:
        claw.output_format = None


    return claw


#--------------------------
def setplot(plotdata):
#--------------------------
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of visclaw.data.ClawPlotData.
    Output: a modified version of plotdata.
    """ 
    plotdata.clearfigures()  # clear any old figures,axes,items data

    # Plot variables
    def bathy(current_data):
        return current_data.aux[0, :]

    def eta(current_data):
        return current_data.q[0, :] + bathy(current_data)

    def velocity(current_data):
        return current_data.q[1, :] / current_data.q[0, :]

    rgb_converter = lambda triple: [float(rgb) / 255.0 for rgb in triple]

    # Figure for depth
    plotfigure = plotdata.new_plotfigure(name='Depth', figno=0)

    # Axes for water depth
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = [-100.0, 100.0]
    plotaxes.ylimits = [-100.0, 80.0]
    plotaxes.title = 'Water Depth'
    plotaxes.axescmd = 'subplot(211)'

    plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between')
    plotitem.plot_var = eta
    plotitem.plot_var2 = bathy
    plotitem.color = rgb_converter((67,183,219))

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = bathy
    plotitem.color = 'k'

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = eta
    plotitem.color = 'k'

    # Axes for velocity
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(212)'
    plotaxes.xlimits = [-85.0, 85.0]
    plotaxes.ylimits = [-5.0, 5.0]
    plotaxes.title = 'Velocity'

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = velocity
    plotitem.color = 'b'
    plotitem.kwargs = {'linewidth':3}
    
    return plotdata

def stepSource(solver,state,dt):
    q = state.q
    xc = state.grid.p_centers[0]

    ndim = 2
    qstar1 = q[0,:] - 0.5*dt*(ndim-1)/xc * q[1,:]
    qstar2 = q[1,:] - 0.5*dt*(ndim-1)/xc * q[1,:]**2 / q[0,:]

    q[0,:] -= dt*(ndim-1)/xc * qstar2
    q[1,:] -= dt*(ndim-1)/xc * qstar2**2 / qstar1

if __name__=="__main__":
    from clawpack.pyclaw.util import run_app_from_main
    output = run_app_from_main(setup,setplot)
