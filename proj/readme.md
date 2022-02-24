Project Title

My project is an Enterprise Rsource Planner (ERP). Orgaizations can use it to aggregate their oerations.

Employees can register and choose their department to access that department's resources.

The departments included are:

`	`- Accounting

`	`- Human Resource

`	`- Sales

The project is designed such that employees cannot access resource of department that is not theirs.


Distinctiveness and Complexity

My project is distinct from the class project as it is an ERP system.

Below are the features contained in the project:

Home/Landing Page: The landing page welcomes the user and their is an option to view the personal

information of the logged in user. The user can also edit their info.

Logged in user can also apply for leave. Each employee is entitled to 15 days leave in a year, days

applied for is deducted from the 15 and can no longer aplly once it remains zero. Also employee can

not apply for leave days more than they have remaining.

Accounting: the accounting department can generate an invoice/bill. There is an option to view and

download the invoice in pdf format.

Human Resource: Employee in Human Resource can view and edit information of employees. The information

saved will automatically reflect on the personal info page of the employee.

Sales: The sales page display the products that the company has available on sale. There is a feature to

add, edit and delete product (CRUD function). On the sales page, there is an option to download the

products list in an excel format.


JavaScript

The 'Darkmode' feature is also implemented. When the slde button is toggled it switches between the ligh and dark mode.

The present time and date is also displayed on the header with the use of javascript



Files Created

Four Apps were created for this project:

`	`- accounting

`	`- erp

`	`- hrm

`	`- sale

Each of the files contain the following:

views.py contains the backend logic fr the view function

urls.py contains the url patterns/route/endpoint for the view functions.

models.py contains the database table for each app.

forms.py contains the ModelForm for each application.

templates folder contains the html files that was rendered to the web page.

The erp app contains static folder that contains the css and javascript file that the project app runs on.


Run the Application

To run the application, type 'python manage.py runserver'


