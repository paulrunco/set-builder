import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def generate_sets(inventory_report, product, order_target_lbs, set_target_lbs, set_min_lbs):

    # Read the inventory report
    inventory = pd.read_excel(inventory_report, 'WebInv')
    inventory['Product'] = inventory['Product'].astype(str)
    inventory['Set'] = "" # Add set column to product table

    # Filter to the parent material of interest
    rolls = inventory.loc[inventory['Product'] == str(product)]

    rolls['Exp Date'] = rolls['Expiration Date'].dt.date

    order_weight_lbs = 0
    set_number = 1 # starting set number
    while order_weight_lbs < order_target_lbs:
        set_weight_lbs = 0
        rolls = rolls.sort_values(by=['Exp Date', 'Weight (Lbs)'], ascending=[True, False])
        # TODO filter to top N lots only

        for i, row in rolls.loc[rolls['Set'] == ''].iterrows():
            if set_weight_lbs + row['Weight (Lbs)'] < set_target_lbs:
                set_weight_lbs += row['Weight (Lbs)']
                rolls.at[i, 'Set'] = set_number
            else:
                # Checking  remaining rolls to see which brings the set closest to target with the existing rolls unchanged
                last_rolls = rolls.loc[rolls['Set'] == '']
                last_rolls['Remainder'] = set_target_lbs - set_weight_lbs - last_rolls['Weight (Lbs)']
                last_roll = last_rolls.loc[last_rolls['Remainder'] >= 0]['Remainder'].idxmin()
                rolls.at[last_roll, 'Set'] = set_number
                set_weight_lbs += rolls.at[last_roll, 'Weight (Lbs)'] # add last roll weight to set weight
                
                break

        order_weight_lbs += set_weight_lbs
        set_number += 1

        # Check if another set, even at minimum weight would overweight the order
        if order_weight_lbs + set_min_lbs > order_target_lbs:
            break
    
    print(f'Order weight: {order_weight_lbs} lbs of {order_target_lbs}')
    print(rolls.groupby(['Set']).sum()['Weight (Lbs)'])

    return rolls

## TODO
# def optimize_remainder(rolls, set_number):
#     #Optimize existing rolls by removing heaviest roll in favor of another
#     set_rolls = rolls.loc[rolls['Set'] == set_number]
#     test_rolls = rolls.loc[rolls['Set'] == '']
#     remainder = set_target_lbs - set_rolls['Weight (Lbs)'].sum() # starting remainder
#     print(f'Starting remainder: {remainder}')
#     for i, row in set_rolls.iterrows():
#         print(i)
#         test_weight = set_rolls['Weight (Lbs)'].sum() - row['Weight (Lbs)'] # weight of set with roll removed
#         test_rolls['Remainder'] = set_target_lbs - (test_weight  + test_rolls['Weight (Lbs)'])
#         print(test_rolls)

    # TODO optimize set assignments to minimize remainder to set weight target
    
    # TODO Repeat until no more sets can be made with selected lots OR order qty is reached OR max number of lots is reached

    # TODO Repeat until order qty is reached OR material is exhausted


