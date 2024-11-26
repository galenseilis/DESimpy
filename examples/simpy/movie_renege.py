##############
# $0 IMPORTS #
##############

import random
import heapq
import warnings

from desimpy import Event, EventScheduler

####################
# $1 CONFIGURATION #
####################

warnings.warn("This example has not been validated. Results may be incorrect.")

RANDOM_SEED = 42
TICKETS = 50  # Number of tickets per movie
SELLOUT_THRESHOLD = 2  # Fewer tickets than this is a sellout
SIM_TIME = 120  # Simulate until
MOVIES = ["Python Unchained", "Kill Process", "Pulp Implementation"]

#####################
# $2 DEFINE THEATER #
#####################


class Theater:
    def __init__(self, env, tickets, movies):
        self.env = env
        self.counter = TicketAgent(env, self)
        self.movies = movies
        self.available = {movie: tickets for movie in movies}
        self.sold_out = {movie: False for movie in movies}
        self.when_sold_out = {movie: None for movie in movies}
        self.num_renegers = {movie: 0 for movie in movies}


#######################
# $3 DEFINE MOVIEGOER #
#######################


def moviegoer(movie: str, num_tickets: int, theater):
    theater.counter.request(movie, num_tickets)


###############################
# $4 DEFINE CUSTOMER ARRIVALS #
###############################


def customer_arrivals(env: EventScheduler, theater: Theater):
    delay = random.expovariate(1 / 0.5)
    movie = random.choice(theater.movies)
    num_tickets = random.randint(1, 6)

    def action():
        if theater.available[movie]:
            env.timeout(0, moviegoer(movie, num_tickets, theater))
        customer_arrivals(env, theater)

    env.timeout(delay, action=action)


#######################
# DEFINE TICKET AGENT #
#######################


class TicketAgent:
    def __init__(self, env, theater):
        self.env = env
        self.theater = theater
        self.queue = []
        self.current_job = None

    def request(self, movie, num_tickets):
        if self.queue:
            self.schedule_job(movie, num_tickets)
        else:
            self.schedule_request(movie, num_tickets)

    def schedule_job(self, movie, num_tickets):
        job = self.create_job(movie, num_tickets)
        self.current_job = job
        self.env.schedule(job)

    def create_job(self, movie, num_tickets):
        time = self.env.current_time
        action = self.complete_service
        context = {"movie": movie, "num_tickets": num_tickets}
        return Event(time, action, context)

    def delay_before_next_job(self, delay: float) -> None:
        """Server is delayed before resuming duties.

        For example, sometimes server will have a discussion
        with a customer.
        """
        if self.queue:
            _, movie, num_tickets = heapq.heappop(self.queue)
            action = lambda: self.schedule_job(movie, num_tickets)
            self.env.timeout(delay, action=action)

    def complete_service(self):
        movie = self.current_job.context["movie"]
        num_tickets = self.current_job.context["num_tickets"]
        self.current_job = None

        if self.theater.sold_out[movie]:
            self.theater.num_renegers[movie] += 1
            self.delay_before_next_job(0)
            return

        if self.theater.available[movie] < num_tickets:
            self.delay_before_next_job(0.5)
            return

        theater.available[movie] -= num_tickets
        if self.theater.available[movie] < SELLOUT_THRESHOLD:
            self.theater.sold_out[movie] = True
            self.theater.when_sold_out[movie] = self.env.current_time
            theater.available[movie] = 0

        self.delay_before_next_job(1)

    def schedule_request(self, movie, num_tickets):
        queue = self.queue
        time = self.env.current_time

        heapq.heappush(queue, (time, movie, num_tickets))


if __name__ == "__main__":
    ##############################
    # INITIALIZE EVENT SCHEDULER #
    ##############################

    env = EventScheduler()

    ###########################
    # CREATE MOVIE THEATER #
    ###########################

    theater = Theater(env, TICKETS, MOVIES)

    ######################
    # REGISTER PROCESSES #
    ######################

    env.timeout(0, customer_arrivals(env, theater))

    ##################
    # RUN SIMULATION #
    ##################

    env.run_until_max_time(SIM_TIME, logging=False)

    ####################
    # ANALYSIS/RESULTS #
    ####################

    for movie in MOVIES:
        if theater.sold_out[movie]:
            sellout_time = theater.when_sold_out[movie]
            num_renegers = theater.num_renegers[movie]
            print(
                f'Movie "{movie}" sold out {sellout_time:.1f} minutes '
                f"after ticket counter opening."
            )
            print(
                f"  Number of people leaving queue when film sold out: {num_renegers}"
            )
        else:
            print(theater.available[movie])
