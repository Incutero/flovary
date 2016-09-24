import heapq

class Avatar(object):
    """Represents an avatar.

    Args:
        energy (float):  Total energy capacity of the Avatar.
        efficiency (float): How many kilometers can be traveled per unit of energy.
    """
    def __init__(self, energy, efficiency):
        self.energy = energy
        self.efficiency = efficiency


class Station(object):
    """Represents an station run by the Na'vi.

    Args:
        position (float): Number of kilometers from the start.
        cost (float): Cost per unit of energy charged by the station.
    """
    def __init__(self, position, cost):
        self.position = position
        self.cost = cost

def travel_cost(avatar, distance, stations):
    """Get the travel cost for an `avatar`.

    The travel cost for an `avatar` is based on the stations that the `avatar`
    stops at during the trip to sleep and re-energize. Stations charge a fixed
    fee of 2.0 and based on amount of energy regained.

    Args:
        avatar (Avatar): Avatar making the trip.
        distance (float): Total distance in kilometers to the destination
            biosphere.
        stations (list<Station>): Stations between the starting and destination
            biospheres.
    """
    start = Station(0, 0)
    end = Station(distance, 0)
    stations = [start] + stations + [end]
    avatarRange = avatar.efficiency * avatar.energy
    
    # Initialize cost of each vertex to infinity
    cost = {}
    for station in stations:
        cost[station] = float('inf')
    cost[start] = 0
    
    # Generating topological sort of the stations
    adj = {}
    pathTo = {}
    for station in stations:
        pathTo[station] = [station]
        
    for i in range(len(stations)):
        currStation = stations[i]
        adjacencies = []
        reachable = []
        rangeDist = (currStation.position + (avatarRange/2.0), currStation.position + avatarRange)
        
        for x in stations[(i+1):]:
            if x.position > rangeDist[1]:
                break
            else:
                reachable.append(x)
                if x.position >= rangeDist[0]:
                    adjacencies.append(x)
                    
        if len(adjacencies) == 0 and len(reachable) > 0:
            #for station in reachable:
            #    adjacencies.append(station)
            adjacencies.append(reachable[-1])
                
        adj[currStation] = adjacencies

    # Relaxing each edge
    for i in range(len(stations)):
        currStation = stations[i]
        if cost[currStation] < float('inf'):
            for nextStation in adj[currStation]:
                energyLoss = float(nextStation.position - currStation.position)/float(avatar.efficiency)
                newCost = cost[currStation] + 2 + energyLoss*float(nextStation.cost)
                if cost[nextStation] > newCost:
                    cost[nextStation] = newCost
    return cost[stations[-1]]-2.0





                                        
