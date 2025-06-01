'''

Author : yunanhou

Date : 2023/12/02

Function : The orbits within a shell are derived based on a clustering algorithm and the satellites are assigned to
           these orbits.

           Specifically, before executing this script, the corresponding relationship between satellites and shells has
           been established, but the relationship between satellites and orbit points has not yet been established. The
           function of this script is to establish the corresponding relationship between satellites and orbit.

           The main function of the script needs to pass in a shell class object, and then cluster the raan of each
           satellite in the shell object to obtain several orbits, and then assign all satellites in the shell to these
           orbits.

'''
import jenkspy
import src.TLE_constellation.constellation_entity.orbit as ORBIT
import matplotlib.pyplot as plt

# Parameter :
# shells : a collection of shell objects that have established corresponding relationships
# Return Value :
# after the function is executed, the mapping relationship between satellite, orbit, and shell has been established
# without any return value.
# def satellite_to_orbit_mapping(shells):
#     for sh in shells:
#         # extract the raan of all satellites in sh
#         raans = []
#         for sat in sh.satellites:
#             raans.append(sat.tle_json["RA_OF_ASC_NODE"])
#         raans = sorted(raans)

#         plt.plot(raans)
#         plt.ylabel('RAANS')
#         plt.show()

#         orbits_number = int(input('\t\t\tPlease enter the number of orbits (integer) based on the raan distribution result of '
#                               'the line chart : '))
#         breaks = jenkspy.jenks_breaks(values = raans, n_classes = orbits_number)
#         orbit_raans = [(breaks[i], breaks[i + 1]) for i in range(len(breaks) - 1)]
#         for ra_index, ra in enumerate(orbit_raans):
#             lower_bound = ra[0]
#             upper_bound = ra[1]
#             orbit = ORBIT.orbit(shell=sh , raan_lower_bound=lower_bound , raan_upper_bound=upper_bound)
#             for sat in sh.satellites:
#                 if ra_index > 0:
#                     if sat.tle_json["RA_OF_ASC_NODE"] > lower_bound and sat.tle_json["RA_OF_ASC_NODE"] <= upper_bound:
#                         sat.orbit = orbit
#                         orbit.satellites.append(sat)
#                 if ra_index == 0:
#                     if sat.tle_json["RA_OF_ASC_NODE"] >= lower_bound and sat.tle_json["RA_OF_ASC_NODE"] <= upper_bound:
#                         sat.orbit = orbit
#                         orbit.satellites.append(sat)

#             sh.orbits.append(orbit)


# TODO(bxhu): Add a predefined orbits number for each shell
# NOTE: https://github.com/SpaceNetLab/StarPerf_Simulator/issues/6
def satellite_to_orbit_mapping(shells):
    predefined_orbits_numbers = [1, 8, 5, 21, 72, 28, 24, 72]
    
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()
    
    for shell_idx, sh in enumerate(shells):
        orbits_number = predefined_orbits_numbers[shell_idx] if shell_idx < len(predefined_orbits_numbers) else 1
        
        raans = []
        for sat in sh.satellites:
            raans.append(sat.tle_json["RA_OF_ASC_NODE"])
        raans = sorted(raans)

        axes[shell_idx].plot(raans)
        axes[shell_idx].set_ylabel('RAANS')
        axes[shell_idx].set_title(f'Shell {shell_idx}: {orbits_number} orbits')
        
        print(f'\t\t\tShell {shell_idx}: Using {orbits_number} orbits (predefined)')
        
        breaks = jenkspy.jenks_breaks(values=raans, n_classes=orbits_number)
        orbit_raans = [(breaks[i], breaks[i + 1]) for i in range(len(breaks) - 1)]
        for ra_index, ra in enumerate(orbit_raans):
            lower_bound = ra[0]
            upper_bound = ra[1]
            orbit = ORBIT.orbit(shell=sh, raan_lower_bound=lower_bound, raan_upper_bound=upper_bound)
            for sat in sh.satellites:
                if ra_index > 0:
                    if sat.tle_json["RA_OF_ASC_NODE"] > lower_bound and sat.tle_json["RA_OF_ASC_NODE"] <= upper_bound:
                        sat.orbit = orbit
                        orbit.satellites.append(sat)
                if ra_index == 0:
                    if sat.tle_json["RA_OF_ASC_NODE"] >= lower_bound and sat.tle_json["RA_OF_ASC_NODE"] <= upper_bound:
                        sat.orbit = orbit
                        orbit.satellites.append(sat)
            sh.orbits.append(orbit)
    
    plt.tight_layout()
    plt.show()