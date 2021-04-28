"""Customers at Hackbright."""


class Customer(object):
    """Ubermelon customer."""

    def __init__(self, 
                first_name, 
                last_name, 
                email_address, 
                password):

        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.password = password

    def __repr__(self):
        """ Convinience method to show information about customer in console. """
        return f"<Customer: {self.first_name} {self.last_name} {self.email_address}>"


def read_customers_from_file(filepath):
    """Read customer data and populate dictionary of customers.

    Dictionary will be {email_address: Customer object}
        """   
    customers = {}

    with open(filepath) as file:
        for line in file:
            (first_name,
            last_name, 
            email_address, 
            password) = line.strip().split('|')


            customers[email_address] = Customer(first_name, 
                                        last_name, 
                                        email_address, 
                                        password)
    
    return customers


def get_by_email(email_address):
    """ Return a customer, given its email address."""
    if email_address not in customers:
        return {}

    return customers[email_address]


customers = read_customers_from_file("customers.txt")
