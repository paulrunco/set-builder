import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def generate_sets(
    inventory_report,
    finished,
    material, 
    order_target_lbs, 
    set_target_lbs, 
    set_min_lbs
    ):

    # Read the inventory report
    inventory = pd.read_excel(inventory_report, 'WebInv')
    inventory['Product'] = inventory['Product'].astype(str)
    inventory['Set'] = "" # Add set column to product table

    # Filter to the parent material of interest
    rolls = inventory.loc[inventory['Product'] == str(material)]

    # Check if there is enough material in inventory to meet order demand
    if rolls['Weight (Lbs)'].sum() < order_target_lbs - set_min_lbs:
        error = ValueError()
        error.message = "Insufficient inventory to meet order demand."
        raise error

    rolls['Exp Date'] = rolls['Expiration Date'].dt.date # convert dates
    rolls = rolls.sort_values(by=['Exp Date', 'Weight (Lbs)'], ascending=[True, False])
    rolls['DaysToExp'] = rolls['Expiration Date'] - pd.to_datetime('now') # days to expiration

    order_weight_lbs = 0
    set_number = 1 # starting set number
    while order_weight_lbs < order_target_lbs - set_min_lbs:

        set_weight_lbs = 0
        set_lots = []
        while set_weight_lbs < set_min_lbs:

            pick_rolls = rolls.loc[rolls['Set'] == ''] # only unassigned rolls
            pick_rolls['Remainder'] = set_target_lbs - set_weight_lbs - pick_rolls['Weight (Lbs)'] # calculate remainder
            pick_rolls = pick_rolls.loc[pick_rolls['Remainder'] >= 0] # don't go over set_target_lbs

            pick_rolls['Score'] = (pick_rolls['Remainder']/pick_rolls['Remainder'].max() + pick_rolls['DaysToExp']/pick_rolls['DaysToExp'].max())/2

            if len(set_lots) == 2:
                pick_rolls = pick_rolls.loc[pick_rolls['Batch'].isin(set_lots)] # limit to N lots per set

            if pick_rolls.shape[0] > 0: # any eligible rolls?

                pick = pick_rolls['Score'].idxmin() # pick lowest scoring roll roll
                rolls.at[pick, 'Set'] = set_number
                set_weight_lbs += rolls.at[pick, 'Weight (Lbs)'] # add last roll weight to set weight
                
                if len(set_lots) < 2: # add lots to set-lot-list if needed
                    batch = rolls.at[pick, 'Batch']
                    if batch not in set_lots:
                        set_lots.append(batch)
            else: 
                # Set cannot be made with first two lots so walk back the first lot and try again
                undo = set_lots.pop(1) # keep oldest lot by default
                print(f'Unable to complete set with first two lots, resetting lot {undo}')

                subtract_weight =  rolls.loc[rolls['Batch'] == undo]['Weight (Lbs)'].sum()
                rolls.loc[rolls['Batch'] == undo, 'Set'] = 0
                set_weight_lbs -= subtract_weight # 

                pass
     
            print(f'Order weight: {order_weight_lbs} lbs of {order_target_lbs}')
            print(rolls.groupby(['Set']).sum()['Weight (Lbs)'])

        set_number += 1
        order_weight_lbs += set_weight_lbs  
            
    rolls.loc[rolls['Set'] == 0, 'Set'] = '' # reset undersized lots that were set aside

    with pd.ExcelWriter(
        inventory_report,
        mode="a",
        if_sheet_exists="overlay"
    ) as writer:
        rolls.to_excel(
            writer,
            sheet_name=f'{material}->{finished}',
            header=True,
            index=False
        )

    return rolls


