"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import melons, customers

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
# app.secret_key = 'this-should-be-something-unguessable'
app.secret_key = '%April17Lab@'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # The logic here will be something like:
    #
    # - get the cart dictionary from the session
    cart = session.get("cart",{})
    # - create a list to hold melon objects and a variable to hold the total
    #   cost of the order
    melon_list = []
    total_order = 0

    # - loop over the cart dictionary, and for each melon id:
    #    - get the corresponding Melon object
    #    - compute the total cost for that type of melon
    #    - add this to the order total

    for melon_id, quantity in cart.items():
        melon = melons.get_by_id(melon_id)

        melon_cost = quantity * melon.price
        total_order = total_order + melon_cost
        
    #    - add the Melon object to the list created above
        melon_list.append(melon)

    #    - add quantity and total cost as attributes on the Melon object
        melon.quantity = quantity
        melon.melon_cost = melon_cost

    # - pass the total order cost and the list of Melon objects to the template
    #
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session

    return render_template("cart.html", cart = melon_list, total = total_order)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    # The logic here should be something like:
    #
    # - check if a "cart" exists in the session, and create one (an empty
    #   dictionary keyed to the string "cart") if not
    if 'cart' in session:
        
        cart = session['cart']
    else:
        cart = session['cart'] = {}
    
    # - check if the desired melon id is the cart, and if not, put it in
    # - increment the count for that melon id by 1
    cart[melon_id] = cart.get(melon_id, 0)+ 1
    # - flash a success message
    flash("Your melon was successfully added!")
    # - redirect the user to the cart page

    return redirect('/cart')


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # The logic here should be something like:
    # - get user-provided name and password from request.form
    user_email = request.form.get("email")
    user_password = request.form.get("password")
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    user = customers.get_by_email(user_email)

    if not user:
        flash("Sorry, this email-address does not exist in our system.")
        return redirect("/login")

    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    
    if user_password != user.password:
        flash("The password does not match our records.")
        return redirect("/login")

    session['logged_in_customer_email'] = user.email_address
    print(session)
    flash("Logged in successfully!")
    return redirect("/melons")    

    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist 

@app.route("/logout")
def process_logout():
    """Log the user out of the site."""

    del session['logged_in_customer_email']
    flash("Logged out succesfully!")
    return redirect("/melons")


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
