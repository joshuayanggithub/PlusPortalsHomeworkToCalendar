# Purpose
Automatically export PlusPortals upcoming coursework to ToDoList (todoist.com), which the site itself has features for 2 way sync with Google calendar and. 1 way sync wih Apple calendar.

# Workings
With your login info on plusportals, and api token for todoist, sync is possible to achieve, with requests happening on a given interval, 10 minutes a good intervals since teachers barely use plusportals anyways. However, at the moment you have to manually retrieve a _requestVerificationToken value for the get API request to work_.  

**Lack of organization and the workingtoken variable problem will be fixed around the school year**
