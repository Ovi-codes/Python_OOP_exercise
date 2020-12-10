# # Assessment - Object-oriented programming

# This code was originally written in Jupyter Notebook, hence the 'block' style of comments and prompts

# In this exercise, we'll create a few classes to simulate a server that's taking connections from the outside and
# then a load balancer that ensures that there are enough servers to serve those connections. To represent the
# servers that are taking care of the connections, we'll use a Server class. Each connection is represented by an id,
# that could, for example, be the IP address of the computer connecting to the server.  For our simulation,
# each connection creates a random amount of load in the server, between 1 and 10.

import random


class Server:
    def __init__(self):
        """Creates a new server instance, with no active connections."""
        self.connections = {}

    def add_connection(self, connection_id):
        """Adds a new connection to this server."""
        connection_load = random.random() * 10 + 1
        # Add the connection to the dictionary with the calculated load
        self.connections[connection_id] = connection_load

    def close_connection(self, connection_id):
        """Closes a connection on this server."""
        # Remove the connection from the dictionary
        del self.connections[connection_id]

    def load(self):
        """Calculates the current load for all connections."""
        total = 0
        # Add up the load for each of the connections
        for given_connection in self.connections:
            total += self.connections[given_connection]
        return total

    def __str__(self):
        """Returns a string with the current load of the server"""
        return "{:.2f}%".format(self.load())


# Now run the following code to create a Server instance and add a connection to it, then check the load:

server = Server()
server.add_connection("192.168.1.1")

print(server.load())

# If your output is a random number between 1 and 10, you have successfully coded the `add_connection` and `load`
# methods of the Server class.  Well done!


server.close_connection("192.168.1.1")
print(server.load())


# You have successfully coded the `close_connection` method if the cell above prints 0.

# Let's look at the basic LoadBalancing class. This class will start with only one server available. When a
# connection gets added, it will randomly select a server to serve that connection, and then pass on the connection
# to the server. The LoadBalancing class also needs to keep track of the ongoing connections to be able to close
# them.


class LoadBalancing:
    def __init__(self):
        """Initialize the load balancing system with one server"""
        self.connections = {}
        self.servers = [Server()]

    def add_connection(self, connection_id):
        """Randomly selects a server and adds a connection to it."""
        server = random.choice(self.servers)
        # Add the connection to the dictionary with the selected server
        self.connections[connection_id] = server
        # Add the connection to the server
        server.add_connection(connection_id)
        self.ensure_availability()

    def close_connection(self, connection_id):
        """Closes the connection on the the server corresponding to connection_id."""
        # Find out the right server
        server = self.connections[connection_id]
        # Close the connection on the server
        server.close_connection(connection_id)
        # Remove the connection from the load balancer
        del self.connections[connection_id]

    def avg_load(self):
        """Calculates the average load of all servers"""
        # Sum the load of each server and divide by the amount of servers
        load = 0
        for server in self.servers:
            load += server.load()

        return load / len(self.servers)

    def ensure_availability(self):
        """If the average load is higher than 50, spin up a new server"""
        if self.avg_load() > 50:
            self.servers.append(Server())

    def __str__(self):
        """Returns a string with the load for each server."""
        loads = [str(server) for server in self.servers]
        return "[{}]".format(",".join(loads))


# This snippet should create a connection in the load balancer, assign it to a running server
# and then the load should be more than zero:

a = LoadBalancing()
a.add_connection("fdca:83d2::f20d")
print(a.avg_load())

# Be sure that the load balancer now has an average load more than 0 before proceeding.
# What if we add a new server?

a.servers.append(Server())
print(a.avg_load())

# The average load should now be half of what it was before.

a.close_connection("fdca:83d2::f20d")
print(a.avg_load())

# Fill in the code of the LoadBalancing class to make the load go back to zero once the connection is closed.

# Before, we added a server manually. But we want this to happen automatically when the average load is more
# than 50%. You can test it with the following code:


for connection in range(20):
    a.add_connection(connection)
print(a)

# The code above adds 20 new connections and then prints the loads for each server in the load balancer.  If you
# coded correctly, new servers should have been added automatically to ensure that the average load of all servers is
# not more than 50%. Run the following code to verify that the average load of the load balancer is not more
# than 50%.

print(a.avg_load())
