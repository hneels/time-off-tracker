TIME-OFF TRACKER

video demo HERE: https://youtu.be/u9AkfSJnACE

Time-Off Tracker is a web-based application which allows company managers to track paid and unpaid time off for a large database of employees. I work for a medium-sized company and oversee a staff team of about 75 employees, and in the past we used a spreadsheet to manually add and subtract time-off hours that employees earned and used. This system was inefficient, and we had no way to track unpaid time-off requests. This application allows multiple users (managers, directors, and HR employees) to add new employees to the system, add PTO hours earned, subtract paid- and unpaid- time off used, view employees totals, and view the history of all time-off exchanges. This particular application is emblazoned with the logo and brand of my company, Turnbridge, but the app can be easily modified to accomodate various company branding. The individual website pages are broken down as follows:

INDEX
The INDEX, or home page (found at "/"), shows the history of all time-off exchanges for every employee since the database was created. For example, if an employee earned 8 PTO hours for working on a holiday, or took 16 unpaid-time-off hours for a holiday, or used 8 paid-time-off hours for a sick day, each exchange will be listed in descending order on the Index table.

VIEW TOTALS
The VIEW TOTALS page (found at "/totals") presents a drop-down list of all employees in the system. When an employee is selected, the page displays a table of that employee's totals. The following information is listed:
Total PTO hours remaining
Eligibility Date: when they become eligible to start using PTO
Starting PTO Hours: how many hours they started with at time of hire
PTO hours earned: any hours earned since being added to the system (such as for working holidays)
PTO Hours Used
Unpaid Time-Off Hours: hours for which they requested not to work their regularly scheduled shifts, but were not paid
Total Hours Off: the sum of paid AND unpaid hours they have requested off work
Below that, the site displays the history of all time-off exchanges for that specific employee.

ADD EMPLOYEE
The ADD EMPLOYEE page (found at "/employee") displays a form for adding new employees to the system. Users must specify the employee's full name, PTO eligiblity date (when they can start using PTO), and starting PTO hours (as determined by HR, prorated from the beginning of the year). The form rejects invalid or incomplete input.

ADD PTO EARNED
The ADD PTO EARNED page (found at "/add") displays a form for adding earned PTO to an employee's PTO total. Users must select an employee from the drop-down list of all employees in the database, specify the number of hours earned, and the reason PTO was earned. (Employees can earn PTO for working on holidays, as well as 'juice' PTO which means a Director has elected to give them extra PTO hours for a job well done.)

SUBTRACT TIME OFF
The SUBTRACT TIME OFF page (found at "/subtract") displays a form for subtracting paid- or unpaid- time-off an employee uses. Users must select from the drop-down list of all employees in the database, specify the number of hours used, the start and end date of their time-off period, the reason they took time off (for example, sick or vacation), and whether that time was paid (PTO) or unpaid (UTO).
When submitted, this form does two things:
Updates that employee's paid- or unpaid- time off totals
Updates the history table to document that specific time-off exchange

Additionally, the application has a SUCCESS function to alert users when an employee has been successfully added or updated, and an ERROR funtion to alert users when information was entered incorectly and the database could not be updated (such as an incomplete form, or trying to add an employee whose name is already in the database).
