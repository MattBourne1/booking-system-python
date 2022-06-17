# Assignment 7

## Time to complete this assignment:

You have two weeks for this assignment.

## Motivation:

You have been hired to build a booking quote system for transporting packages. 
You will write this system in Python, as a terminal application. You will use 
simple terminal IO (input and print) as a user interface for now. Another 
developer in the future will convert this to a server application that is 
front-ended with a browser (you don’t need to worry about how this happens as 
it's not part of your work, but it can and should influence how you build your 
system).

The application you are building will capture the following information:

* Name of the customer.
* Package description.
* Are the contents dangerous? [Y/N]
* Weight (kgs).
* Volume (cubic meters).
* Required delivery date (month/date/year).
* International destination? [Y/N]

The application will then attempt to find the best way to route the package (air / ground / ocean).

The rules it will use are as follows:

1. Packages can only be shipped if they weigh less than 10Kg **or** are smaller 
than 5x5x5 meters (125 cubic meters).
1. If the package contains dangerous goods it cannot be routed via air.
1. 'Urgent' means a package has to be delivered in less than 3 business days.
1. If the package is urgent it will be routed via air, if possible.
1. If the package is heavy or large (towards the maximum end of the boundaries 
set in 1 above), and is not urgent, it can be routed via truck (or even ocean 
if it is for an international destination).
1. Air shipments cost $10 per kilogram or $20 per cubic meter, whichever is 
the highest.
1. Truck shipments cost a flat rate of $25, or $45 if urgent.
1. Ocean shipments costs a flat rate of $30.

Your system will apply these rules to the booking and will calculate 
alternative shipping options (or one, or possibly none, depending on how the 
above rules affect the booking).

The shipping options must be printed in a clearly understood format, and 
should be appended to a booking_quotes.csv file. There will be one row in the
file for each quote.

This application is to be developed using an object oriented approach.

It will require extensive automated tests to ensure the above rules are 
correctly applied by the system.

## Here is what you need to do:

1. Use automated testing to validate the system behaves as intended.
1. Develop the data capture functionality, paying careful attention to any 
implied data needs.
1. Make sure the data is validated, so data entry errors can be prevented as 
much as possible.
1. Build a menu so the system is easy to use.
1. Ensure each booking has a unique id.
1. Make use of formatting techniques to ensure that information reported to 
the screen is well laid out and easy to understand.
1. Be sure each booking quote is stored in the csv file.
1. Be sure to commit to local git frequently and use a virtual environment.

## Submission:

Your submission should include the following:

1. All Python (.py) files, including tests, that you developed.
1. The csv file with some quote data in it.
1. Any other files required to run your code.
1. You also need to upload your code to Canvas, uploading it as a pull request.
1. In Canvas, add a comment to your submission with a link to your pull request.

Your submission **should not** include your virtual environment.

## Tips

1. Be creative! Use this as an oportunity to reflect on everything you have 
learned so far and apply it to application development.
1. Consider making your user interface fully separated from the rest of the project. This will make it
easier to implement a new web-based interface later on without having to modify the underlying implementation.
1. Use your time well, two weeks might seem like a lot, but you will run out of time if you
wait too much to get started. At the end of the first week, you should have the first
*draft* of your project, so that you can devote the second week fixing potential crashes
and adding any missing features.
