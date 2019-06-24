# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:57:22 2019

@author: ODsLaptop
"""

# import libraries
import csv
import math
import networkx as net
from networkx.algorithms import bipartite as bi
import matplotlib as plot
import pandas as pd
 
# load data in from csv to pandas dataframe
nba_data = csv.reader(open("NBA_network.csv"))
#nba_data = pd.read_csv("NBA_network.csv")
# create network 
g = net.Graph()

# lists of all distinct teams and players
teams = []
players = []

# construct directed graph
for row in nba_data:
    if row[0] not in teams:
        teams.append(row[0])
    if row[1] not in players:
        players.append(row[1])
    g.add_edge(row[0], row[1], weight=1)

# draw the network (giant blob..)
#net.draw(g, with_labels=True)

# find the size of the network (number of nodes)
print "nodes in network:", len(g)

# look at components of the whole network
connected_net = list(net.connected_component_subgraphs(g))
print "size of largest component:", len(connected_net[0])

# create an affiliation network of only teams
teamnet = bi.weighted_projected_graph(g, teams)
#net.draw(teamnet)

# create an affiliation network of only players
# this will become our main network..
playernet = bi.weighted_projected_graph(g, players)
#net.draw(playernet)

# look at centrality among players
deg = net.degree(playernet)
deg_list = sorted(playernet.degree, key=lambda x: x[1], reverse=True)
print "LeBron James' degree:", deg['LeBron James']
print "top 10 highest degree:", deg_list[0:9]
print "ok, this list looks like players that have stayed in NBA but bounced around.."
print "degree centrality doesn't matter for teams.."
print "==================="

# look at closeness centrality of players, and teams
import operator
closeness_cen = net.closeness_centrality(playernet)
closeness_list = sorted(closeness_cen.items(), key=operator.itemgetter(1))
print "LeBron James' closeness:", closeness_cen['LeBron James']
print "top 10 highest closeness:", closeness_list[520:529]
print "looks like a lot of the same players as degree centrality"
print "==================="

# look at betweenness centrality of players
betweenness_cen = net.betweenness_centrality(playernet)
betweenness_list = sorted(betweenness_cen.items(), key=operator.itemgetter(1))
print "LeBron James' betweenness:", betweenness_cen['LeBron James']
print "top 10 highest betweennessd:", betweenness_list[520:529]
print "looks like a lot of the same players as degree centrality"
print "==================="

# now, to see the players with the highest degree (start of the island method..)
deg_tests = [30, 40, 50, 60, 70, 80]
num_players = 0
for i in deg_tests:    
    for j in players:
        if deg(j)>i:
            num_players = num_players + 1
    print i, num_players
    num_players = 0

# let's look at only the nodes with 60+ degree
for i in players:
    if deg(i)<47:
        playernet.remove_node(i)
net.draw(playernet, with_labels=True)

deg_list = sorted(playernet.degree, key=lambda x: x[1], reverse=True)
print "top 10 highest degree:", deg_list[0:9]

# Now, to identify the network of current allstar players
all_stars = ['James Harden',
             'Kevin Durant',
             'Kyrie Irving',
             'Kawhi Leonard',
             'LeBron James',
             'Anthony Davis',
             'Ben Simmons',
             'Bradley Beal',
             'Damian Lillard',
             'Dwayne Wade',
             'Karl-Anthony Towns',
             'Klay Thompson',
             'LaMarcus Aldridge',
             'Giannis Antetokounmpo',
             'Stephen Curry',
             'Joel Embiid',
             'Paul George',
             'Kemba Walker',
             'Blake Griffin',
             'DAngelo Russell',
             'Dirk Nowitzki',
             'Khris Middleton',
             'Kyle Lowry',
             'Nikola Jokic',
             'Nikola Vucevic',
             'Victor Oladipo',
             'Russell Westbrook']