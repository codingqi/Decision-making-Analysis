########################################
#
# @file rum_ana5.py
# @author: Qi Tian
# @date: 12/23/2018
# @model starts with full attendance + 1 attribute is ignored: 1+5=6 classes
# payment class removed
#######################################

from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *

#Parameters to be estimated
# Arguments:
#   - 1  Name for report; Typically, the same as the variable.
#   - 2  Starting value.
#   - 3  Lower bound.
#   - 4  Upper bound.
#   - 5  0: estimate the parameter, 1: keep it fixed.

# Parameters: Note that latent class models often get stuck in local maxima. To ensure a global maximum multiple starting values should be tested.
# To avoid getting trap in a local maxima, here we use starting values near the best known maximum.

# Here we focus on attendence behavior, rather than preference heterogeneity, so we apply Equality Constrained Latent Class which assumes
# same preference parameters for different classes

#Hypothetical parameters to be estimated
B_rfall      = Beta('B_rfall',0,-10,10,0)
B_rside      = Beta('B_rside',0,-10,10,0)
B_rwinter    = Beta('B_rwinter ',0,-10,10,0)
B_nitrogen   = Beta('B_nitrogen',0,-10,10,0)
B_pay        = Beta('B_pay',0,-10,10,0)
B_sq         = Beta('B_sq', 0, -10,10,0)
#Prime parameters to be estimated
P_rfall      = Beta('P_rfall ',0,-10,10,0)
P_rside      = Beta('P_rside ',0,-10,10,0)
P_rwinter    = Beta('P_rwinter',0,-10,10,0)
P_nitrogen   = Beta('P_nitrogen',0,-10,10,0)
P_pay        = Beta('P_pay',0,-10,10,0)

P_rfall      = B_rfall
P_rside      = B_rside
P_rwinter    = B_rwinter
P_nitrogen   = B_nitrogen
P_pay        = B_pay

#RUM model gamma=0
B_gamma      = Beta('B_gamma',0,0,1,1)
P_gamma      = Beta('P_gamma',0,0,1,1)

# Class membership parameters
s1 = Beta('s1',0,-100,100,1)
#s2 = Beta('s2',3.23,-100,100,0)
s2 = Beta('ana_fall', 0,-100,100,0)
s3 = Beta('ana_side',0,-100,100,0)
s4 = Beta('ana_winter',0,-100,100,0)
s5 = Beta('ana_nitrogen',0,-100,100,0)


#Generate regret variables
#The regret of choosing alt1 from rfall
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

# Utility / regret functions

# RUM class 1: all attended

R1_1 = - ( log( B_gamma + 1 )                                 + log( B_gamma + exp( B_rfall * rfall2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_rside * rside2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_rwinter * rwinter2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_nitrogen * nitrogen2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_pay * pay2_1 ) ) +
         log( P_gamma + exp( P_rfall * rfall3_1 ) )         +
         log( P_gamma + exp( P_rside * rside3_1 ) )         +
         log( P_gamma + exp( P_rwinter * rwinter3_1 ) )     +
         log( P_gamma + exp( P_nitrogen * nitrogen3_1 ) )   +
         log( P_gamma + exp( P_pay * pay3_1 ) ) )
         
R2_1 = - ( log( B_gamma + exp( B_rfall * rfall1_2 ) )         + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_rside * rside1_2 ) )         + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_rwinter * rwinter1_2 ) )     + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_nitrogen * nitrogen1_2 ) )   + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_pay * pay1_2 ) )             + log( B_gamma + 1 ) +
         log( P_gamma + exp( P_rfall * rfall3_2 ) )         +
         log( P_gamma + exp( P_rside * rside3_2 ) )         +
         log( P_gamma + exp( P_rwinter * rwinter3_2 ) )     +
         log( P_gamma + exp( P_nitrogen * nitrogen3_2 ) )   +
         log( P_gamma + exp( P_pay * pay3_2 ) ) )
         
         
R3_1 = - ( log( B_gamma + exp( B_rfall * rfall1_3 ) )         + log( B_gamma + exp( B_rfall * rfall2_3 ) ) +
         log( B_gamma + exp( B_rside * rside1_3 ) )         + log( B_gamma + exp( B_rside * rside2_3 ) ) +
         log( B_gamma + exp( B_rwinter * rwinter1_3 ) )     + log( B_gamma + exp( B_rwinter * rwinter2_3 ) ) +
         log( B_gamma + exp( B_nitrogen * nitrogen1_3 ) )   + log( B_gamma + exp( B_nitrogen * nitrogen2_3 ) ) +
         log( B_gamma + exp( B_pay * pay1_3 ) )             + log( B_gamma + exp( B_pay * pay2_3 ) ) +
         log( P_gamma + 1 )                                 +                          
         log( P_gamma + 1 )                                 +                                 
         log( P_gamma + 1 )                                 +                                  
         log( P_gamma + 1 )                                 +  
         log( P_gamma + 1 )                                 + 
         B_sq )

# RUM class 2: fall ignored
R1_2 = - ( log( B_gamma + 1 )                                 + log( B_gamma + exp( 0 * rfall2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_rside * rside2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_rwinter * rwinter2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_nitrogen * nitrogen2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_pay * pay2_1 ) ) +
         log( P_gamma + exp( 0 * rfall3_1 ) )         +
         log( P_gamma + exp( P_rside * rside3_1 ) )         +
         log( P_gamma + exp( P_rwinter * rwinter3_1 ) )     +
         log( P_gamma + exp( P_nitrogen * nitrogen3_1 ) )   +
         log( P_gamma + exp( P_pay * pay3_1 ) ) )
         
R2_2 = - ( log( B_gamma + exp( 0 * rfall1_2 ) )         + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_rside * rside1_2 ) )         + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_rwinter * rwinter1_2 ) )     + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_nitrogen * nitrogen1_2 ) )   + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_pay * pay1_2 ) )             + log( B_gamma + 1 ) +
         log( P_gamma + exp( 0 * rfall3_2 ) )         +
         log( P_gamma + exp( P_rside * rside3_2 ) )         +
         log( P_gamma + exp( P_rwinter * rwinter3_2 ) )     +
         log( P_gamma + exp( P_nitrogen * nitrogen3_2 ) )   +
         log( P_gamma + exp( P_pay * pay3_2 ) ) )
         
         
R3_2 = - ( log( B_gamma + exp( 0 * rfall1_3 ) )         + log( B_gamma + exp( 0 * rfall2_3 ) ) +
         log( B_gamma + exp( B_rside * rside1_3 ) )         + log( B_gamma + exp( B_rside * rside2_3 ) ) +
         log( B_gamma + exp( B_rwinter * rwinter1_3 ) )     + log( B_gamma + exp( B_rwinter * rwinter2_3 ) ) +
         log( B_gamma + exp( B_nitrogen * nitrogen1_3 ) )   + log( B_gamma + exp( B_nitrogen * nitrogen2_3 ) ) +
         log( B_gamma + exp( B_pay * pay1_3 ) )             + log( B_gamma + exp( B_pay * pay2_3 ) ) +
         log( P_gamma + 1 )                                 +                          
         log( P_gamma + 1 )                                 +                                 
         log( P_gamma + 1 )                                 +                                  
         log( P_gamma + 1 )                                 +  
         log( P_gamma + 1 )                                 + 
         B_sq )

# RUM class 3: side ignored
R1_3 = - ( log( B_gamma + 1 )                                 + log( B_gamma + exp( B_rfall * rfall2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( 0 * rside2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_rwinter * rwinter2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_nitrogen * nitrogen2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_pay * pay2_1 ) ) +
         log( P_gamma + exp( P_rfall * rfall3_1 ) )         +
         log( P_gamma + exp( 0 * rside3_1 ) )         +
         log( P_gamma + exp( P_rwinter * rwinter3_1 ) )     +
         log( P_gamma + exp( P_nitrogen * nitrogen3_1 ) )   +
         log( P_gamma + exp( P_pay * pay3_1 ) ) )
         
R2_3 = - ( log( B_gamma + exp( B_rfall * rfall1_2 ) )         + log( B_gamma + 1 ) +
         log( B_gamma + exp( 0 * rside1_2 ) )         + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_rwinter * rwinter1_2 ) )     + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_nitrogen * nitrogen1_2 ) )   + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_pay * pay1_2 ) )             + log( B_gamma + 1 ) +
         log( P_gamma + exp( P_rfall * rfall3_2 ) )         +
         log( P_gamma + exp( 0 * rside3_2 ) )         +
         log( P_gamma + exp( P_rwinter * rwinter3_2 ) )     +
         log( P_gamma + exp( P_nitrogen * nitrogen3_2 ) )   +
         log( P_gamma + exp( P_pay * pay3_2 ) ) )
         
         
R3_3 = - ( log( B_gamma + exp( B_rfall * rfall1_3 ) )         + log( B_gamma + exp( B_rfall * rfall2_3 ) ) +
         log( B_gamma + exp( 0 * rside1_3 ) )         + log( B_gamma + exp( 0 * rside2_3 ) ) +
         log( B_gamma + exp( B_rwinter * rwinter1_3 ) )     + log( B_gamma + exp( B_rwinter * rwinter2_3 ) ) +
         log( B_gamma + exp( B_nitrogen * nitrogen1_3 ) )   + log( B_gamma + exp( B_nitrogen * nitrogen2_3 ) ) +
         log( B_gamma + exp( B_pay * pay1_3 ) )             + log( B_gamma + exp( B_pay * pay2_3 ) ) +
         log( P_gamma + 1 )                                 +                          
         log( P_gamma + 1 )                                 +                                 
         log( P_gamma + 1 )                                 +                                  
         log( P_gamma + 1 )                                 +  
         log( P_gamma + 1 )                                 + 
         B_sq )

# RUM class 4: wint ignored
R1_4 = - ( log( B_gamma + 1 )                                 + log( B_gamma + exp( B_rfall * rfall2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_rside * rside2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( 0 * rwinter2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_nitrogen * nitrogen2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_pay * pay2_1 ) ) +
         log( P_gamma + exp( P_rfall * rfall3_1 ) )         +
         log( P_gamma + exp( P_rside * rside3_1 ) )         +
         log( P_gamma + exp( 0 * rwinter3_1 ) )     +
         log( P_gamma + exp( P_nitrogen * nitrogen3_1 ) )   +
         log( P_gamma + exp( P_pay * pay3_1 ) ) )
         
R2_4 = - ( log( B_gamma + exp( B_rfall * rfall1_2 ) )         + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_rside * rside1_2 ) )         + log( B_gamma + 1 ) +
         log( B_gamma + exp( 0 * rwinter1_2 ) )     + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_nitrogen * nitrogen1_2 ) )   + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_pay * pay1_2 ) )             + log( B_gamma + 1 ) +
         log( P_gamma + exp( P_rfall * rfall3_2 ) )         +
         log( P_gamma + exp( P_rside * rside3_2 ) )         +
         log( P_gamma + exp( 0 * rwinter3_2 ) )     +
         log( P_gamma + exp( P_nitrogen * nitrogen3_2 ) )   +
         log( P_gamma + exp( P_pay * pay3_2 ) ) )
         
         
R3_4 = - ( log( B_gamma + exp( B_rfall * rfall1_3 ) )         + log( B_gamma + exp( B_rfall * rfall2_3 ) ) +
         log( B_gamma + exp( B_rside * rside1_3 ) )         + log( B_gamma + exp( B_rside * rside2_3 ) ) +
         log( B_gamma + exp( 0 * rwinter1_3 ) )     + log( B_gamma + exp( 0 * rwinter2_3 ) ) +
         log( B_gamma + exp( B_nitrogen * nitrogen1_3 ) )   + log( B_gamma + exp( B_nitrogen * nitrogen2_3 ) ) +
         log( B_gamma + exp( B_pay * pay1_3 ) )             + log( B_gamma + exp( B_pay * pay2_3 ) ) +
         log( P_gamma + 1 )                                 +                          
         log( P_gamma + 1 )                                 +                                 
         log( P_gamma + 1 )                                 +                                  
         log( P_gamma + 1 )                                 +  
         log( P_gamma + 1 )                                 + 
         B_sq )
# RUM class 5: nitr ignored

R1_5 = - ( log( B_gamma + 1 )                                 + log( B_gamma + exp( B_rfall * rfall2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_rside * rside2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_rwinter * rwinter2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( 0 * nitrogen2_1 ) ) +
         log( B_gamma + 1 )                                 + log( B_gamma + exp( B_pay * pay2_1 ) ) +
         log( P_gamma + exp( P_rfall * rfall3_1 ) )         +
         log( P_gamma + exp( P_rside * rside3_1 ) )         +
         log( P_gamma + exp( P_rwinter * rwinter3_1 ) )     +
         log( P_gamma + exp( 0 * nitrogen3_1 ) )   +
         log( P_gamma + exp( P_pay * pay3_1 ) ) )
         
R2_5 = - ( log( B_gamma + exp( B_rfall * rfall1_2 ) )         + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_rside * rside1_2 ) )         + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_rwinter * rwinter1_2 ) )     + log( B_gamma + 1 ) +
         log( B_gamma + exp( 0 * nitrogen1_2 ) )   + log( B_gamma + 1 ) +
         log( B_gamma + exp( B_pay * pay1_2 ) )             + log( B_gamma + 1 ) +
         log( P_gamma + exp( P_rfall * rfall3_2 ) )         +
         log( P_gamma + exp( P_rside * rside3_2 ) )         +
         log( P_gamma + exp( P_rwinter * rwinter3_2 ) )     +
         log( P_gamma + exp( 0 * nitrogen3_2 ) )   +
         log( P_gamma + exp( P_pay * pay3_2 ) ) )
         
         
R3_5 = - ( log( B_gamma + exp( B_rfall * rfall1_3 ) )         + log( B_gamma + exp( B_rfall * rfall2_3 ) ) +
         log( B_gamma + exp( B_rside * rside1_3 ) )         + log( B_gamma + exp( B_rside * rside2_3 ) ) +
         log( B_gamma + exp( B_rwinter * rwinter1_3 ) )     + log( B_gamma + exp( B_rwinter * rwinter2_3 ) ) +
         log( B_gamma + exp( 0 * nitrogen1_3 ) )   + log( B_gamma + exp( 0 * nitrogen2_3 ) ) +
         log( B_gamma + exp( B_pay * pay1_3 ) )             + log( B_gamma + exp( B_pay * pay2_3 ) ) +
         log( P_gamma + 1 )                                 +                          
         log( P_gamma + 1 )                                 +                                 
         log( P_gamma + 1 )                                 +                                  
         log( P_gamma + 1 )                                 +  
         log( P_gamma + 1 )                                 + 
         B_sq )
         


# Associate utility functions with the numbering of alternatives
V1 = {1: R1_1,
      2: R2_1,
      3: R3_1}

V2 = {1: R1_2,
      2: R2_2,
      3: R3_2}

V3 = {1: R1_3,
      2: R2_3,
      3: R3_3}
      
V4 = {1: R1_4,
      2: R2_4,
      3: R3_4}

V5 = {1: R1_5,
      2: R2_5,
      3: R3_5}

 

# Associate the availability conditions with the alternatives
one =  DefineVariable('one',1)

av = {1: one,
      2: one,
      3: one}

# Class membership model
probClass1 = exp(s1)/(exp(s1) + exp(s2) + exp(s3) + exp(s4) + exp(s5) )
probClass2 = exp(s2)/(exp(s1) + exp(s2) + exp(s3) + exp(s4) + exp(s5) )
probClass3 = exp(s3)/(exp(s1) + exp(s2) + exp(s3) + exp(s4) + exp(s5) )
probClass4 = exp(s4)/(exp(s1) + exp(s2) + exp(s3) + exp(s4) + exp(s5) )
probClass5 = exp(s5)/(exp(s1) + exp(s2) + exp(s3) + exp(s4) + exp(s5) )


# The choice model is a logit, with availability conditions
prob1 = bioLogit(V1,av,chalt)
prob2 = bioLogit(V2,av,chalt)
prob3 = bioLogit(V3,av,chalt)
prob4 = bioLogit(V4,av,chalt)
prob5 = bioLogit(V5,av,chalt)


# Iterator on individuals, that is on groups of rows.
metaIterator('personIter','__dataFile__','panelObsIter','idset')

# For each item of personIter, iterates on the rows of the group. 
rowIterator('panelObsIter','personIter')

#Conditional probability for the sequence of choices of an individual
ProbIndiv_1 = Prod(prob1,'panelObsIter')
ProbIndiv_2 = Prod(prob2,'panelObsIter')
ProbIndiv_3 = Prod(prob3,'panelObsIter')
ProbIndiv_4 = Prod(prob4,'panelObsIter')
ProbIndiv_5 = Prod(prob5,'panelObsIter')


# Define the likelihood function for the estimation
BIOGEME_OBJECT.ESTIMATE = Sum(log(probClass1 * ProbIndiv_1 + probClass2 * ProbIndiv_2 + probClass3 * ProbIndiv_3 + probClass4 * ProbIndiv_4 + probClass5 * ProbIndiv_5 ),'personIter')


# All observations verifying the following expression will not be
# considered for estimation
# for Q5, don't have the capacity to participate （q5 == 3)/don't like any government program(q5==5)
# Observations will be removed.
#exclude = (( q5 == 5)+(chalt == 9999)) > 0
exclude = (( q5 == 5)+(chalt == 9999)+(set == 3) + (set ==2) + (set ==1)) > 0
BIOGEME_OBJECT.EXCLUDE = exclude

# Statistics
BIOGEME_OBJECT.PARAMETERS['optimizationAlgorithm'] = "CFSQP"
BIOGEME_OBJECT.PARAMETERS['numberOfThreads'] = "4"
BIOGEME_OBJECT.STATISTICS['Number of individuals'] = Sum(1,'personIter')





