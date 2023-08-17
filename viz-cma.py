from ConfigSpace import ConfigurationSpace
from ConfigSpace.util import generate_grid
from ioh_xplainer import explainer
from modcma import ModularCMAES, Parameters
import numpy as np
import traceback

"""Attributes
----------
lambda_: int = None
    The number of offspring in the population
mu: int = None
    The number of parents in the population
sigma0: float = .5
    The initial value of sigma (step size)

"""
cs = ConfigurationSpace({
    'elitist' : [False, True], 
    'mirrored': ['mirrored pairwise', 'nan', 'mirrored'], 
    'base_sampler': ['sobol', 'gaussian', 'halton'], 
    'weights_option': ['default', 'equal', '1/2^lambda'], 
    'local_restart': ['nan', 'IPOP', 'BIPOP'], 
    'step_size_adaptation': ['csa', 'psr']
}) #20k+

steps_dict = {
}


def run_cma(func, config, budget, dim, *args, **kwargs):

    

    local_restart = config.get('local_restart')
    if config.get('local_restart') == 'nan':
        local_restart = None
    #mirrored
    mirrored = config.get('mirrored')
    if config.get('mirrored') == 'nan':
        mirrored = None
    

    elitist = bool(config.get('elitist'))
    if config.get('elitist')=="True":
        elitist = True
    if config.get('elitist')=="False":
        elitist = False

    item = {'elitist' : elitist, 
        'mirrored': mirrored, 
        'base_sampler': config.get('base_sampler'), 
        'weights_option': config.get('weights_option'), 
        'local_restart': local_restart
         }
    item['budget'] = int(budget)
    c = ModularCMAES(func, dim, **item)

    try:
        c.run()
        return []
    except Exception as e:
        print(f"Found target {func.state.current_best.y} target, but exception ({e}), so run failed")
        traceback.print_exc()
        print(item)
        return []

cma_explainer = explainer(run_cma, 
                 cs , 
                 algname="mod-cma",
                 dims = [5,30],#,10,40],#, 10, 20, 40  ,15,30
                 fids = np.arange(1,25), #,5
                 iids = [1,5], #,5 
                 reps = 3, #maybe later 10? = 11 days processing time
                 sampling_method = "grid",  #or random
                 grid_steps_dict = steps_dict,
                 sample_size = None,  #only used with random method
                 budget = 10000, #10000
                 seed = 1,
                 verbose = False)

#cma_explainer.run(paralell=True)
#cma_explainer.save_results("de_results_huge5d.pkl")


cma_explainer.load_results("cma_es.pkl")
#x = de_explainer.df[(de_explainer.df['fid'] == 1) & (de_explainer.df['dim'] == 5)][["F","CR","lambda_"]].to_numpy()

#y = de_explainer.df[(de_explainer.df['fid'] == 1) & (de_explainer.df['dim'] == 5)]["auc"].to_numpy()
#np.savetxt("sobol/x.csv", x)
#np.savetxt("sobol/y.csv", y)

cma_explainer.explain(file_prefix = "cma_img/img_", keep_order=True)