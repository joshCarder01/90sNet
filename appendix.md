Meetings

2023-08-31 (2 hrs)
Goals: Weekly Assignment and project planning
* Create repo on github
* Upload prof. bios to repo
* Uploaded file with basic team and project information into the repo
* Find advisor
	* Chad thinks Dr Hawkins III would be able to do it. He will be contacting him about this
* Identify areas of proficiency: Josh
	* Well versed in current university network structure
		* Will be informative in potentially REing old systems to make sure they make sense with current methods
	* Well versed in campus structure history
		* Will be informative in making sure any historical documents are consistent with time period
		* Will be informative to fill in gaps with well informed guesses where documentation doesn't exist
	* Experience building frameworks to be used by outside teams
	* Experience building automation scripts 
	* Experience with network hardware and systems
	
* Identify areas of proficiency: Chad
	* Experience with containers and virtual machines
		* This technology is what we believe we will be building our solution off of
	* Experience with Capture the Flag cyber games
		* This is the primary use for our project.
		* His knowledge will be helpful in making sure we have necessary parts and technology that is expected at these events	
* Create rough feature set for project:
	* Student connections (anywhere on campus) Pros:
		* Can be a part of the games mechanics (moving from place to place to get access to different things)
	* Cons:
		* How would we implement this? This seems hard to balance for gameplay
	
--------------------------------------------------------------------------------------
2023-09-07 (2hrs)
Goals: Weekly assignment and project planning
Recap: All parties completed 2 hrs of independent work. (6hrs since project start)
* Outline meeting expectations
	* We are both able to meet thursdays
	* Get confirmation from Dr Hawkins to see if he is able to also meet that day occasionally
* Breakdown tasks
	* Historical research
		* interviews
		* finding documentation
		* finding general historical information
	* Build layout of network
	* Build interface for network
	* Build network
		* what level do we want to do this on
		* what hardware will we use to build it
		* we should probably use a modular system to allow for reuse of parts where necessary
			* investigate technologies applicable to this
* Add team contract to repo
* Chad got confirmation from Dr Hawkins III
* Independently work on essays
* Josh reaching out to campus workers regarding network

--------------------------------------------------------------------------------------
2023-09-14
Goals: Weekly assignment and project planning
Recap: All parties completed 4 hrs of independent work. (12hrs since project start)
* Chad: Develope user stories
	* Has most experience with CTF, best person for this job
* What systems will we include in the network?
	* Personal devices
		* At what density or depth? Should we invest in scaling with hardware abilities. Auto scaling based on admins?
	* Network devices
		* Should they be made in function or function and form (copy exact OS vs just function)
	* Physical security (card swipes)
		* research for this real system is hard to come by
		* When did UC implement this system  and what for (no timeline)
		* ethical concern for mimicking exact system for people to find loopholes to use in real life
		* What if we built our own fake backend. Would be hard but fun? on backburner
	* Lab systems
		* Fake lab projects?
	* Proxies for people interacting with the project
		* How do we make these safe
* Automated systems
	* How are we going to know what is going on in the network
		* some sort of event collection
		* This will depend on the technology we choose to persue with network
		* Josh thinks docker containers will be easiest to interact with while not being on the network
		* Docker can't really do windows containers?

* Josh: Design Diagrams
	* 90sNet project encapsulation
	* Separate automated systems and admin systems
		* Virtual network should also incluse Faculty systems and dept systems

* Josh: interview with Dr Franco recap
	* IBM mainframe (bad)
	* No personal details on systems
	* Mentioned personal computers used
	* Thin clients were prominent with servers on campus (ATT?)
* No response from others

--------------------------------------------------------------------------------------
2023-09-21
Goals: Weekly assignment and project planning
Recap: All parties completed 2 hrs of independent work. (16hrs since project start)

* Make task list:
	# Task List

	# Research Phase
	1. Research university network structure in 1990s. [Josh Hale]
	2. Research university network systems in the 1990s. [Josh Hale]
	3. Research general university information (buildings etc) in the 1990s to fill knowledge gaps. [Josh Hale]
	4. Research general campus networking practices (common systems and structure) in the 1990s to fill knowledge gaps. [Josh Hale]

	5. Research viable hardware to run project on {Likely nomad with lab hardware}. [Chad Lape]
	6. Research viable medium to run project on (Docker etc). [Chad Lape]
	7. Research Daemons which can give an overview of the state of the network. [Chad Lape]
	8. Research methods to access hardware remotely. [Chad Lape]

	# Design Phase
	9. Specify systems to include on network. [Josh Hale]
	10. Develop a small scale test network on the hardware. [Chad Lape]
	11. Design admin control system and a way to interact with the virtual network. [Chad Lape]
	12. Develop methods for event collection+queuing and scoring in the automated systems. [Josh Hale]
	13. Develop Admin Dashboard for tracking container failures and logging. [Chad Lape]

	# Development of Virtual Network Environment
	14. Develop proxies which competitors will connect into the environment. [Josh Hale]
	15. Develop images for containers of the Lab Systems. [Josh Hale]
	16. Develop images for containers of the Physical Security Systems. [Josh Hale]
	17. Develop images for containers of the Network Devices. [Chad Lape]
	18. Develop images for containers of the Personal NPC Devices. [Chad Lape]
	19. Develop images for containers of the Department Systems. [Chad Lape]


	# Stretch Tasks
	* Develop automated adversary system to act as an attacker.
	* Develop method for proxies to be in different physical locations on the campus.
	
* review general outline for network (small scale) that Josh made
	* We realize that we will need a scalable solution to fit with given hardware
	* weighing options on auto scaling vs manual manipulation
* Chad continues research on software solution. Nomad? Quemu support will be needed with windows?


2023-09-28
Goals: Weekly assignment and project planning
Recap: All parties completed 2 hrs of independent work. (20hrs since project start)
* Josh creates proof of concept sucking info from docker containers
	* dir copy, check files, take action
	* uses docker
* Chad confirmed we are able to use Cyber@UC lab hardware
# Milesstones for assignment:
1. Lock down network design (complete 10/31): Have a formal design written for the network structure within 90s net set.	10/01/23
2. Small scale network demonstration (10/31): Have one network spoke along with around a dozen devices virtualized and communicating. A user should be able to proxy into this network as well.	10/01/23
3. Network interaction demonstration (11/30): Have an automated system and admin abilities to interact with the network.	11/01/23
4. Network device template design lock (1/30): All devices on the virtual network will be derived from a handful of templates. This templates should be finished (operational single units)	01/01/24
5. Admin infrastructure demonstration (2/28): Infrastructure, systems, and programs used by admins to interact with	02/01/24
6. Event scanning demonstration (2/28): Events that occur on the network should be logged to be seen by admins for dealt with by future automated systems	02/01/24
7. Automated system dealing with events demonstration (3/31): A system that scores players based on actions taken in the network. Built off of event scanning and logging.	03/01/24
8. Full network demonstration (4/15): Implement full network and demonstrate all capabilities	04/01/24
# Tasks for assignment
1. Research university network structure in 1990s [Josh Hale]	09/01/23
2. Research university network systems in the 1990s [Josh Hale]	09/01/23
3. Research general university information (buildings etc) in the 1990s to fill knowledge gaps [Josh Hale]	09/01/23
4. Research general campus networking practices (common systems and structure) in the 1990s to fill knowledge gaps [Josh Hale]	09/01/23
5. Research viable hardware to run project on {Likely nomad with lab hardware} [Chad Lape]	09/01/23
6. Research viable medium to run project on (Docker etc) [Chad Lape]	09/01/23
7. Research Daemons which can give an overview of the state of the network [Chad Lape]	09/01/23
8. Research methods to access hardware remotely [Chad Lape]	09/01/23
9. Specify systems to include on network [Josh Hale]	10/01/23
10. Develop a small scale test network on the hardware [Chad Lape]	10/01/23
14. Develop proxies which competitors will connect into the environment [Josh Hale]	10/01/23
11. Design admin control system and a way to interact with the virtual network [Chad Lape]	11/01/23
13. Develop Admin Dashboard for tracking container failures and logging [Chad Lape]	02/01/24
12. Develop methods for event collection+queuing and scoring in the automated systems [Josh Hale]	03/01/24
15. Develop images for containers of the Lab Systems [Josh Hale]	04/01/24
16. Develop images for containers of the Physical Security Systems [Josh Hale]	04/01/24
17. Develop images for containers of the Network Devices [Chad Lape]	04/01/24
18. Develop images for containers of the Personal NPC Devices [Chad Lape]	04/01/24
19. Develop images for containers of the Department Systems [Chad Lape]	04/01/24
#Effort Matrix for assignment
Items	Josh Effort %	Chad Effort %
Tasks	75.00%	25.00%
1. Research university network structure in 1990s [Josh Hale]	75.00%	25.00%
2. Research university network systems in the 1990s [Josh Hale]	75.00%	25.00%
3. Research general university information (buildings etc) in the 1990s to fill knowledge gaps [Josh Hale]	75.00%	25.00%
4. Research general campus networking practices (common systems and structure) in the 1990s to fill knowledge gaps [Josh Hale]	75.00%	25.00%
5. Research viable hardware to run project on {Likely nomad with lab hardware} [Chad Lape]	25.00%	75.00%
6. Research viable medium to run project on (Docker etc) [Chad Lape]	25.00%	75.00%
7. Research Daemons which can give an overview of the state of the network [Chad Lape]	25.00%	75.00%
8. Research methods to access hardware remotely [Chad Lape]	25.00%	75.00%
9. Specify systems to include on network [Josh Hale]	75.00%	25.00%
10. Develop a small scale test network on the hardware [Chad Lape]	25.00%	75.00%
14. Develop proxies which competitors will connect into the environment [Josh Hale]	75.00%	25.00%
11. Design admin control system and a way to interact with the virtual network [Chad Lape]	25.00%	75.00%
13. Develop Admin Dashboard for tracking container failures and logging [Chad Lape]	25.00%	75.00%
12. Develop methods for event collection+queuing and scoring in the automated systems [Josh Hale]	75.00%	25.00%
15. Develop images for containers of the Lab Systems [Josh Hale]	75.00%	25.00%
16. Develop images for containers of the Physical Security Systems [Josh Hale]	75.00%	25.00%
17. Develop images for containers of the Network Devices [Chad Lape]	25.00%	75.00%
18. Develop images for containers of the Personal NPC Devices [Chad Lape]	25.00%	75.00%
19. Develop images for containers of the Department Systems [Chad Lape]	25.00%	75.00%


2023-10-05
Goals: Weekly assignment and project planning
Recap: All parties completed 2 hrs of independent work. (24hrs since project start)
* Both continuing lots of work on prototypes
* Chad deeper research on Nomad
* Essay:
	Project Constraints:
	Economic Constraints
		Focus on hardware and computing resources
		Implementation running on a server maintained by a student organization
		Utilization of preexisting implementations for scalable deployment
	Ethical Constraints
	Avoiding the project becoming a testing ground for modern-day malware
	Simulation of a 90s network as a live-fire environment to render it irrelevant for modern attackers
	Minimal risk due to the need for intimate knowledge of a specific network's inner workings
	Accessibility for Future Maintainers
		Quick understanding of the project's workings
		Relatively easy to grasp with basic knowledge of cloud computing
		Minimizing the learning curve for maintainers to prevent prolonged training periods
	Security Measures:
		Importance of Contestant Security
		Live-fire environment's connections may come into contact with malicious software
		Implementation of proxies and networking rules to mitigate threats to contestants
		Ongoing Research for Enhanced Security
		Plans for further research to safely sandbox the network from external resources
*Essay final
	The project will satisfy various constraints, including but not limited to economics, ethics, maintenance, and security. The economic constraints would center on the hardware used and computing resources available. Our implementation will run on a server maintained by a student organization. The project would use preexisting implementations of scalable deployment such that it runs on any hardware given to it. The ethical constraints of this project center on this project becoming a testing ground for modern-day malware. With this simulating a network from the 90s, this live-fire environment would be irrelevant for any modern attackers. Any risk of this is minimal as a simulation of a corporate network would already require intimate knowledge of that network's inner workings. This software's purpose would be constrained if it were esoteric to others. It must be easily extendable to fit the needs of other projects which rely on it. In addition, future project maintainers should be able to quickly understand its workings. It must also be relatively easy to know given a basic knowledge of cloud computing and such so that maintainers would not be burdened with months of learning just this tool alone. The security of contestants is of utmost importance as connections to the live-fire environment will come into contact with malicious software. Implementation of proxies and networking rules can help mitigate the threat to contestants. We will conduct further research to safely sandbox the network from outside resources.

2023-10-12
Goals: Weekly assignment and project planning
Recap: All parties completed 4 hrs of independent work. (30hrs since project start)
* Josh received a reply from other people he contacted
	* outlook not so good
	* they said no one in the department was around during the 90s
	* they said there was no other documents regarding things from the 90s
		* likely story lol I'm pretty sure this is just cover cause they don't want to release the plans
		* I don't blame them really tbh
* How are we going replicate if we don't have hard facts to go on?
	* Josh completed extensive research on historical UC systems
	* note: UC main street project happened in the 90s, we are opting to set our time after manti was built but before major construction was done (alumni building still in place, lots of parking, etc)
* More research done by chad into how we are hosting
* Assignment: video presentation
	* putting together all the previous assignments
	* Demo ideas?

2023-10-19
Goals: Weekly assignment and project planning
Recap: All parties completed 2 hrs of independent work. (34hrs since project start)
* Josh and Chad continued to work on planning out video
* Video recorded
* Continued discussion regarding scalability
* Reconsider some timelines due to more research needing to be done

2023-10-26
Goals: Weekly assignment and project planning
Recap: All parties completed 2 hrs of independent work. (38hrs since project start)
* Both members independently reviewed others projects and left notes
* Took notes regarding things we think other groups are doing well and what we want to take from that
* Reviewed given so far from other groups
	* very positive reception
	* maybe make demo more guided?
* general discussion regarding project progress and direction

2023-11-02
Goals: Weekly assignment and project planning
Recap: All parties completed 2 hrs of independent work. (42hrs since project start)
* Started putting together work for final assignment
* Chad building out prototype
* Josh building out prototype
* continued discussion

2023-11-16
Goals: Weekly assignment and project planning
Recap: All parties completed 3 hrs of independent work. (47hrs since project start)
* finalized outline for work separation for final assignment
* continued work on prototypes

--------------------------------------------------------------------------------------
					NEW SEMESTER
--------------------------------------------------------------------------------------
2024-01-15 (2hrs)
Goals: Weekly assignment and project planning
Recap: All parties completed 0 hrs of independent work. (49hrs since project start)
* Develope test plan
	* User connection
	* User interaction
	* Bad user
	* Network separation
	* Infrastructure boot
	* Bad user in infrastructure
	* Data read
	* Event creation
	* Frontend test
	* Full system tests
* Begin outlining logistical connection of prototypes

2024-01-18 (2hrs)
Goals: Combine protypes
Recap: All parties completed 2 hrs of independent work. (53hrs since project start)
* discuss what parts of each prototype we want to continue working with
* Outline connection methodology -> network
* Josh to start with new frontend


--------------------------------------------------------------------------------------
2024-01-22 (2hrs)
Goals: Weekly assignment
Recap: All parties completed 6 hrs of independent work. (61hrs since project start)
* Josh has new frontend prototype 
	* tkinter 
* New backend prototype using constant network connections (should we do this)
* User docs
	* Frontend good enough to write docs for
	* Other docs are temp as we build things out

2024-01-25 (2hrs)
Goals: Discuss how we are moving forward
Recap: All parties completed 1 hrs of independent work. (64hrs since project start)
* Centralized server where everything is communicating with http html json requests
* More functions added to frontend

--------------------------------------------------------------------------------------
2024-02-05 (2hrs)
Goals: Discuss how we are moving forward
Recap: All parties completed 4 hrs of independent work. (67hrs since project start)
* Josh continues to work on the frontend
	* Network map
	* event view
	* crash handles
* Chad continues on docs


2024-02-08 (2hrs)
Goals: Discuss how we are moving forward
Recap: All parties completed 1 hrs of independent work. (70hrs since project start)
* Josh continues on frontend
	* score management
	
--------------------------------------------------------------------------------------
2024-02-12 (2hrs)
Goals: Weekly assignment
Recap: All parties completed 0 hrs of independent work. (72hrs since project start)
* Slidedeck	
	* outline responsbilities and start


2024-02-15 (2hrs)
Goals: Discuss how we are moving forward
Recap: All parties completed 4 hrs of independent work. (78hrs since project start)
* Josh continues on frontend
	* stop continued connection, move to single http requets
* Chad continues work on backend
* both work on slide deck
	
--------------------------------------------------------------------------------------
2024-02-19 (2hrs)
Goals: Weekly assignment
Recap: All parties completed 0 hrs of independent work. (80hrs since project start)
* Josh continues on frontend
* Chad continues on backend


2024-02-22 (2hrs)
Goals: Discuss how we are moving forward
Recap: All parties completed 4 hrs of independent work. (86hrs since project start)
* Chad shows main central sever
	* group testing with current infrastructure
	* moddify things to fit

--------------------------------------------------------------------------------------
2024-02-26 (2hrs)
Goals: Weekly assignment
Recap: All parties completed 8 hrs of independent work. (96hrs since project start)
* Josh continues on frontend
	* continued integration
* Josh works on actual network
* Chad continues on backend
	* Move to docker
* Outline what we need on expo poste


2024-02-29 (2hrs)
Goals: Discuss how we are moving forward
Recap: All parties completed 2 hrs of independent work. (100hrs since project start)
* EXpo poster

--------------------------------------------------------------------------------------
2024-03-18 (2hrs)
Goals: Weekly assignment
Recap: All parties completed 16 hrs of independent work. (118hrs since project start)
* Josh Backend
	* Network
	* basic proxy
	* Basic monitor
	* easy container start
	* basic docker manager
	* wrote basic manual tests for all things
* Chad backend
	* fixing server bugs and mantaince


2024-03-21 (2hrs)
Goals: Discuss how we are moving forward
Recap: All parties completed 6 hrs of independent work. (126hrs since project start)
* Assignment
* Monitor pushes info to server
* Chad backend central server continued improvements
* new boot instructions
* manager works 
* command systems starting to work on the frontend

--------------------------------------------------------------------------------------
2024-03-25 (2hrs)
Goals: Weekly assignment
Recap: All parties completed 6 hrs of independent work. (134hrs since project start)
* frontend continued integration with backend
* backend overhaul


2024-03-28 (2hrs)
Goals: Discuss how we are moving forward
Recap: All parties completed 6 hrs of independent work. (142hrs since project start)
* New compose generator
* backend fixes
* big monitor refactor for better optimization


--------------------------------------------------------------------------------------
2024-04-01 (2hrs)
Goals: Weekly assignment
Recap: All parties completed 6 hrs of independent work. (150hrs since project start)
* Auto adversary bones based on monitor
* Lots of backend work
* updated docs


2024-04-04 (2hrs)
Goals: Discuss how we are moving forward
Recap: All parties completed 6 hrs of independent work. (158hrs since project start)
* things wrapping up
* new start scripts
* AA finished
* Frontend features complete
* updated tests 
* Chad adding  challenges
* Remove unneeded things