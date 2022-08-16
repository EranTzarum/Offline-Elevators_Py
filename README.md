# Offline-Elevators

## | @RazGavrieli | @AmitMelamed  | @EranDavidTzarum |

This projects is for the second assigment on OOP course Ariel Universitiy 2021, winter semster.

TO RUN the project just clone it into your computer,

**and use command: python3 main.py Ex1_Buildings/B5.json Ex1_Calls/Calls_a.csv output.csv**

you can change to any Building from Ex1_Buildings folder (B1-B5) and to any Call from Ex1_Calls folder (Calls_a - Calls_d).


KEEP IN MIND that if you want to run the test automaticly right after you run the algorithm, scroll down to the last line and uncomment the subproccess line.

##OOP 21 - Assignment Ex1

<img width="391" alt="elevetors" src="https://user-images.githubusercontent.com/106338500/184890118-0cb9b242-c989-4b44-b8b0-b34311d8be21.png">


Python and offline algorithm


We begin by defining the biggest difference between the Online and Offline algorithm.
At the time of solving the Online algorithm we have taken for granted the function that
calculates the Elevator’s position.
In this assignment we have explored the idea of writing our own algorithm that can foresee
the position of a given elevator and a list of calls that it had to satisfy.
The idea of this kind of solution would involve Dynamic Programming, using matrices to hold
the value of time that the elevator would get to a specific floor. And that way calculating
when the elevator would get to every floor at any given time.
On the other hand, we had another more elegant solution that would divide the calls to all
the elevators, trying to scatter the calls in an even manner. When we choose this route, we
noticed that it is important to divide the calls to groups of time zones, meaning that a call that
has taken place at the beginning of the day won’t affect the decision for a call that is taking
place at the middle of the day, much later.
This solution is also using the position of the elevator, trying to update it as the code runs.
But (and this is taken into account) the position is estimated and not exact.
Taking inspiration from the first assignment, we’ve implemented the idea of a callsQueue for
every elevator. That way we can have group-control and have a more efficient solution.


##Offline Algorithm

First we’ve created two new objects, Call and Elevator. 

Class Elevator - 
This object holds all the data given from the building through the json file.
It also holds a list named callsQueue, so each elevator has its own queue of calls. 
It also holds a list named arrfloose that contain the second that the elevator will by at the 
(i - minFloor) floor.
spf stand for - second per floor and we calculate this 
stf=((speed*(maxFloor-minFloor))-startTime-stopTime-openTime-closeTime)/(maxFloor-minFloor)
 for every elevator
we also have mood for every elevator to see if the elevator going up or down in every call.


clearCompleteCalls -
If the ‘current’ time + INTERVAL is bigger than the call’s time, 
delete this call from callsQueue.


Class Call -
This object holds all the data given from the csv file. 
It also holds information about the distance (in floors) of the call, and the allocated elevators for this call. 
The allocatedElevators field is used to write into the output which elevators has been allocated to each floor. 


Main allocating algorithm -

nearsource - this function allocated an elevator by checking if the call is up or down.
after we want to go over all elevators to see which one closer to call.source be given call.time and compare it to elevator[i].arrfloose[call.source] which contains the second that the elevator will be the call.source floor .
the elevator who have the mintime to go to the call.source end doest have too many calls
end in up mood will take the call
if the elevator has many calls we will give the call to the elevator with the less calls on the function callQ .
when an elevator takes the call we inishiz her arrfloose and mood.
We will do the same for down calls.

allocateElevatorFor2Elevators - 
Check which elevator is faster. 
If the call is in the upper two thirds of the building, use the faster elevator. 
Else (the call is in the lower third of the building), use the slower elevator. 
This method does not use calcTime nor callsQueue. 



Performance:

The Data is written as  - **average waiting time per call / uncompleted calls**

For example: average waiting time per call: 112.92,  unCompleted calls,0 == 112.92/0

| Building/Calls | A        | B           | C          | D           |
|---|----------|-------------|------------|-------------|
| 1 | 112.92/0 | -           | -          | -           |
| 2 | 56.32/0  | -           | -          | -           |
| 3 | 44.25/0  | 485.032/140 | 523.140/65 | 491.445/84  |
| 4 | 25.32/0  | 527.656/318 | 541.333/84 | 551.780/311 |
| 5 | 23.68/0  | 228.652/101 | 222.539/43 | 170.579/41  |





This project has a change in the algorithms from our original project found in - LINKS:
main git link: https://github.com/amitmelamed/Offline-Elevators-EX1 Documentation 

PDF link: https://github.com/amitmelamed/Offline-Elevators-EX1/blob/main/Documentation.pdf

But still the contribution of each of us is the same.
