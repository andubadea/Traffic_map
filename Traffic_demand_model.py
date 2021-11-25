from Create_distributioncenter_Layer import Create_distributioncenter_layer
from Create_vertiport_layer import Create_vertiport_layer
from Node_coupling import Node_coupling
from Distribute_demand import Distribute_demand
from Loitering_missions import Loitering_missions
from multiprocessing import Pool as ThreadPool


list_of_demands = ['very_low','low', 'medium', 'high', 'ultra']
list_of_Dcenter_proportions = [0.40, 0.50, 0.60, 0.70, 0.80]
list_of_loitering_missions_number = [5, 6, 7, 8, 9]                     #set them accordingly for the demandlevels in this order: ['very_low', 'low', 'medium', 'high', 'ultra']

##Fixed variables distribute demand:
Number_of_samples = 9                       #amount of samples that are created with the exact same parameters
timesteps = 3600                            #amount of seconds in which flights are distributed
#Percentage_Dcenters = 0.80                 #proportion of vertiport demand that will come from distribution centers (taken from list)
Percentage_closest_Dcenters = 0.80          #proportion of vertiport demand that will come from the closest distribution centers
Number_of_Dcenters_per_vertiport = 5        #amount of distribution centers that are considered closest
Percentage_known_flights = 0.80             #percentage of all flights that are revealed at 00:00:00
Percentage_emergency_flights = 0.002         #percentage of the flights, that are not revealed at the start, that are revealed 1 minute in advance instead of 10 minutes
ac_types= ['MP20', 'MP30']

#input loitering
negative_time_margin = 120                  #seconds before departure from when the loiter missions start
positive_time_margin = 600                  #seconds after departure until when the loiter missions last (since the arrival time is unknown)
loiter_area_side = 300                      #meter: square 500 by 500 meter
#number_of_loitering_missions = 5           #(taken from list)
asd = []

input_arr = []
for demandlevel in range(len(list_of_demands)):
    for proportion in list_of_Dcenter_proportions:
        for sample in range(Number_of_samples):
            input_arr.append([demandlevel,proportion,sample])

def calculate_intention(variables):
    demandlevel,proportion,sample = variables
    traffic_level = list_of_demands[demandlevel]
    number_of_loitering_missions = list_of_loitering_missions_number[demandlevel]
    Percentage_Dcenters = proportion
    
    Distribution_centers_locations = Create_distributioncenter_layer()
    
    Vertiport_locations = Create_vertiport_layer(traffic_level)
    
    Distribution_centers_df, Vertiports_df = Node_coupling(Distribution_centers_locations, 
                                                           Vertiport_locations)
    
    flight_schedule_df = Distribute_demand(timesteps, Percentage_Dcenters, Percentage_closest_Dcenters, 
                      Number_of_Dcenters_per_vertiport, Percentage_known_flights, 
                      Percentage_emergency_flights, ac_types,
                      Distribution_centers_df, Vertiports_df)
    
    Loitering_missions(traffic_level, Percentage_Dcenters, negative_time_margin, 
                       positive_time_margin, loiter_area_side, number_of_loitering_missions, 
                       sample, flight_schedule_df, Distribution_centers_df)
    return

def main():
    calculate_intention(input_arr[0])
    # pool = ThreadPool(32)
    # results = pool.map(calculate_intention, input_arr)
    # pool.close()

if __name__ == '__main__':
    main()

# for demandlevel in range(len(list_of_demands)):
#     traffic_level = list_of_demands[demandlevel]
#     number_of_loitering_missions = list_of_loitering_missions_number[demandlevel]
#     for proportion in list_of_Dcenter_proportions:
#         Percentage_Dcenters = proportion
        
#         for sample in range(Number_of_samples):
            
#             Distribution_centers_locations = Create_distributioncenter_layer()
            
#             Vertiport_locations = Create_vertiport_layer(traffic_level)
            
#             Distribution_centers_df, Vertiports_df = Node_coupling(Distribution_centers_locations, 
#                                                                    Vertiport_locations)
            
#             flight_schedule_df = Distribute_demand(timesteps, Percentage_Dcenters, Percentage_closest_Dcenters, 
#                               Number_of_Dcenters_per_vertiport, Percentage_known_flights, 
#                               Percentage_emergency_flights, ac_types,
#                               Distribution_centers_df, Vertiports_df)
            
#             Loitering_missions(traffic_level, Percentage_Dcenters, negative_time_margin, 
#                                positive_time_margin, loiter_area_side, number_of_loitering_missions, 
#                                sample, flight_schedule_df, Distribution_centers_df)

































#Reveal time
    #1. Part of the flights (60%) is known at 00:00:00
    #1. Function of departure time (10-15 minutes before departure)
    #2. Emergency flights (1 minute before departure)    
#Drone Type
    #1. 3 types (20, 25 and 30 knots)
    #2. Equal proportion
#Priority (perhaps based on distance) (higher is more important)
    #1. 3 Levels and a 4th for emergency flights 
    #   food local deliveries more important
    #   loitering more important
    #   Emergency = 4
    #   Loitering = 3
    #   Vertirport to Vertiport = 2
    #   Dcenter to Vertiport = 1    
#loitering:
    #1. Needs to be destined in constrained airpsace
    #2. Needs to be destined not in range of Dcenter
    #3. Choose random


#add new center_points 
#fix loitering N per Traffic level
#append to flight intention start time, duration, polygon
#repeat nine times 
#Document, more comments/report
#Slides M2 meeting: dont explain all the variabels. But more inro the demand level literature Aprrox: 3/4 slides
#Report 
















