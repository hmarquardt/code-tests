# Exercise setup

This was a full stack web exercise, instructions are contained in the instructions.md file.   The file does in fact use a [composer](https://getcomposer.org/) 
package and dependency managerment, so if you're not familiar with that, you may need to do a little research to get this going if you want to see it run.

Essentially there is a PHP file that has a crude REST api, and a Javascript file that consumes that API and manages the display.  Bootstrap is used for styling.

Below is the original contents when I submitted the exercise.   For the record, I didn't get this job, they were already much further along with another candidate
and offered him the job the day after I submitted this.   I did get a nice note back on the exercise though.

> "Your exercise was elegant, and it seems like you've got the skills we would need, but since we only have the ability to bring on one new developer right now ..."

Quick and Dirty ISBN Price Checker
===============

Installation and Execution
---------------
- Update/checkout repository from github
- Change to repository directory
- Execute *composer install*
- Change to public directory
- Execute local PHP Server, e.g. *php -S localhost:8000*
- In browser, navigate to [http://localhost:8000](http://localhost:8000)
- Of course if you have functioning LAMP stack, feel free to improvise :)

Notes
---------------
- While a pure JavaScript solution might have been fun, this is a backend/full stack position, so I used PHP
- I don't enjoy pain so I accepted your generous offer of the API
- This is bootstrap, Underscore.js, jQuery and pure PHP, no other frameworks involved
- 93 lines of HTML, 34 lines of Javascript, and 49 lines of PHP
- I heeded your warning about error checking but couldn't make the Valore API fail, so
  - I have a blanket try/catch around the API call
  - I check for a zero recordset
  - I catch the AJAX fail
  - That's about it, if I find an error, I'll test for it
- I don't clear the input field on submit intentionally, was easier to incrementally add new ISBNs 

