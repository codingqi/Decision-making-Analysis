#############################################################################
#                                                                           #
# @file gm-rrm.py                                                        #
# @author: Qi Tian                                                          #
# @date: 7/11/2018                                                          #
# Using rdata - upper bound of experienced adoption                         #
#                                                                           #
#############################################################################

# Before getting started:
# Check gamma constrain value first!!!!!!!!!!!!!!!!!!!!!!!!!!
# certain(1-5, 5 as very certain)


# step 1: import libraries
from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *


# Step 2: Parameters to be estimated
# Arguments:
#   - 1  Name for report; Typically, the same as the variable.
#   - 2  Starting value.
#   - 3  Lower bound.
#   - 4  Upper bound.
#   - 5  0: estimate the parameter, 1: keep it fixed.


#Prime parameters to be estimated
P_rfall      = Beta('P_rfall ',0,-10,10,0)
P_rside      = Beta('P_rside ',0,-10,10,0)
P_rwinter    = Beta('P_rwinter',0,-10,10,0)
P_nitrogen   = Beta('P_nitrogen',0,-10,10,0)
P_pay        = Beta('P_pay',0,-10,10,0)
B_sq         = Beta('B_sq', 0, -10,10,0)

#Assumption 1: Hypothetical parameters = Prime paramter * rx
#Assumption 2: only hypothetical alternatives for nitrogen, and pay have effects
rf           = Beta('ra_fall', 0, 0, 1, 1)
rs           = Beta('ra_side', 0, 0, 1, 1)
rw           = Beta('ra_winter', 0, 0, 1, 1)
rn           = Beta('ra_nitrogen', 0, 0, 1, 0) #set as flexible
rp           = Beta('ra_pay', 0, 0, 1, 0) #set as flexible
#hypothetical alternative
B_rfall      = P_rfall*rf
B_rside      = P_rside*rs
B_rwinter    = P_rwinter*rw
B_nitrogen   = P_nitrogen*rn
B_pay        = P_pay*rp
#Assumption 3: gamma = g_cons + g_beta * certainty of choice
#we use this function to test the impact of certainty of choice on decision rule
g_cons        = Beta('gamma constant',0,-10,10,0)
g_beta        = Beta('gamma beta',0,-10,10,0)

# Step 3: write utility function 

#Generate regret variables
#The regret of choosing alt1 from rfall is generated by comparison
rfall2_1 = DefineVariable('rfall2_1', ( rfall2 - rfall1 ) / 1)
rfall3_1 = DefineVariable('rfall3_1', ( rfall3 - rfall1 ) / 1)

#The regret of choosing alt2 from rfall
rfall1_2 = DefineVariable('rfall1_2', ( rfall1 - rfall2 ) / 1)
rfall3_2 = DefineVariable('rfall3_2', ( rfall3 - rfall2 ) / 1)

#The regret of choosing alt3 from rfall
rfall1_3 = DefineVariable('rfall1_3', ( rfall1 - rfall3 ) / 1)
rfall2_3 = DefineVariable('rfall2_3', ( rfall2 - rfall3 ) / 1)

#The regret of choosing alt1 from rside
rside2_1 = DefineVariable('rside2_1', ( rside2 - rside1 ) / 1)
rside3_1 = DefineVariable('rside3_1', ( rside3 - rside1 ) / 1)

#The regret of choosing alt2 from rside
rside1_2 = DefineVariable('rside1_2', ( rside1 - rside2 ) / 1)
rside3_2 = DefineVariable('rside3_2', ( rside3 - rside2 ) / 1)

#The regret of choosing alt3 from rside
rside1_3 = DefineVariable('rside1_3', ( rside1 - rside3 ) / 1)
rside2_3 = DefineVariable('rside2_3', ( rside2 - rside3 ) / 1)

#The regret of choosing alt1 from rwinter
rwinter2_1 = DefineVariable('rwinter2_1', ( rwinter2 - rwinter1 ) / 1)
rwinter3_1 = DefineVariable('rwinter3_1', ( rwinter3 - rwinter1 ) / 1)

#The regret of choosing alt2 from rwinter
rwinter1_2 = DefineVariable('rwinter1_2', ( rwinter1 - rwinter2 ) / 1)
rwinter3_2 = DefineVariable('rwinter3_2', ( rwinter3 - rwinter2 ) / 1)

#The regret of choosing alt3 from rwinter
rwinter1_3 = DefineVariable('rwinter1_3', ( rwinter1 - rwinter3 ) / 1)
rwinter2_3 = DefineVariable('rwinter2_3', ( rwinter2 - rwinter3 ) / 1)

#The regret of choosing alt1 from nitrogen
nitrogen2_1 = DefineVariable('nitrogen2_1', ( nitrogen2 - nitrogen1 ) / 1)
nitrogen3_1 = DefineVariable('nitrogen3_1', ( nitrogen3 - nitrogen1 ) / 1)

#The regret of choosing alt2 from nitrogen
nitrogen1_2 = DefineVariable('nitrogen1_2', ( nitrogen1 - nitrogen2 ) / 1)
nitrogen3_2 = DefineVariable('nitrogen3_2', ( nitrogen3 - nitrogen2 ) / 1)

#The regret of choosing alt3 from nitrogen
nitrogen1_3 = DefineVariable('nitrogen1_3', ( nitrogen1 - nitrogen3 ) / 1)
nitrogen2_3 = DefineVariable('nitrogen2_3', ( nitrogen2 - nitrogen3 ) / 1)

#The regret of choosing alt1 from pay
pay2_1 = DefineVariable('pay2_1', ( pay2 - pay1 ) / 1)
pay3_1 = DefineVariable('pay3_1', ( pay3 - pay1 ) / 1)

#The regret of choosing alt2 from pay
pay1_2 = DefineVariable('pay1_2', ( pay1 - pay2 ) / 1)
pay3_2 = DefineVariable('pay3_2', ( pay3 - pay2 ) / 1)

#The regret of choosing alt3 from pay
pay1_3 = DefineVariable('pay1_3', ( pay1 - pay3 ) / 1)
pay2_3 = DefineVariable('pay2_3', ( pay2 - pay3 ) / 1)

# Utility functions

R1 = - ( log( g_cons + g_beta *certain + 1 )                                 + log( g_cons + g_beta *certain + exp( B_rfall * rfall2_1 ) ) +
         log( g_cons + g_beta *certain + 1 )                                 + log( g_cons + g_beta *certain + exp( B_rside * rside2_1 ) ) +
         log( g_cons + g_beta *certain + 1 )                                 + log( g_cons + g_beta *certain + exp( B_rwinter * rwinter2_1 ) ) +
         log( g_cons + g_beta *certain + 1 )                                 + log( g_cons + g_beta *certain + exp( B_nitrogen * nitrogen2_1 ) ) +
         log( g_cons + g_beta *certain + 1 )                                 + log( g_cons + g_beta *certain + exp( B_pay * pay2_1 ) ) +
         log( g_cons + g_beta *certain + exp( P_rfall * rfall3_1 ) )         +
         log( g_cons + g_beta *certain + exp( P_rside * rside3_1 ) )         +
         log( g_cons + g_beta *certain + exp( P_rwinter * rwinter3_1 ) )     +
         log( g_cons + g_beta *certain + exp( P_nitrogen * nitrogen3_1 ) )   +
         log( g_cons + g_beta *certain + exp( P_pay * pay3_1 ) ) )
         
R2 = - ( log( g_cons + g_beta *certain + exp( B_rfall * rfall1_2 ) )         + log( g_cons + g_beta *certain + 1 ) +
         log( g_cons + g_beta *certain + exp( B_rside * rside1_2 ) )         + log( g_cons + g_beta *certain + 1 ) +
         log( g_cons + g_beta *certain + exp( B_rwinter * rwinter1_2 ) )     + log( g_cons + g_beta *certain + 1 ) +
         log( g_cons + g_beta *certain + exp( B_nitrogen * nitrogen1_2 ) )   + log( g_cons + g_beta *certain + 1 ) +
         log( g_cons + g_beta *certain + exp( B_pay * pay1_2 ) )             + log( g_cons + g_beta *certain + 1 ) +
         log( g_cons + g_beta *certain + exp( P_rfall * rfall3_2 ) )         +
         log( g_cons + g_beta *certain + exp( P_rside * rside3_2 ) )         +
         log( g_cons + g_beta *certain + exp( P_rwinter * rwinter3_2 ) )     +
         log( g_cons + g_beta *certain + exp( P_nitrogen * nitrogen3_2 ) )   +
         log( g_cons + g_beta *certain + exp( P_pay * pay3_2 ) ) )
         
         
R3 = - ( log( g_cons + g_beta *certain + exp( B_rfall * rfall1_3 ) )         + log( g_cons + g_beta *certain + exp( B_rfall * rfall2_3 ) ) +
         log( g_cons + g_beta *certain + exp( B_rside * rside1_3 ) )         + log( g_cons + g_beta *certain + exp( B_rside * rside2_3 ) ) +
         log( g_cons + g_beta *certain + exp( B_rwinter * rwinter1_3 ) )     + log( g_cons + g_beta *certain + exp( B_rwinter * rwinter2_3 ) ) +
         log( g_cons + g_beta *certain + exp( B_nitrogen * nitrogen1_3 ) )   + log( g_cons + g_beta *certain + exp( B_nitrogen * nitrogen2_3 ) ) +
         log( g_cons + g_beta *certain + exp( B_pay * pay1_3 ) )             + log( g_cons + g_beta *certain + exp( B_pay * pay2_3 ) ) +
         log( g_cons + g_beta *certain + 1 )                                 +                          
         log( g_cons + g_beta *certain + 1 )                                 +                                 
         log( g_cons + g_beta *certain + 1 )                                 +                                  
         log( g_cons + g_beta *certain + 1 )                                 +  
         log( g_cons + g_beta *certain + 1 )                                 + 
         B_sq )

# step 4: prepare estimation with logistic model
# Associate utility functions with the numbering of alternatives
V = {1: R1,
     2: R2,
     3: R3}

# Associate the availability conditions with the alternatives
av = {1: one,
      2: one,
      3: one}

# The choice model is a logit, with availability conditions
prob = bioLogit(V,av,chalt)
logP = log(prob)

# Defines an itertor on the data
rowIterator('obsIter') 

# DEfine the likelihood function for the estimation
BIOGEME_OBJECT.ESTIMATE = Sum(logP,'obsIter')

# step 5*: set up the sample
# All observations verifying the following expression will not be
# considered for estimation
# for Q5, don't have the capacity to participate （q5 == 3)/don't like any government program(q5==5)
# Observations will be removed.
exclude = (( q5 == 5)+(certain==9999)) > 0

BIOGEME_OBJECT.EXCLUDE = exclude



# step 6: Statistics estimation

nullLoglikelihood(av,'obsIter')
choiceSet = [1,2,3]
cteLoglikelihood(choiceSet,chalt,'obsIter')
availabilityStatistics(av,'obsIter')


BIOGEME_OBJECT.PARAMETERS['optimizationAlgorithm'] = "CFSQP"
BIOGEME_OBJECT.PARAMETERS['numberOfThreads'] = "2"
