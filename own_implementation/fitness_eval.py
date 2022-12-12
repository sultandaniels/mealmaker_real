# This module defines functions for section "4) Fitness Evaluation" of the paper

import initial_popul as pop

def s_heat(B_h,ing,ing_list,agroup_x_ing,thresh_heat,eps_heat):
    """
    returns a list of of booleans of the same length as B_h; when in doubt, set thresh_heat=0.65 and eps_heat=0.1
    """
    return [0 if pop.heat_ratio(ing,ing_list,agroup_x_ing)>thresh_heat+eps_heat and not bit 
            else 0 if pop.heat_ratio(ing,ing_list,agroup_x_ing)<thresh_heat-eps_heat and bit 
            else 1 for bit in B_h]

def s_prep(B_p,ing,ing_list,agroup_x_ing,thresh_prep,eps_prep):
    """
    returns a list of of booleans of the same length as B_p; when in doubt, set thresh_prep=0.35 and eps_prep=0.1
    """
    return [0 if pop.prep_ratio(ing,ing_list,agroup_x_ing)>thresh_prep+eps_prep and not bit 
        else 0 if pop.prep_ratio(ing,ing_list,agroup_x_ing)<thresh_prep-eps_prep and bit 
        else 1 for bit in B_p]


def prepare_score(ingredient:Ingredient):
    ing_str = ingredient._base_ingredient
    
    g_ing = to_grouped_ingredient(ingredient)
    
    ratio = prepare_ratio(ing_str)
    
    if ratio > PREPARE_RATIO_THRESHOLD + PREPARE_SCORE_EPS:
        if 'prepare' not in g_ing._action_set:
            return 0
    
    if ratio < PREPARE_RATIO_THRESHOLD - PREPARE_SCORE_EPS:
        if 'prepare' in g_ing._action_set:
            return 0
    
    return 1

def heat_score(ingredient:Ingredient):
    ing_str = ingredient._base_ingredient
    
    g_ing = to_grouped_ingredient(ingredient)
    
    ratio = heat_ratio(ing_str)
    
    if ratio > HEAT_RATIO_THRESHOLD + HEAT_SCORE_EPS:
        if 'heat' not in g_ing._action_set:
            return 0
    
    if ratio < HEAT_RATIO_THRESHOLD - HEAT_SCORE_EPS:
        if 'heat' in g_ing._action_set:
            return 0
    
    return 1


