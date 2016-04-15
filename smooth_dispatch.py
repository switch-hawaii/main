"""Perform lexicographic optimization to minimize "burning off" or circulating renewable power 
during curtailment periods and to smooth out demand-side actions used to balance the system."""
# TODO: finish writing this and test its performance (may fail to converge with such complex 
# and tight constraints; may be possible to improve it by giving a little slack on them.)

# TODO: fix all variables except the ones here and others that are not in the main objective function.
# or just fix everything except transmission dispatch, generator dispatch and these.
# or keep lists of "build variables" and "operate variables" and freeze all the build variables.

# TODO: maybe switch to simple sum of squared values?
def var(comp):
    n = len(comp)
    var = (
        sum(comp[i] * comp[i] for i in comp) / n
        -
        (sum(comp[i] for i in comp) / n) * (sum(comp[i] for i in comp) / n)
    )
    return var

def define_components(m):
    # add an alternative objective expression that minimizes spurious losses
    # (e.g., due to running excess renewable power through the transmission network
    # when it has 0 cost). Note: we can't deal with the odd situation where more
    # renewables are "burned off" in order to boost their share of production and
    # meet the RPS.
    m.TotalProduction = Expression(rule=lambda m:
        sum(
            getattr(m, component)[lz, t] 
                for lz in m.LOAD_ZONES 
                    for t in m.TIMEPOINTS 
                        for component in m.LZ_Energy_Components_Produce)
    )
    # minimize production (i.e., maximize curtailment / minimize losses)
    m.Minimize_Excess_Production = Objective(sense=minimize, rule=lambda m:

    # smooth out various energy-consumption variables that may all 
    # be on the margin at the same time (otherwise they can be arbitrarily spiky)
    def FreeVariableVariance_rule(m):
        total_var = 0.0
        smoothable_vars = [
            "DemandResponse", "ChargeEVs", "ChargeBattery", "RunElectrolyzerMW", "LiquifyHydrogenMW"
        ]
        for comp in smoothable_vars:
            if hasattr(m, comp):
                total_var += var(getattr(m, comp))
                print "Will smooth {}.".format(comp)
    m.FreeVariableVariance = Expression(rule=FreeVariableVariance_rule, sense=minimize)

    # targets to use for lexicographic optimization
    m.min_TotalCost = Param(default=float("inf"), mutable=True)
    m.min_TotalProduction = Param(default=float("inf"), mutable=True)
    
    # 
def pre_iterate(m):
    # iteration 0: deactivate all special objectives and constraints
    # iteration 1: activate Minimize_Excess_Production objective, deactivate TotalCost objective, activate min_TotalCost constraint
    # iteration 2: deactivate Minimize_Excess_Production objective; activate Minimize_FreeVariableVariance objective and min_TotalProduction constraint
    
def post_iterate(m):
    # TODO: write this
    # iteration 0: cache duals
    old_duals = [
        (z, t, m.dual[m.Energy_Balance[z, t]])
            for z in m.LOAD_ZONES
                for t in m.TIMEPOINTS]
    # iteration 2: restore TotalCost objective; restore original duals, report convergence
    
def old_code():    
            fix_obj_expression(switch_instance.Minimize_System_Cost)
            switch_instance.Minimize_System_Cost.deactivate()
            switch_instance.Smooth_Free_Variables.activate()
            switch_instance.preprocess()
            log("smoothing free variables...\n")
            results = _solve(switch_instance)
            # restore hourly duals from the original solution
            for (z, t, d) in old_duals:
               switch_instance.dual[switch_instance.Energy_Balance[z, t]] = d
            # unfix the variables
            fix_obj_expression(switch_instance.Minimize_System_Cost, False)
            log("finished smoothing free variables; "); toc()


        if hasattr(switch_instance, "ChargeBattery"):
            double_charge = [
                (
                    z, t, 
                    switch_instance.ChargeBattery[z, t].value, 
                    switch_instance.DischargeBattery[z, t].value
                ) 
                    for z in switch_instance.LOAD_ZONES 
                        for t in switch_instance.TIMEPOINTS 
                            if switch_instance.ChargeBattery[z, t].value > 0 
                                and switch_instance.DischargeBattery[z, t].value > 0
            ]
            if len(double_charge) > 0:
                print ""
                print "WARNING: batteries are simultaneously charged and discharged in some hours."
                print "This is usually done to relax the biofuel limit."
                for (z, t, c, d) in double_charge:
                    print 'ChargeBattery[{z}, {t}]={c}, DischargeBattery[{z}, {t}]={d}'.format(
                        z=z, t=switch_instance.tp_timestamp[t],
                        c=c, d=d
                    )

def fix_obj_expression(e, status=True):
    """Recursively fix all variables included in an objective expression."""
    if hasattr(e, 'fixed'):
        e.fixed = status      # see p. 171 of the Pyomo book
    elif hasattr(e, '_numerator'):
        for e2 in e._numerator:
            fix_obj_expression(e2, status)
        for e2 in e._denominator:
            fix_obj_expression(e2, status)
    elif hasattr(e, '_args'):
        for e2 in e._args:
            fix_obj_expression(e2, status)
    elif hasattr(e, 'expr'):
        fix_obj_expression(e.expr, status)
    elif hasattr(e, 'is_constant') and e.is_constant():
        pass    # numeric constant
    else:
        raise ValueError(
            'Expression {e} does not have an expr, fixed or _args property, ' +
            'so it cannot be fixed.'.format(e=e)
        )
