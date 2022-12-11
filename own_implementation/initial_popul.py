# This file defines functions used in the section "2) Initial Population:"

# NOTICE that this function requires the pre-existence of variable ing_list. See "support_for_initial_population.ipynb" to build this.
def prep_ratio(ing,ing_list,agroup_x_ing):
    """
    returns the ratio of the number of prep actions and the number of heating actions historically applied to an ingredient
    """
    if ing in ing_list:
        idx = ing_list.index(ing)
        if round(agroup_x_ing[2,idx]) == 0:
            return 0
        if round(agroup_x_ing[0,idx]) == 0:
            return 1
        return agroup_x_ing[2,idx] / agroup_x_ing[0,idx]
    else:
        print(ing+' is an unfamiliar ingredient. MealMaker is proceeding anyway.')
        return 0

def rand_prep(ing,ing_list,agroup_x_ing,prep_thresh):
    """
    returns a boolean value (with randomness) of whether ing should be prepared. If in doubt, set prep_thresh = 0.35
    """
    return prep_ratio(ing,ing_list,agroup_x_ing) > np.random.normal(prep_thresh,0.1)


def heat_ratio(ing,ing_list,agroup_x_ing):
    """
    returns the ratio of the number of prep actions and the number of heating actions historically applied to an ingredient
    """
    if ing in ing_list:
        idx = ing_list.index(ing)
        if round(agroup_x_ing[2,idx]) == 0:
            return 1
        if round(agroup_x_ing[0,idx]) == 0:
            return 0
        ratio = 1 - agroup_x_ing[2,idx] / agroup_x_ing[0,idx]
        return ratio
    else:
        print(ing+' is an unfamiliar ingredient. MealMaker is proceeding anyway.')
        return 0

def rand_heat(ing,ing_list,agroup_x_ing,heat_thresh):
    """
    returns a boolean value (with randomness) of whether ing should be prepared. If in doubt, set heat_thresh = 0.65
    """
    return heat_ratio(ing,ing_list,agroup_x_ing) > np.random.normal(prep_thresh,0.15)

